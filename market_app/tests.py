from django.db import connection
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from market_app.models import Advertisement, Review
from users_app.models import User


class MarketTestCase(APITestCase):

    def setUp(self):
        """
        Метод для установки тестовых данных.
        """
        self.client = APIClient()

        # Создание тестовых аккаунтов
        self.user = User.objects.create(
            email='test@test.ru',
            first_name="R",
            last_name="T",
            password="Aa12345!"
        )

        self.another_user = User.objects.create(
            email='testik@test.ru',
            first_name="T",
            last_name="R",
            password="Bb12345!"
        )

        # Аутентификация тестового аккаунта
        self.client.force_authenticate(user=self.user)

        # Создание тестовых объявления и отзыва
        self.adv = Advertisement.objects.create(
            author=self.user,
            title="test",
            price="300",
            description="test adv"
        )

        self.another_adv = Advertisement.objects.create(
            author=self.another_user,
            title="test 2",
            price="3000",
            description="test adv 2"
        )

        self.review = Review.objects.create(
            author=self.user,
            ad=self.adv,
            text="test review"
        )

    def tearDown(self):
        """
        Метод cброса тестовых данных.
        """

        # Удаляет всех пользователей и привычки
        User.objects.all().delete()
        Advertisement.objects.all().delete()
        Review.objects.all().delete()
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

    def test_get_adv_list(self):
        """
        Тест для получения списка объявлений.
        """

        response = self.client.get(
            reverse('market_app:ads-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_adv_retrieve(self):
        """
        Тест для получения существующего объявления.
        """

        response = self.client.get(
            reverse('market_app:ads-detail', kwargs={'pk': self.adv.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_another_adv_retrieve(self):
        """
        Тест для получения существующего объявления другого пользователя.
        """

        response = self.client.get(
            reverse('market_app:ads-detail',
                    kwargs={'pk': self.another_adv.pk}
                    ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_adv_create(self):
        """
        Тестирование создания объявления пользователем (валидными данными).
        """
        data = {
            "author": self.user.pk,
            "title": "test 4",
            "price": "230",
            "description": "test 4"
            }

        response = self.client.post(
            reverse('market_app:ads-list'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Advertisement.objects.filter(title=data["title"]).exists()
        )

    def test_invalid_adv_create(self):
        """
        Тестирование создания объявления пользователем (невалидными данными).
        """

        data = {
            "author": self.user.pk,
            "title": "test 5",
            "description": "test 5"
            }

        response = self.client.post(
            reverse('market_app:ads-list'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_adv_update(self):
        """
        Тестирование обновления объявления пользователем (валидными данными).
        """

        data = {
            "author": self.user.pk,
            "title": "test 4",
            "price": "230",
            "description": "test 4"
        }

        response = self.client.put(
            reverse('market_app:ads-detail', kwargs={'pk': self.adv.pk}),
            data=data
        )
        wished_answer = {
            'author': 1,
            'created_at':
                self.adv.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'description': 'test 4',
            'id': 1,
            'image': None,
            'price': '230.00',
            'review': ['test review'],
            'review_count': 1,
            'title': 'test 4'
            }

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            wished_answer
        )

    def test_invalid_adv_update(self):
        """
        Тестирование обновления объявления пользователем (невалидными данными).
        """

        data = {
            "author": self.user.pk,
            "title": "test 4",
            "description": "test 4"
        }

        response = self.client.put(
            reverse('market_app:ads-detail', kwargs={'pk': self.adv.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_another_adv_update(self):
        """
        Тестирование обновления объявления другого пользователя.
        """

        data = {
            "author": self.another_user.pk,
            "title": "test 4",
            "price": "230",
            "description": "test 4"
        }

        response = self.client.put(
            reverse('market_app:ads-detail',
                    kwargs={'pk': self.another_adv.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_adv_patch(self):
        """
        Тестирование частичного обновления объявления пользователем
        (валидными данными).
        """

        data = {
            "title": "test 4"
        }

        response = self.client.patch(
            reverse('market_app:ads-detail', kwargs={'pk': self.adv.pk}),
            data=data
        )

        wished_answer = {
            'author': 1,
            'created_at':
                self.adv.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'description': 'test adv',
            'id': 1,
            'image': None,
            'price': '300.00',
            'review': ['test review'],
            'review_count': 1,
            'title': 'test 4'
            }

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            wished_answer
        )

    def test_invalid_adv_patch(self):
        """
        Тестирование частичного обновления объявления пользователем
        (невалидными данными).
        """

        data = {
            "price": "test"
        }

        response = self.client.patch(
            reverse('market_app:ads-detail', kwargs={'pk': self.adv.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_another_adv_patch(self):
        """
        Тестирование частичного обновления объявления другого пользователя.
        """

        data = {
            "title": "test 4"
        }

        response = self.client.put(
            reverse('market_app:ads-detail',
                    kwargs={'pk': self.another_adv.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_adv_delete(self):
        """
        Тестирование удаления объявления пользователем (валидными данными).
        """

        response = self.client.delete(
            reverse('market_app:ads-detail', kwargs={'pk': self.adv.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_another_adv_delete(self):
        """
        Тестирование удаления объявления другого пользователя.
        """

        response = self.client.delete(
            reverse('market_app:ads-detail',
                    kwargs={'pk': self.another_adv.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
