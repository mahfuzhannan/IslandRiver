from __future__ import unicode_literals
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone = phone,
        )
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, password=None):

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone = phone,
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.TextField(max_length=13, blank=True)

    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        # __unicode__ on Python 2g
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin


class Address(models.Model):
    house = models.CharField(max_length=50)
    line1 = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# class Basket(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     items = models.ManyToManyField(Item)
#     total = models.CharField(max_length=50)


class Catalog(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150)
    description = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey('CatalogCategory', related_name='products')
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=150)
    description = models.TextField()
    photo = models.ImageField(upload_to='static/app/images/product_photo', blank=True)
    manufacturer = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return self.name


class CatalogCategory(models.Model):
    catalog = models.ForeignKey('Catalog',related_name='categories')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=150)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.catalog, self.name)


class ProductDetail(models.Model):
    '''
    The ``ProductDetail`` model represents information unique to a
    specific product. This is a generic design that can be used
    to extend the information contained in the ``Product`` model with
    specific, extra details.
    '''
    product = models.ForeignKey('Product', related_name='details')
    attribute = models.ForeignKey('ProductAttribute')
    value = models.CharField(max_length=500)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s: %s - %s' % (self.product, self.attribute, self.value)


class ProductAttribute(models.Model):
    '''
    The "ProductAttribute" model represents a class of feature found
    across a set of products. It does not store any data values
    related to the attribute, but only describes what kind of a
    product feature we are trying to capture. Possible attributes
    include things such as materials, colors, sizes, and many, many
    more.
    '''
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s' % self.name


class Basket(models.Model):
    user = models.OneToOneField(User, null=True)

    def __unicode__(self):
        return u'%s' % self.user


class BasketProductManager(models.Manager):
    def add(self, **kwargs):
        if 'basket_product_id' in kwargs:
            basket_product = self.get(id=kwargs.basket_product_id)
            basket_product.quantity += 1
            basket_product.save()
        elif 'basket' in kwargs and 'product' in kwargs:
            try:
                basket_product = self.get(basket=kwargs.basket, product=kwargs.product)
                self.add(basket_product.id)
            except self.DoesNotExist:
                self.create(basket=kwargs.basket, product=kwargs.product)

    def remove(self, basket_product_id):
        basket_product = self.get(id=basket_product_id)
        if basket_product.quantity == 0:
            self.delete()
        else:
            basket_product.quantity -= 1
            basket_product.save()


class BasketProduct(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_products',
                               related_query_name='basket_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=0, default=1)

    objects = BasketProductManager()

    def __unicode__(self):
        return u'%s: %s - %s' % (self.basket, self.product, self.quantity)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return u':%s' % (self.id)


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s: %s %s (%s)' % (self.id, self.product, self.quantity, self.order)

