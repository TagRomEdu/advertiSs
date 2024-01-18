from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


NULLABLE = {'blank': True, 'null': True}


class UserManager(BaseUserManager):
    """
    функция создания пользователя — в нее мы передаем обязательные поля
    """
    def create_user(self, email, first_name, last_name, role='user',
                    phone=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name,
                         phone=None, password=None):
        """
        функция для создания суперпользователя —
        это можно сделать с помощью команды createsuperuser
        """

        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
            role='admin'
        )

        user.save(using=self._db)
        return user


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'User'),
        (ADMIN, 'Admin'),
    ]

    username = None

    email = models.EmailField(unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    phone = models.CharField(_("phone"), max_length=15, **NULLABLE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,
                            default='user')
    image = models.ImageField(_("avatar"), **NULLABLE, upload_to='media/')

    USERNAME_FIELD = 'email'
    # Поля, которые будут вызываться при создании
    # через команду createsuperuser и create_user
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'image']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
