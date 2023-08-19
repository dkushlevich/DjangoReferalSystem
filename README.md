<div align=center>
  
  # DjangoReferalSystem <br> (Реализация тестового задания) <br> [Деплой](https://referalsystem.ddns.net)
  
  [![ReferalSystem_CI/CD](https://github.com/dkushlevich/DjangoReferalSystem/workflows/ReferalSystem_CI/CD/badge.svg)](https://github.com/dkushlevich/DjangoReferalSystem/workflows/ReferalSystem_CI/CD/badge.svg)
  
  ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
  ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
  ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

  ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
  ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
  ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
  
  ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)


</div>


## Описание тестового задания


### Задание:
Реализовать простую реферальную систему. Минимальный интерфейс для
тестирования

### Реализовать логику и API для следующего функционала :

- Авторизация по номеру телефона. Первый запрос на ввод номера
телефона. Имитировать отправку 4хзначного кода авторизации(задержку
на сервере 1-2 сек). Второй запрос на ввод кода

- Если пользователь ранее не авторизовывался, то записать его в бд

- Запрос на профиль пользователя

- Пользователю нужно при первой авторизации нужно присвоить
рандомно сгенерированный 6-значный инвайт-код(цифры и символы)

- В профиле у пользователя должна быть возможность ввести чужой
инвайт-код(при вводе проверять на существование). В своем профиле
можно активировать только 1 инвайт код, если пользователь уже когда-
то активировал инвайт код, то нужно выводить его в соответсвующем
поле в запросе на профиль пользователя

- В API профиля должен выводиться список пользователей(номеров
телефона), которые ввели инвайт код текущего пользователя.

- Реализовать и описать в readme Api для всего функционала

- Создать и прислать Postman коллекцию со всеми запросами

- Залить в сеть, чтобы удобнее было тестировать(например бесплатно на
https://www.pythonanywhere.com или heroku)

#### Опционально:

- Интерфейс на Django Templates

- Документирование апи при помощи ReDoc

- Docker

#### Ограничения на стек технологий:

- Python

- Django, DRF


## Описание проекта


DjangoReferalSystem - REST API проект написанный на DRF, в котором представлена реферальная система для зарегистрированных пользователей.

## Пользовательские роли и права доступа

* **Аноним** — доступны эндпоинты регистрации и получения токена.
* **Аутентифицированный пользователь** (user) — доступны эндпоинты `users/me` и `users/activate_invite_code`, с помощью которых пользователь может получать и редактировать информацию о себе и активировать инвайт код от других пользователей соответственно. Эта роль присваивается по умолчанию каждому новому пользователю.
* **Администратор** обладает доступом в админ-панель, дополнительно к аутентифицированному пользователю доступны эндпоинты просмотра информации о всех пользователях (`users/`), просмотр информации о конкретном пользователе (GET-запрос `users/{phone_number}`) и полная блокировка пользователя (DELETE-запрос `users/{phone_number}`).

## Алгоритм регистрации нового пользователя

* Пользователь отправляет POST-запрос на добавление нового пользователя с параметром phone_number на эндпоинт `/api/v1/auth/signup/`.
* Пользователь получает код подтверждения (confirmation_code) на указанный телефонный номер.
* Пользователь отправляет POST-запрос с параметрами phone_number и confirmation_code на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
* При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).
  

## Алгоритм активации инвайт кода

* Пользователь получает код приглашения от другого пользователя.
* Предварительно авторизовавшись, пользователь отправляет POST-запрос с кодом к эндпоинту `/api/v1/users/activate_invite_code/`.
* В случае валидности предоставленного кода создаётся связь в БД между текущим пользователем и ползователем, предоставившим код.
  
> Блокировка пользователя предоставившего код не влияет на пользователя, активировавшего код

## CI/CD проекта

В реализованном с помощью GitHub Actions CI/CD пайплайне после пуша в main выполняются следующие задания:

- **tests:** запуск pytest.
- **build_and_push_to_docker_hub:** сборка и размещение образов проекта на DockerHub.
- **deploy:** автоматический деплой на сервер и запуск проекта.

---

<details>
  <summary>
    <h2>Запуск проекта на локальном сервере</h2>
  </summary>



> Для MacOs и Linux вместо python использовать python3

1. Клонировать репозиторий.
   ```
   $ git@github.com:dkushlevich/DjangoReferalSystem.git
   ```
2. Cоздать и активировать виртуальное окружение, установить зависимости:
   - **pip**

     ```
      $ cd /referalsystem/
      $ python -m venv venv
     ```
    
    Для Windows:
    ```
      $ source venv/Scripts/activate
    ```
    Для MacOs/Linux:
    ```
      $ source venv/bin/activate
    ```

    ```
    (venv) $ python -m pip install --upgrade pip
    (venv) $ pip install -r requirements.txt
    ```
    - **poetry**
    ```
    cd /referalsystem/
    poetry install
    ```
  
5. Создать секретный ключ приложения:
    * Создать файл .env в корневой папке проекта
    * Сгенерировать секретный ключ с помощью команды:
        ```
        (venv) $ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
        ```
    *  Заполнить файл env по шаблону:
        ```env
        DATABASE=sqlite #(Если необходимо работать с postgres - удалите данную запись)
        DEBUG=True
        
        SECRET_KEY = <ваш секретный ключ>
        ALLOWED_HOSTS=<IP сервера>, <Домен сервера>
        POSTGRES_USER=django_user
        POSTGRES_PASSWORD=django_password
        POSTGRES_DB=django_db
        
        DB_HOST=db
        DB_PORT=5432
        ```


6. Выполнить миграции:
    ```
    (venv) $ python manage.py migrate
    ```

7. Запустить сервер:
    ```
    (venv) $ python manage.py runserver
    ```
После выполнения вышеперечисленных инструкций бэкенд проекта будет доступен по адресу http://127.0.0.1:8000/

> Подробная документация API доступна после запуска сервера по адресу http://127.0.0.1:8000/redoc/

</details>

---

<details>
  <summary>
    <h2>Запуск проекта на удалённом сервере</h2>
  </summary>

1. Создать директорию referalsystem/ в домашней директории сервера.

2. В корне папки referalsystem/ поместить файл .env, заполнить его по шаблону

  ```env
    SECRET_KEY = <ваш секретный ключ>
    ALLOWED_HOSTS=<IP сервера>, <Домен сервера>
    POSTGRES_USER=django_user
    POSTGRES_PASSWORD=django_password
    POSTGRES_DB=django_db
    
    DB_HOST=db
    DB_PORT=5432
```

4. Установить Nginx и настроить конфигурацию так, чтобы все запросы шли в контейнеры на порт 8000.

    ```bash
        sudo apt install nginx -y 
        sudo nano etc/nginx/sites-enabled/default
    ```
    
    Пример конфигурация nginx
    ```bash
        server {
            server_name <Ваш IP> <Домен вашего сайта>;
            server_tokens off;
            client_max_body_size 20M;
        
            location / {
                proxy_set_header Host $http_host;
                proxy_pass http://127.0.0.1:8000;
        }
    ```
    
    > При необходимости настройте SSL-соединение

5. Установить docker и docker-compose
   
``` bash
    sudo apt update
    sudo apt install curl
    curl -fSL https://get.docker.com -o get-docker.sh
    sudo sh ./get-docker.sh
    sudo apt-get install docker-compose-plugin     
```

4. Форкнуть данный репозиторий и добавить в Secrets GitHub Actions переменные окружения

``` env
    DOCKER_USERNAME=<имя пользователя DockerHub>
    DOCKER_PASSWORD=<пароль от DockerHub>
    
    USER=<username для подключения к удаленному серверу>
    HOST=<ip сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш приватный SSH-ключ>
    
```
5. Запустить workflow проекта выполнив команды:

```bash
  git add .
  git commit -m ''
  git push
```
6. После этого выпонятся следующие workflow jobs:

- **tests:** запуск pytest.
- **build_and_push_to_docker_hub:** сборка и размещение образа проекта на DockerHub.
- **deploy:** автоматический деплой на боевой сервер и запуск проекта.

> С примерами запросов можно ознакомиться в [спецификации API](https://referalsystem.ddns.net/redoc/)


</details>

<div align=center>

## Контакты

[![Telegram Badge](https://img.shields.io/badge/-dkushlevich-blue?style=social&logo=telegram&link=https://t.me/dkushlevich)](https://t.me/dkushlevich) [![Gmail Badge](https://img.shields.io/badge/-dkushlevich@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:dkushlevich@gmail.com)](mailto:dkushlevich@gmail.com)

</div>
