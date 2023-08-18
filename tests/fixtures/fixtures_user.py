import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        phone_number='89161234567',
        email='test@mail.ru',
        username='TestUser',
        first_name='TestFirstName',
        last_name='TestLastName',
    )

@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create_user(
        email='another_user@mail.ru',
        username='AnotherTestUser',
        first_name='AnotherTestFirstName',
        last_name='AnotherTestLastName',
        phone_number='89161234568'
    )


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        username="TestAdmin",
        email='admin@mail.ru',
        first_name='AdminFirstName',
        last_name='AdminLastName',
        phone_number='89161111111',
        is_staff=True,
    )


@pytest.fixture
def token_user(user):
    token = AccessToken.for_user(user)
    return {
        "access": str(token),
    }


@pytest.fixture
def token_admin(admin):
    token = AccessToken.for_user(admin)
    return {
        "access": str(token),
    }


@pytest.fixture
def user_client(token_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_user["access"]}')
    return client

@pytest.fixture
def admin_client(token_admin):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_admin["access"]}')
    return client
