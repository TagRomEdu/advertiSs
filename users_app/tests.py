from django.db import connection
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users_app.models import User


class UsersTestCase(APITestCase):

    def setUp(self):
        """
        Метод для установки тестовых данных.
        """
        self.client = APIClient()

        # Создание тестового аккаунта
        self.user = User.objects.create(
            email='test@test.ru',
            first_name="R",
            last_name="T",
            password="Aa12345!"
        )

        # Аутентификация тестового аккаунта
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        """
        Метод cброса тестовых данных.
        """

        # Удаляет всех пользователей и привычки
        User.objects.all().delete()
        super().tearDown()

        # Подключение к тесовой базе данных
        with connection.cursor() as cursor:
            # Сброс идентификаторов пользователей и привычек
            cursor.execute("""
                SELECT setval(pg_get_serial_sequence(
                           '"users_app_user"','id'), 1, false);
                SELECT setval(pg_get_serial_sequence(
                           '"market_app_advertisement"','id'), 1, false);
                SELECT setval(pg_get_serial_sequence(
                           '"market_app_review"','id'), 1, false);
            """)

    def test_get_users_list(self):
        """
        Тест для получения списка пользователей.
        """

        response = self.client.get(
            reverse('users_app:users-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_users_retrieve(self):
        """
        Тест для получения существующего пользователя.
        """

        response = self.client.get(
            reverse('users_app:users-detail', kwargs={'id': self.user.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_users_create(self):
        """
        Тестирование создания пользователя (валидными данными).
        """
        data = {
            "email": "k@sster.ru",
            "first_name": "R",
            "last_name": "T",
            "password": "Aa12345!"
            }

        response = self.client.post(
            reverse('users_app:users-list'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            User.objects.filter(email=data["email"]).exists()
        )

    def test_invalid_users_create(self):
        """
        Тестирование создания пользователя (невалидными данными).
        """

        data = {
            "email": "k@sster",
            "first_name": "R",
            "last_name": "T",
            "password": "Aa12345!"
            }

        response = self.client.post(
            reverse('users_app:users-list'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_users_update(self):
        """
        Тестирование обновления пользователя (валидными данными).
        """

        data = {
            "first_name": "Ro",
            "last_name": "Ta"
        }

        response = self.client.put(
            reverse('users_app:users-detail', kwargs={'id': self.user.pk}),
            data=data
        )
        wished_answer = {
            'email': 'test@test.ru',
            'first_name': 'Ro',
            'id': 1,
            'image': None,
            'last_name': 'Ta',
            'phone': None
            }

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            wished_answer
        )

    def test_invalid_users_update(self):
        """
        Тестирование обновления пользователя (невалидными данными).
        """

        data = {
            'first_name': "",
            "last_name": ""
        }

        response = self.client.put(
            reverse('users_app:users-detail', kwargs={'id': self.user.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_users_patch(self):
        """
        Тестирование частичного обновления пользователя
        (валидными данными).
        """

        data = {
            "first_name": "Ro"
        }

        response = self.client.patch(
            reverse('users_app:users-detail', kwargs={'id': self.user.pk}),
            data=data
        )

        wished_answer = {
            'email': 'test@test.ru',
            'first_name': 'Ro',
            'id': 1,
            'image': None,
            'last_name': 'T',
            'phone': None
            }

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            wished_answer
        )

    def test_invalid_users_patch(self):
        """
        Тестирование частичного обновления пользователя
        (невалидными данными).
        """

        data = {
            "first_name": ""
        }

        response = self.client.patch(
            reverse('users_app:users-detail', kwargs={'id': self.user.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_users_delete(self):
        """
        Тестирование удаления пользователя.
        """

        response = self.client.delete(
            reverse('users_app:users-detail', kwargs={'id': self.user.pk}),
            data={'current_password': self.user.password}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
