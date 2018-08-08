from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    mark = models.CharField(max_length=50)
    price = models.CharField(null=True, blank=True, max_length=50)  # храню в char field т.к. кроме как выводить с ней ничего делать не надо
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Формат: '+999999999'. Допускается меньше 15 цифр")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.CharField(max_length=75)

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.id) + '_' + str(self.title)
