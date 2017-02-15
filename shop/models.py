from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length = 50)
    desc = models.CharField(max_length = 50)
    price = models.CharField(max_length = 50)
    quantity = models.CharField(max_length = 50)

class Basket(models.Model):
    items = models.ManyToManyField(Item)
    total = models.CharField(max_length = 50)
    # user = models.OneToOneField(user)
