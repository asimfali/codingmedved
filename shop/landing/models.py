from django.db import models


class Subscriber(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    email = models.EmailField()

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

    def __str__(self):
        return f'{self.name} {self.email}'
