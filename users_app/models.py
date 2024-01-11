from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _


NULLABLE = {'blank': True, 'null': True}


class CustomUserManager(UserManager):

    def create_superuser(self, email, first_name, last_name,
                         phone=None, password=None):

        user = super().create_superuser(
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
    phone = models.IntegerField(_("phone"), **NULLABLE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    image = models.ImageField(_("avatar"), **NULLABLE, upload_to='media/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    objects = CustomUserManager()

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
