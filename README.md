

![examp workflow](https://github.com/VladimirKobenyakov/yamdb_final/actions/workflows/main.yml/badge.svg)


# Учебный проект yamdb_final
# Автор - Владимир Кобеняков

Проект разработан и реализован в рамках обучения по специальности Python-разработчик в Яндекс Практикум
Данный проект - это платформа для получения и добавления пользователями информации о книгах и фильмах. В нем имеется возможность добавления категорий, произведений, а также оставления отзывов о произведениях и комментариев к данным отзывам.


В проекте используются следующие технологии:
>asgiref==3.2.10
> 
>Django==2.2.16
> 
>django-filter==2.4.0
> 
>djangorestframework==3.12.4
> 
>djangorestframework-simplejwt==4.8.0
> 
>gunicorn==20.0.4
> 
>psycopg2-binary==2.8.6
> 
>PyJWT==2.1.0
> 
>pytz==2020.1
> 
>sqlparse==0.3.1

# Для запуска используйте следующие команды

```sh
docker-compose up
```

Затем из директории infra_sp2/infra поочередно выполните следующие команды:

```sh
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```

# Примеры запросов API:
http://localhost/api/v1/auth/token/
http://localhost/api/v1/auth/signup/
http://localhost/api/v1/users/
