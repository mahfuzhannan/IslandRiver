from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from rest_framework import viewsets, generics
from rest_framework.decorators import detail_route
from rest_framework import filters
import xml.etree.ElementTree
import simplejson

from app.serializers import UserSerializer, CatalogSerializer, ProductSerializer, CatalogCategorySerializer, \
    BasketSerializer, BasketProductSerializer
from .forms import SignupForm, LoginForm
from app.models import User, Address, Basket, BasketProduct, Catalog, Product, CatalogCategory
from app.permissions import RestApiPermissions


##############################################################
# Static views
##############################################################
def home(request):
    context = {'logged_in':request.user.is_authenticated}
    return render(request, 'app/home.html', context)


def about(request):
    context = {'logged_in':request.user.is_authenticated}
    return render(request, 'app/about.html', context)


def shop(request, *args, **kwargs):
    if request.user.is_authenticated:
        context = {'logged_in': True}
        return render(request, 'app/shop.html', context)
    else:
        return redirect('login')


def basket_view(request):
    if request.user.is_authenticated:
        context = {'logged_in': True}
        return render(request, 'app/basket.html', context)
    else:
        return redirect('login')


def account_view(request):
    if request.user.is_authenticated:
        context = {'logged_in':True}
        return render(request, 'app/account.html', context)
    else:
        return redirect('login')


##############################################################
# Auth views
##############################################################
def signup_user(request):
    if request.user.is_authenticated:
        # redirect to shop
        return redirect('shop')
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
                        user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, phone=phone, password=password)
                        house = form.cleaned_data['house']
                        line1 = form.cleaned_data['line1']
                        postcode = form.cleaned_data['postcode']
                        # create associated address
                        Address.objects.create(house=house, line1=line1, postcode=postcode, user=user)
                        # create associated basket
                        Basket.objects.create(user=user)
                        # redirect to shop
                        context = {'logged_in':True}
                        return render(request, 'app/shop.html', context)
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


def login_user(request):
    if request.user.is_authenticated:
        # redirect to shop
        return redirect('shop')
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
                        return redirect('shop')
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


def logout_user(request):
    logout(request)
    return redirect('home')


##############################################################
# Web APIs
##############################################################
def user(request):
    if request.user.is_authenticated:
        return JsonResponse(request.user)
    else:
        return JsonResponse({'error': 'User not logged in.'})


def basket_products(request):
    if request.user.is_authenticated:
        basket = Basket.objects.get(user=request.user)
        basket_products = BasketProduct.objects.filter(basket=basket)
        data = serializers.serialize('json', basket_products)
        return HttpResponse(data, 'application/json')
    else:
        return JsonResponse({'error': 'User not logged in.'})


def baskets(request):
    message = None
    error = None
    if request.method == 'PUT':
        dict = simplejson.JSONDecoder().decode(request.body)
        # adding from basket
        if 'add' in dict:
            basket_product = None
            dict = dict['add']
            if 'basket_product_id' in dict:
                basket_product_id = dict['add']['basket_product_id']
                product_name = dict['add']['product_name']
                try:
                    basket_product = BasketProduct.objects.get(basket_product_id)
                    basket_product.quantity += 1
                    basket_product.save()
                    message = 'Another ' + product_name + ' has been added to your basket.'
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
                            message = 'Another ' + product.name + ' has been added to your basket.'
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
            try:
                basket_product_id = dict['remove']['basket_product_id']
                product_name = dict['remove']['product_name']
                basket_product = BasketProduct.objects.get(basket_product_id)
                basket_product.quantity -= 1
                basket_product.save()
                message = 'One ' + product_name + ' has been removed from your basket.'
            except BasketProduct.DoesNotExist:
                BasketProduct.objects.get(basket_product_id)
    elif request.method == 'DELETE':
        basket_product_id = request.GET.get('basket_product_id')
        product_name = request.GET.get('product_name')
        try:
            basket_product = BasketProduct.objects.get(id=basket_product_id)
            basket_product.delete()
            message = product_name + ' has been removed from your basket.'
        except BasketProduct.DoesNotExist:
            error = 'Product could not be removed from your basket.'
    if error:
        return HttpResponseServerError({'error': error}, {'content_type': 'application/json'})
    else:
        return JsonResponse({'message': message})


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


##############################################################
# Setup views
##############################################################
def setup_shop(request):
    e = xml.etree.ElementTree.parse('movies.xml').getroot()
    for element in e.findall('programme'):
        print element[0].text, element[1].text
        if Product.objects.create(name=element[0].text, desc=element[2].text, img=element[1].text, price=10, quantity=100):
            print "added to database"
        else:
            print 'not added to database'

    return redirect('shop')