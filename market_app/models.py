from django.db import models
from django.utils.translation import gettext_lazy as _
from config import settings


class Advertisement(models.Model):
    title = models.CharField(_("title"), max_length=150)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    description = models.TextField(_("description"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("date of creation"), auto_now_add=True)
    image = models.ImageField(_("preview of advirtisement"),
                              upload_to='images/')

    class Meta:
        ordering = ('-created_at',)

        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class Review(models.Model):
    text = models.TextField(_("review's text"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    ad = models.ForeignKey(Advertisement,
                           on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("date of creation"), auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
