from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    subscriptions_detail, subscriptions_list)

app_name = 'api'

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path(
        'users/subscriptions/',
        subscriptions_list,
        name='subscriptions'
    ),
    path(
        'users/<int:id>/subscribe/',
        subscriptions_detail,
        name='subscribe_detail'
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
