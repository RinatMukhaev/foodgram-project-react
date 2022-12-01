![example workflow](https://github.com/RinatMukhaev/foodgram-project-react/actions/workflows/main.yml/badge.svg)

### Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

### Адрес проекта
http://51.250.9.76/

### Адрес для аминистратора
http://51.250.9.76/admin/

login: admin@admin.ru
password: admin753

### Название
FOODGRAM

### Описание
Cайт Foodgram - онлайн-сервис, на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, употреблять для приготовления одного набора или выбранных блюд.

### Установка и требования

- Регистрация на dockerhub
- Настроенный SSH доступ к серверу по ключу с паролем
- Регистрация на GitHub
- Выделенный сервер Linux Ubuntu 20.04 с с публичным IP адресом

#### Настройка GitHub Secrets
Клонируйте репозиторий и настройте переменные GitHub secrets согласно Вашему окружению

- DOCKER_PASSWORD
- DOCKER_USERNAME
- SERVER_HOST #публичный адрес сервера для доступа по SSH
- SERVER_SUDO_USER
- SSH_KEY #Скопируйте приватный ключ с компьютера, имеющего доступ к боевому серверу: cat ~/.ssh/id_rsa
- SSH_PASSWORD
- DB_ENGINE пример django.db.backends.postgresql
- DB_NAME #имя образа docker-compose с базой - db
- DB_POSTGRES_USER
- DB_POSTGRES_PASSWORD
- DB_HOST
- DB_PORT

#### Установка на выделенном сервере
На боевом сервере установите docker и docker-compose
Остановите службу nginx
Скопируйте файлы из директории infra в домашную папку пользователя
    docker-compose.yaml
    nginx - сохраняя стурктуру и название папок

#### Deploy автоматически при команде git push
при git push запускается скрипт GitHub actions который выполняет автоматический deploy на сервер
