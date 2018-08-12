from django.db import models


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=True, max_length=50)
    title = models.CharField(max_length=50)
    mark = models.CharField(max_length=50)
    price = models.CharField(null=True, blank=True, max_length=50)  # храню в char field т.к. кроме как выводить с ней ничего делать не надо
    phone_number = models.CharField(max_length=17)
    email = models.CharField(max_length=75)

    def __str__(self):
        return str(self.id) + '_' + str(self.title)
