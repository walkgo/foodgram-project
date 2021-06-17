# foodgram

![Django-app workflow](https://github.com/walkgo/foodgram-project/actions/workflows/foodgram_workflow.yaml/badge.svg)

Адрес: http://130.193.40.74/

Дипломный проект "Foodgram"

Сайт, на котором пользователи публикуют рецепты, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Для запуска на сервере необходим установленный Docker, docker-compose.

После запуска необходимо произвести ряд действий:

**Выполнить миграции:**

1. `docker-compose exec web python3 manage.py makemigrations`

2. `docker-compose exec web python3 manage.py migrate`

**Выполнить миграции:**

 - `docker-compose exec web python manage.py createsuperuser`

**Выполнить миграции:**

 - `docker-compose exec web python manage.py collectstatic`

**Выполнить миграции:**

 - `docker-compose exec web python manage.py loaddata fixtures.json`
 
 
#### Использованные технологии

Python, Django, Docker, Nginx, Postgresql, Gunicorn

***

**Licence** | [MIT](https://github.com/walkgo/yamdb_final/blob/master/LICENSE)

**Author** | [walkgo](https://github.com/walkgo/)