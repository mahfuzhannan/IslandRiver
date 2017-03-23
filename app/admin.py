from django.contrib import admin
from .models import User, Catalog, Product, CatalogCategory, ProductDetail, ProductAttribute, Basket, BasketProduct

# Register your models here.
admin.site.register(User)
admin.site.register(Catalog)
admin.site.register(Product)
admin.site.register(CatalogCategory)
admin.site.register(ProductDetail)
admin.site.register(ProductAttribute)
admin.site.register(Basket)
admin.site.register(BasketProduct)
