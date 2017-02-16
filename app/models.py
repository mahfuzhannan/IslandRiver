from __future__ import unicode_literals

from django.db import models


# Create your models here.
class ItemManager(models.Manager):
    def addItem(self, name, desc, price, quantity):
        if name is None or desc is None or price is None or quantity is None:
            return False

        Item.objects.create(name=name, desc=desc, price=price, quantity=quantity);
        return True

    def deleteItem(self, itemId):
        if id is None:
            return False

        return Item.objects.get(_id=itemId).delete()

    def updateItem(self, itemId, **kwargs):
        if itemId is None or not kwargs.get('name') or not kwargs.get('desc') or not kwargs.get('price') \
                or not kwargs.get('quantity'):
            return False

        item = Item.objects.get(_id=itemId)
        return item.update(name=kwargs.get('name'), desc=kwargs.get('desc'), price=kwargs.get('price'),
                           quantity=kwargs.get('quantity'))


class Item(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    items = ItemManager()


class BasketManager(models.Manager):
    def addItem(self, userId, itemId):
        if userId is None or itemId is None:
            return False

        item = Item.objects.get(_id=itemId)
        basket = Basket.objects.get(_id=userId)
        return basket.items.add(item)

    def removeItem(self, userId, itemId):
        if userId is None or itemId is None:
            return False

        item = Item.objects.get(_id=itemId)
        basket = Basket.objects.get(_id=userId)
        return basket.items.remove(item)

    def removeAll(self, userId):
        if userId is None:
            return False

        basket = Basket.objects.get(_id=userId)
        return basket.items.clear()


class Basket(models.Model):
    items = models.ManyToManyField(Item)
    total = models.CharField(max_length=50)
    # user = models.OneToOneField(user)
    baskets = BasketManager()