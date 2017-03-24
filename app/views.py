from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.db import transaction
from rest_framework import viewsets, generics
from rest_framework import filters
from django.core.mail import send_mail
import simplejson

from app.serializers import UserSerializer, CatalogSerializer, ProductSerializer, CatalogCategorySerializer, \
    BasketSerializer, BasketProductSerializer, OrderSerializer, OrderProductSerializer
from app.models import User, Address, Basket, BasketProduct, Catalog, Product, CatalogCategory, Order, OrderProduct
from app.permissions import RestApiPermissions
from app.forms import SignupForm, LoginForm


##############################################################
# Home Page
##############################################################
def home(request):
    context = {'logged_in': request.user.is_authenticated}
    return render(request, 'app/home.html', context)


##############################################################
# About Page
##############################################################
def about(request):
    context = {'logged_in': request.user.is_authenticated}
    return render(request, 'app/about.html', context)


##############################################################
# View Shop
##############################################################
def shop(request, *args):
    if request.user.is_authenticated:
        context = {'logged_in': True}
        return render(request, 'app/shop.html', context)
    else:
        return redirect('login')


def shop_product(request, catalog_slug, product_slug):
    if request.user.is_authenticated:
        product = Product.objects.get(category__catalog__slug=catalog_slug, slug=product_slug)
        context = {'logged_in': True, 'product': product}
        return render(request, 'app/product.html', context)
    else:
        return redirect('login')


##############################################################
# View basket
##############################################################
def basket_view(request):
    if request.user.is_authenticated:
        context = {'logged_in': True}
        return render(request, 'app/basket.html', context)
    else:
        return redirect('login')


##############################################################
# View user account
##############################################################
def account_view(request):
    if request.user.is_authenticated:
        context = {'logged_in': True}
        return render(request, 'app/account.html', context)
    else:
        return redirect('login')


##############################################################
# Signup User
##############################################################
def signup_user(request):
    if request.user.is_authenticated:
        # redirect to shop
        return redirect('/shop/men/')
    else:
        error = None
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone = form.cleaned_data['phone']
                password = form.cleaned_data['password']
                password_confirm = form.cleaned_data['password_confirm']
                if not User.objects.filter(email=email).exists():
                    if password == password_confirm:
                        # create user
                        user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name,
                                                        phone=phone, password=password)
                        house = form.cleaned_data['house']
                        line1 = form.cleaned_data['line1']
                        postcode = form.cleaned_data['postcode']
                        # create associated address
                        Address.objects.create(house=house, line1=line1, postcode=postcode, user=user)
                        # create associated basket
                        Basket.objects.create(user=user)
                        # redirect to shop
                        login(request, user)
                        return redirect('/shop/men/')
                    else:
                        error = 'Passwords do not match.'
                else:
                    error = 'Email address is already in use.'
            else:
                error = 'Form details are invalid.'
        else:
            form = SignupForm()
        context = {'form': form, 'error': error, 'logged_in': False}
        return render(request, 'app/signup.html', context)


##############################################################
# Login User
##############################################################
def login_user(request):
    if request.user.is_authenticated:
        # redirect to shop
        return redirect('/shop/men')
    else:
        error = None
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                # check is email exists
                if User.objects.filter(email=email).exists():
                    user = authenticate(username=email, password=password)
                    # if user not null login
                    if user is not None:
                        login(request, user)
                        return redirect('/shop/men/')
                    else:
                        error = 'Email or password is incorrect'
                else:
                    error = 'Email does not exist'
            else:
                error = 'Form details are invalid.'
        else:
            form = LoginForm()
        context = {'form': form, 'error': error, 'logged_in': False}
        return render(request, 'app/login.html', context)


##############################################################
# Logout User
##############################################################
def logout_user(request):
    logout(request)
    return redirect('home')


##############################################################
# Handle Basket add/remove/delete
##############################################################
def baskets(request):
    message = None
    error = None
    if request.method == 'PUT':
        dict = simplejson.JSONDecoder().decode(request.body)
        # adding from basket
        if 'add' in dict:
            dict = dict['add']
            if 'basket_product_id' in dict:
                basket_product_id = dict['basket_product_id']
                product_name = dict['product_name']
                try:
                    basket_product = BasketProduct.objects.get(id=basket_product_id)
                    basket_product.quantity += 1
                    basket_product.save()
                    message = str(basket_product.quantity) + ' ' + product_name + '\'s are in your basket.'
                except BasketProduct.DoesNotExist:
                    error = 'Something went wrong adding ' + product_name + '.'
            # adding from shop
            elif 'product_id' in dict:
                try:
                    basket = Basket.objects.get(user=request.user)
                    try:
                        product_id = dict['product_id']
                        product = Product.objects.get(id=product_id)
                        try:
                            basket_product = BasketProduct.objects.get(basket=basket, product=product)
                            basket_product.quantity += 1
                            basket_product.save()
                            message = str(basket_product.quantity) + ' ' + product.name + '\'s are in your basket.'
                        except BasketProduct.DoesNotExist:
                            BasketProduct.objects.create(basket=basket, product=product)
                            message = product.name + ' has been added to your basket.'
                    except Product.DoesNotExist:
                        error = 'Product does not exist.'
                except Basket.DoesNotExist:
                    error = 'User does not have a basket.'
            else:
                error = 'Something went wrong.'
        elif 'remove' in dict:
            basket_product_id = dict['remove']['basket_product_id']
            product_name = dict['remove']['product_name']
            try:
                basket_product = BasketProduct.objects.get(id=basket_product_id)
                basket_product.quantity -= 1
                basket_product.save()
                if basket_product.quantity == 0:
                    basket_product.delete()
                    message = product_name + ' has been completely removed from your basket.'
                else:
                    if basket_product.quantity > 1:
                        message = str(basket_product.quantity) + ' ' + product_name + '\'s are in your basket.'
                    else:
                        message = str(basket_product.quantity) + ' ' + product_name + ' is in your basket.'
            except BasketProduct.DoesNotExist:
                error = 'User does not have a basket.'
    elif request.method == 'DELETE':
        basket_product_id = request.GET.get('basket_product_id')
        product_name = request.GET.get('product_name')
        try:
            basket_product = BasketProduct.objects.get(id=basket_product_id)
            basket_product.delete()
            message = product_name + ' has been completely removed from your basket.'
        except BasketProduct.DoesNotExist:
            error = 'Product could not be removed from your basket.'
    if error:
        return HttpResponseServerError({'error': error}, {'content_type': 'application/json'})
    else:
        return JsonResponse({'message': message})


##############################################################
# Order Summary
##############################################################
def order_summary_view(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.latest('date')
            order_products = OrderProduct.objects.filter(order=order)
            order.total = 0
            # calculate total and prices of order items
            for order_product in order_products:
                order_product.price = order_product.quantity * order_product.product.price
                order.total += order_product.price
            context = {'logged_in': True, 'order': order, 'order_products': list(order_products)}
            return render(request, 'app/order.html', context)
        except Order.DoesNotExist:
            return HttpResponseServerError({'error': 'Failed to get order'}, {'content_type': 'application/json'})
    else:
        return redirect('login')


##############################################################
# Checkout
##############################################################
@transaction.atomic
def checkout(request):
    try:
        # Create order
        order = Order.objects.create(user=request.user)
        basket = Basket.objects.get(user=request.user)
        basket_products = BasketProduct.objects.filter(basket=basket)
        for basket_product in basket_products:
            OrderProduct.objects.create(product=basket_product.product, order=order, quantity=basket_product.quantity)
            basket_product.delete()
        message = 'Your order ' + str(order.id) + ' has been confirmed. An email has been sent to ' + \
                  request.user.email + '.\nPlease wait while we redirect you to your order summary...'
        return JsonResponse({'message': message, 'order_id': order.id, 'next': '/orders/summary/'})
    except:
        return HttpResponseServerError({'error': 'Checkout failed'}, {'content_type': 'application/json'})


##############################################################
# Basket Product list view
##############################################################
class BasketProductList(generics.ListAPIView):
    queryset = BasketProduct.objects.all()
    serializer_class = BasketProductSerializer
    permission_classes = (RestApiPermissions,)

    def get_queryset(self):
        user = self.request.user
        return BasketProduct.objects.filter(basket__user__id=user.id)


##############################################################
# REST Framework views (READ ONLY)
##############################################################
class RestApiUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (RestApiPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'email', 'first_name', 'last_name', 'phone')


class RestApiCatalogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    permission_classes = (RestApiPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'name', 'slug', 'description', 'pub_date')


class RestApiProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (RestApiPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'category', 'name', 'slug', 'description', 'manufacturer', 'price',
                     'category__id', 'category__name', 'category__slug',
                     'category__catalog__name', 'category__catalog__slug')


class RestApiCatalogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CatalogCategory.objects.all()
    serializer_class = CatalogCategorySerializer
    permission_classes = (RestApiPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'catalog', 'parent', 'name', 'slug', 'description',
                     'catalog__id', 'catalog__name', 'catalog__slug',)


class RestApiBasketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (RestApiPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'user',
                     'user__id', 'user__email', 'user__first_name', 'user__last_name', 'user__phone')


class RestApiBasketProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BasketProduct.objects.all()
    serializer_class = BasketProductSerializer
    permission_classes = (RestApiPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'basket', 'product', 'quantity',
                     'basket__id', 'basket__user__id', 'basket__user__email',
                     'product__id', 'product__name', 'product__slug', 'product__description',)


class RestApiOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (RestApiPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'user', 'date',
                     'user__id', 'user__email', 'user__first_name', 'user__last_name', 'user__phone')


class RestApiOrderProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    permission_classes = (RestApiPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'product', 'date', 'order',
                     'product__id', 'product__name', 'product__slug', 'product__description',
                     'order__id', 'o    rder__user__id')
