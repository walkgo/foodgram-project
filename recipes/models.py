from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from slugify import slugify

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(
        max_length=50, verbose_name='Тег'
    )
    slug = models.SlugField(blank=True)
    checkbox_style = models.CharField(max_length=15, blank=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Название'
    )
    unit = models.CharField(
        max_length=20, verbose_name='Единица измерения', null=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=200, verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/', default='no_image.jpg', verbose_name='Изображение'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient',
        through_fields=('recipe', 'ingredient')
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги'
    )
    duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления в минутах'
    )
    slug = models.SlugField(
        unique=True, verbose_name='Путь'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, blank=True,
        null=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save()
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(self.id)
            self.save()


class RecipeIngredient(models.Model):
    amount = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name='Количество'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_follow'
            ),
            models.CheckConstraint(
                name='prevent_self_follow',
                check=~models.Q(user=models.F('author'))
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites',
        null=True
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites',
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_favorite'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopper',
        null=True
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_list',
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_shoplist'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
