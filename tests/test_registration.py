from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestUserRegistration:
    url_signup = '/api/v1/auth/signup/'
    url_token = '/api/v1/auth/token/'

    def test_nodata_signup(self, client):
        response = client.post(self.url_signup)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.url_signup}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос, отправленный на эндпоинт `{self.url_signup}`, '
            'не содержит необходимых данных, должен вернуться ответ со '
            'статусом 400.'
        )

    def test_invalid_data_signup(self, client, django_user_model):
        invalid_data = {
            'invalid_phone_number': '1234',
        }
        users_count = django_user_model.objects.count()

        response = client.post(self.url_signup, data=invalid_data)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос к эндпоинту `{self.url_signup}` содержит '
            'некорректные данные, должен вернуться ответ со статусом 400.'
        )
        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{self.url_signup}` с '
            'некорректными данными не создаёт нового пользователя.'
        )

        response_json = response.json()
        invalid_fields = ['phone_number']
        for field in invalid_fields:
            assert (field in response_json
                    and isinstance(response_json.get(field), list)), (
                f'Если в  POST-запросе к `{self.url_signup}` переданы '
                'некорректные данные, в ответе должна возвращаться информация '
                'о неправильно заполненных полях.'
            )

    def test_valid_data_user_signup(self, client, django_user_model):
        valid_data = {
            'phone_number': '+79161109450',
        }

        response = client.post(self.url_signup, data=valid_data)
        assert response.status_code == HTTPStatus.OK, (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{self.url_signup}`, должен вернуть ответ со статусом 200.'
        )
        assert response.json() == valid_data, (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{self.url_signup}`, должен вернуть ответ, содержащий '
            'информацию о  `phone_number` созданного пользователя.'
        )

        new_user = django_user_model.objects.filter(
            phone_number=valid_data['phone_number']
        )

        assert new_user.exists(), (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{self.url_signup}`, должен создать нового пользователя.'
        )
        
        assert new_user.first().invite_code, (
            f'При создании нового пользователя через `{self.url_signup}`'
            'должен прописываться код-приглашение'
        )

        assert new_user.first().confirmation_code, (
            f'При создании нового пользователя через `{self.url_signup}`'
            'должен прописываться код активации'
        )


    def test_obtain_jwt_token_invalid_data(self, client, django_user_model):
        response = client.post(self.url_token)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.url_token}` не найдена. Проверьте настройки в '
            '*urls.py*.'
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что POST-запрос без данных, отправленный на эндпоинт '
            f'`{self.url_token}`, возвращает ответ со статусом 400.'
        )

        invalid_data = {
            'confirmation_code': 12345
        }

        response = client.post(self.url_token, data=invalid_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что POST-запрос, отправленный на эндпоинт '
            f'`{self.url_token}`и не содержащий информации о `phone_number`, '
            'возвращает ответ со статусом 400.'
        )

        invalid_data = {
            'phone_number': '+79161111112',
            'confirmation_code': '1234'
        }
        response = client.post(self.url_token, data=invalid_data)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            'Проверьте, что POST-запрос с несуществующим `phone_number`, '
            f'отправленный на эндпоинт `{self.url_token}`, возвращает ответ '
            'со статусом 404.'
        )

        valid_signup_data = {
            'phone_number': '+79161111111',
        }

        response = client.post(self.url_signup, data=valid_signup_data)
        new_user = django_user_model.objects.filter(
            phone_number=valid_signup_data['phone_number']
        )

        valid_data = {
            'phone_number': '+79161111111',
            'confirmation_code': new_user.first().confirmation_code
        }


        response = client.post(self.url_token, data=valid_data)
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что POST-запрос с валидными данными, '
            f'отправленный на эндпоинт `{self.url_token}`, возвращает ответ '
            'со статусом 200.'
        )

        assert 'Bearer' in response.json(), (
            'Проверьте, что POST-запрос с валидными данными, '
            f'отправленный на эндпоинт `{self.url_token}`, возвращает токен'
        )
