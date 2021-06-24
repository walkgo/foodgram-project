import json
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from recipes.models import (Favorite, Follow, Ingredient, Recipe, ShoppingList,
                            User)

SUCCESS_RESPONSE = JsonResponse({'success': True})
BAD_RESPONSE = JsonResponse(
    {'success': False}, status=HTTPStatus.BAD_REQUEST
)
NOT_FOUND_RESPONSE = JsonResponse(
    {'success': False}, status=HTTPStatus.NOT_FOUND
)


class Favorites(LoginRequiredMixin, View):
    """ Функция добавления/удаления рецепта из "Избранного"
    """
    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get('id')
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            _, created = Favorite.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            return JsonResponse({'success': created})
        return NOT_FOUND_RESPONSE

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(
            Favorite, recipe=recipe_id, user=request.user
        )
        recipe.delete()
        return SUCCESS_RESPONSE


class Follows(LoginRequiredMixin, View):
    """ Функция добавления/удаления подписок
    """
    def post(self, request):
        req_ = json.loads(request.body)
        author_id = req_.get('id')
        if author_id is not None:
            author = get_object_or_404(User, id=author_id)
            if request.user == author:
                return JsonResponse({'success': False})
            _, created = Follow.objects.get_or_create(
                user=request.user, author=author
            )
            return JsonResponse({'success': created})
        return NOT_FOUND_RESPONSE

    def delete(self, request, author_id):
        author = get_object_or_404(User, id=author_id)
        removed = Follow.objects.filter(
            user=request.user, author=author
        ).delete()
        if removed:
            return SUCCESS_RESPONSE
        return BAD_RESPONSE


class Purchases(LoginRequiredMixin, View):
    """ Функция добавления/удаления рецептов в список покупок
    """
    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get('id')
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            _, created = ShoppingList.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            return JsonResponse({'success': created})
        return NOT_FOUND_RESPONSE

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        removed = ShoppingList.objects.filter(
            user=request.user, recipe=recipe
        ).delete()
        if removed:
            return SUCCESS_RESPONSE
        return BAD_RESPONSE


class Ingredients(LoginRequiredMixin, View):
    """ Функция получения списка ингредиентов
    """
    def get(self, request):
        text = request.GET['query']
        ingredients = list(
            Ingredient.objects.filter(title__icontains=text).values(
                'title', 'unit'
            )
        )
        return JsonResponse(ingredients, safe=False)
