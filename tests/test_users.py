from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestUserAPI:
    users_url = '/api/v1/users/'

    def test_users_not_authenticated(self, client):
        response = client.get(self.users_url)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/v1/users/` не найден. Проверьте настройки в '
            '*urls.py*.'
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Проверьте, что GET-запрос к `/api/v1/users/` без токена '
            'авторизации возвращается ответ со статусом 401.'
        )
    
    def test_users_phone_number_not_authenticated(self, client, admin):
        response = client.get(f'/api/v1/users/{admin.phone_number}/')

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/v1/users/{phone_number}/` не найден. Проверьте '
            'настройки в *urls.py*.'
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Проверьте, что GET-запрос `/api/v1/users/{phone_number}/` без '
            'токена авторизации возвращает ответ со статусом 401.'
        )

    def test_users_me_not_authenticated(self, client):
        response = client.get('/api/v1/users/me/')

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/v1/users/me/` не найден. Проверьте настройки '
            'в *urls.py*.'
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Проверьте, что GET-запрос `/api/v1/users/me/` без токена '
            'авторизации возвращает ответ со статусом 401.'
        )
    
    def test_users_get_admin(self, admin_client, admin):
        response = admin_client.get('/api/v1/users/')
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/v1/users/` не найден.'
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос к `/api/v1/users/` с токеном '
            'авторизации возвращает ответ со статусом 200.'
        )
    
    def test_users_get_admin_only(self, user_client):
        url = '/api/v1/users/'

        response = user_client.get(url)

        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'Проверьте, что GET-запрос к `{url}` от пользователя, не '
            'являющегося администратором, возвращает ответ со статусом '
            '403.'
        )
    
    def test_users_phone_number_get_admin(self, admin_client, user):
        response = admin_client.get(f'/api/v1/users/{user.phone_number}/')
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/v1/users/{phone_number}/` не найден. Проверьте '
            'настройки в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос администратора к '
            '`/api/v1/users/{phone_number}/` возвращает ответ со статусом 200.'
        )

        response_data = response.json()
        expected_keys = (
            'first_name', 'last_name', 'phone_number',  'email', 'invite_code',
        )
        for key in expected_keys:
            assert response_data.get(key) == getattr(user, key), (
                'Проверьте, что ответ на GET-запрос администратора к '
                '`/api/v1/users/{phone_number}/` содержит данные пользователя.'
                f'Сейчас ключ {key} отсутствует в ответе либо содержит '
                'некорректные данные.'
            )

    def test_users_phone_number_get_not_admin(self, user_client, admin):

        response = user_client.get(f'/api/v1/users/{admin.phone_number}/')

        assert response.status_code == HTTPStatus.FORBIDDEN, (
            'GET-запрос пользователя, не обладающего правами '
            'администратора, отправленный к `/api/v1/users/{phone_number}/`, '
            'должен вернуть ответ со статусом 403.'
        )
    

    def test_users_phone_number_delete_user(
        self, user_client, user
    ):
        response = user_client.delete(f'/api/v1/users/{user.phone_number}/')
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            'Проверьте, что DELETE-запрос модератора к '
            '`/api/v1/users/{phone_number}/` возвращает ответ со статусом 403.'
        )

        assert user.is_active == True, (
            'Проверьте, что DELETE-запрос авторизованного ползователя к '
            '`/api/v1/users/{phone_number}/` не блокирует пользователя.'
        )
    
    def test_users_phone_number_delete_admin(
        self, 
        admin_client,
        user
    ):
        response = admin_client.delete(
            f'/api/v1/users/{user.phone_number}/'
        )

        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'Проверьте, что DELETE-запрос суперпользователя к '
            '`/api/v1/users/{phone_number}/` возвращает ответ со статусом 204.'
        )


    def test_users_me_get(self, user_client, user):
        response = user_client.get('/api/v1/users/me/')
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос обычного пользователя к '
            '`/api/v1/users/me/` возвращает ответ со статусом 200.'
        )

        response_data = response.json()
        expected_keys = ('first_name', 'last_name', 'phone_number',  'email', 'invite_code',)
        for key in expected_keys:
            assert response_data.get(key) == getattr(user, key), (
                'Проверьте, что GET-запрос к `/api/v1/users/me/` возвращает '
                'данные пользователя в неизмененном виде. Сейчас ключ '
                f'`{key}` отсутствует либо содержит некорректные данные.'
            )


    def test_users_me_patch(self, django_user_model,
                                  user_client, user):
        data = {'last_name': 'new_name'}

        response = user_client.patch('/api/v1/users/me/', data=data)
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что PATCH-запрос к `/api/v1/users/me/` доступен '
            'авторизованным пользователям и возвращает ответ со статусом 200.'
        )
        user = django_user_model.objects.filter(
            phone_number=user.phone_number
        ).first()
        assert user.last_name == data['last_name'], (
            'Проверьте, что PATCH-запрос к `/api/v1/users/me/` изменяет '
            'данные пользователя.'
        )
    

    def test_users_activate_invite_code_not_authenticated(self, client):
        response = client.get('/api/v1/users/activate_invite_code/')

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/v1/users/activate_invite_code/` не найден. Проверьте настройки '
            'в *urls.py*.'
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Проверьте, что POST-запрос `/api/v1/users/activate_invite_code/` без токена '
            'авторизации возвращает ответ со статусом 401.'
        )

    def test_users_activate_invite_code_user(self, user_client, admin, user, django_user_model):
        
        data = {'invite_code': admin.invite_code}
        response = user_client.post('/api/v1/users/activate_invite_code/', data=data)

        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что успешный POST-запрос к `/api/v1/users/activate_invite_code/` '
            ' возвращает ответ со статусом 200.'
        )

        user = django_user_model.objects.filter(
            phone_number=user.phone_number
        ).first()

        assert user.inviter == admin, (
            'Проверьте, что успешный POST-запрос к `/api/v1/users/activate_invite_code/` '
            'связывает пользователей'
        )

    def test_users_self_activate_invite_code_user(self, user_client, user, django_user_model):
        data = {'invite_code': user.invite_code}
        response = user_client.post('/api/v1/users/activate_invite_code/', data=data)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что POST-запрос к `/api/v1/users/activate_invite_code/` '
            'со своим собственным кодом возвращает статус 400'
        )
    
        user = django_user_model.objects.filter(
            phone_number=user.phone_number
        ).first()

        assert not user.inviter , (
            'Проверьте, что POST-запрос к `/api/v1/users/activate_invite_code/` '
            'не влияет на запись в БД'
        )
