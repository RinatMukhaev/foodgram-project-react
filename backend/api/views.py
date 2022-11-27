from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Subscription, User

from .filters import IngredientFilter, RecipeFilter
from .mixins import GetCreateDeleteViewSet
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, ShowSubscriptionsSerializer,
                          SubscriptionSerializer, TagSerializer)


class SubscribeViewSet(GetCreateDeleteViewSet):
    """ Операция подписки/отписки. """

    permission_classes = [IsAuthenticated, ]
    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        Subscription.objects.create(
            user=request.user, author=user)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Subscription, user__id=user_id, author__id=author_id)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShowSubscriptionsView(ListAPIView):
    """ Отображение подписок пользователя. """
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination

    def get(self, request):
        user = request.user
        queryset = User.objects.filter(author__user=user)
        page = self.paginate_queryset(queryset)
        serializer = ShowSubscriptionsSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


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
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

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


class BaseFavoriteShoppingCartViewSet(GetCreateDeleteViewSet):
    """ Обработка любимых рецептов и модели корзины. """

    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.model.objects.create(
            user=request.user, recipe=recipe)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        object = get_object_or_404(
            self.model, user__id=user_id, recipe__id=recipe_id)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(BaseFavoriteShoppingCartViewSet):
    """ Обработка модели корзины. """

    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    model = ShoppingCart


class FavoriteViewSet(BaseFavoriteShoppingCartViewSet):
    """ Обработка любимых рецептов моделей. """

    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    model = Favorite
