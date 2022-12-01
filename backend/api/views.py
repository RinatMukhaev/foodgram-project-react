from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Subscription, User

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, ShowSubscriptionsSerializer,
                          SubscriptionSerializer, TagSerializer)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscriptions_list(request):
    """
    Вывод списка подписок.
    """
    subscriptions = User.objects.filter(following__user=request.user)
    paginator = CustomPagination()
    page = paginator.paginate_queryset(subscriptions, request=request)
    serializer = ShowSubscriptionsSerializer(
        page, many=True, context={'request': request}
    )
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscriptions_detail(request, id):
    """
    Добавление, удаление подписки.
    """
    author = get_object_or_404(User, id=id)
    if request.method == 'POST':
        data = {
            'user': request.user.id,
            'author': author.id
        }
        serializer = SubscriptionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if Subscription.objects.filter(user=request.user, author=author).exists():
        subscription = get_object_or_404(
            Subscription, user=request.user, author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ Отображение тегов. """

    permission_classes = [AllowAny, ]
    pagination_class = None
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get',)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Отображение ингредиентов. """

    permission_classes = [AllowAny, ]
    pagination_class = None
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [IngredientFilter, ]
    search_fields = ['^name', ]
    http_method_names = ('get',)


class RecipeViewSet(viewsets.ModelViewSet):
    """ Операции с рецептами: добавление/изменение/удаление/просмотр. """

    pagination_class = CustomPagination
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'put', 'patch', 'delete',)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeSerializer
        return CreateRecipeSerializer

    def add_recipe(self, request, pk, serializer):
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, request, pk, model):
        recipe = get_object_or_404(Recipe, id=pk)
        if model.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            model.objects.filter(
                user=request.user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """
        Добавление рецепта в список покупок.
        """
        return self.add_recipe(request, pk, ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        """
        Удаление рецепта из списка покупок.
        """
        return self.delete_recipe(request, pk, ShoppingCart)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """
        Добавление рецепта в избранные.
        """
        return self.add_recipe(request, pk, FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        """
        Удаление рецепта из избранного.
        """
        return self.delete_recipe(request, pk, Favorite)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        ingredient_list = "Cписок покупок:"
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        for num, i in enumerate(ingredients):
            ingredient_list += (
                f"\n{i['ingredient__name']} - "
                f"{i['amount']} {i['ingredient__measurement_unit']}"
            )
            if num < ingredients.count() - 1:
                ingredient_list += ', '
        file = 'shopping_list'
        response = HttpResponse(
            ingredient_list, 'Content-Type: application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
        return response
