from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models


# Create your models here.
class ItemCategory(models.Model):
    category = models.CharField(max_length=50)


class Item(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    img = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    # category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)


class Basket(models.Model):
    items = models.ManyToManyField(Item)
    total = models.CharField(max_length=50)
    # user = models.OneToOneField(user)


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(
            email=self.mormalize_email(email)
        )

        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    phone = models.TextField(max_length=13, blank=True)


class Address(models.Model):
    house = models.CharField(max_length=50)
    line1 = models.CharField(max_length=50)
    line2 = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name