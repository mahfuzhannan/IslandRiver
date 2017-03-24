from rest_framework import serializers
from app.models import User, Catalog, Product, CatalogCategory, Basket, BasketProduct, Order, OrderProduct


# class ItemSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = Item
#         fields = ('name', 'desc', 'img', 'price', 'quantity')
#
#
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone')


class CatalogSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Catalog
        fields = ('id', 'name', 'slug', 'description', 'pub_date')


class CatalogCategorySerializer(serializers.HyperlinkedModelSerializer):
    catalog = CatalogSerializer(read_only=True)

    class Meta:
        model = CatalogCategory
        fields = ('id', 'catalog', 'parent', 'name', 'slug', 'description')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = CatalogCategorySerializer(read_only=True)
    photo = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'slug', 'description', 'photo', 'manufacturer', 'price')


class BasketSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Basket
        fields = ('id', 'user')


class BasketProductSerializer(serializers.HyperlinkedModelSerializer):
    basket = BasketSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = BasketProduct
        fields = ('id', 'basket', 'product', 'quantity')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'date')


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ('id', 'product', 'date', 'order')
