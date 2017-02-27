from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.http import HttpResponse


from app.models import Item, User, Address
from .forms import SignupForm, LoginForm


# Create your views here.


def home_page(request):
    return render(request, 'app/home.html')


def about_page(request):
    return render(request, 'app/about.html')


def signup_page(request):
    form = SignupForm()
    return render(request, 'app/signup.html', {'form': form})


def login_page(request):
    return render(request, 'app/login.html')


def shop(request):
    return render(request, 'app/shop.html')


def basket(request):
    return render(request, 'app/basket.html')


def get_items(request):
    items = Item.objects.all()
    return HttpResponse(serializers.serialize('json', items), content_type='application/json')


def signup_user(request):
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

                return render(request, 'app/shop.html')

    context = {'form': form, 'error': error}
    return render(request, 'app/signup.html', context)


def login_user(request):
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

    context = {'form': form, 'error': error}
    return render(request, 'app/login.html', context)