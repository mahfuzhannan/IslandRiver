from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from app.models import Item, User, Address, Basket
from .forms import SignupForm, LoginForm


# Create your views here.


def home(request):
    context = {'logged_in':request.user.is_authenticated}
    return render(request, 'app/home.html', context)


def about(request):
    context = {'logged_in':request.user.is_authenticated}
    return render(request, 'app/about.html', context)


def shop(request):
    if request.user.is_authenticated:
        context = {'logged_in':True}
        return render(request, 'app/shop.html', context)
    else:
        return redirect('login')


def users(request):
    if request.method == 'GET':
        all_items = User.objects.all()
        return HttpResponse(serializers.serialize('json', all_items), content_type='application/json')
    if request.method == 'POST':
        # create item
        return HttpResponse({'message': 'added user'}, content_type='application/json')
    if request.method == 'PUT':
        # edit item
        return HttpResponse({'message': 'changed user'}, content_type='application/json')
    if request.method == 'DELETE':
        # delete item
        return HttpResponse({'message': 'deleted user'}, content_type='application/json')


def baskets(request):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            item_id = request.POST['item']
            item = Item.objects.get(id=item_id)
            basket = Basket.objects.get(email=request.user.email)
            basket.items.add(item)
            return JsonResponse({'item': item_id})
        if request.method == 'DELETE':
            item_id = request.POST['item']
            item = Item.objects.get(id=item_id)
            basket = Basket.objects.get(email=request.user.email)
            basket.items.remove(item)
            return JsonResponse({'item': item_id})
        if request.method == 'GET':
            user = User.objects.get(email=request.user.email)
            basket = Basket.objects.get(user=request.user)
            context = {'logged_in':True, 'basket': basket}
            return render(request, 'app/basket.html', context)
    else:
        return redirect('login')


def items(request):
    if request.method == 'GET':
        all_items = Item.objects.all()
        return HttpResponse(serializers.serialize('json', all_items), content_type='application/json')
    if request.method == 'POST':
        # create item
        return HttpResponse({'message': 'added item'}, content_type='application/json')
    if request.method == 'PUT':
        # edit item
        return HttpResponse({'message': 'changed item'}, content_type='application/json')
    if request.method == 'DELETE':
        # delete item
        return HttpResponse({'message': 'deleted item'}, content_type='application/json')


def signup_user(request):
    if not request.user.is_authenticated:
        form = SignupForm()
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

                if password != password_confirm:
                    error = 'Passwords do not match'
                else:
                    user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, phone=phone, password=password)
                    house = form.cleaned_data['house']
                    line1 = form.cleaned_data['line1']
                    postcode = form.cleaned_data['postcode']
                    Address.objects.create(house=house, line1=line1, postcode=postcode, user=user)

                    context = {'logged_in':True}
                    return render(request, 'app/shop.html', context)
        context = {'form': form, 'error': error, 'logged_in': False}
        return render(request, 'app/signup.html', context)
    else:
        return redirect('shop')


def login_user(request):
    if not request.user.is_authenticated:
        form = LoginForm()
        error = None
        if request.method == 'POST':
            form = LoginForm(request.POST)

            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                if User.objects.filter(email=email).exists():
                    # login
                    user = authenticate(username=email, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('shop')
                    else:
                        error = 'Email or password is incorrect'
        context = {'form': form, 'error': error, 'logged_in': False}
        return render(request, 'app/login.html', context)
    else:
        return redirect('shop')


def logout_user(request):
    logout(request)
    return redirect('home')