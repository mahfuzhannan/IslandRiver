from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from app.models import Item, User, Address
import xml.etree.ElementTree

from .forms import SignupForm, LoginForm


# Create your views here.


def home_page(request):
    return render(request, "app/home.html")


def about_page(request):
    return render(request, "app/about.html")


def signup_page(request):
    form = SignupForm()
    return render(request, "app/signup.html", {'form': form})


def login_page(request):
    return render(request, "app/login.html")


def shop(request):
    return render(request, "app/shop.html")


def basket(request):
    return render(request, "app/basket.html")


def setup_shop(request):
    e = xml.etree.ElementTree.parse('movies.xml').getroot()

    for element in e.findall('programme'):
        print (element[0].text, element[1].text)
        if Item.objects.create(name=element[0].text, desc=element[2].text, img=element[1].text, price=10, quantity=100):
            print ("added to database")
        else:
            print ('not added to database')

    return render(request, "app/shop.html")


def get_items(request):
    items = Item.objects.all()
    return HttpResponse(serializers.serialize('json', items), content_type='application/json')


def signup(request):
    form = SignupForm(request.POST)

    if form.is_valid():
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['firstname']
        last_name = form.cleaned_data['lastname']
        phone = form.cleaned_data['phone']
        password = form.cleaned_data['password']
        password_confirm = form.cleaned_data['password_confirm']

        if password != password_confirm:
            return render(request, 'app/signup.html', {'form': form, 'error': 'Passwords do not match'})
        else:
            user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, phone=phone, password=password)

            house = form.cleaned_data['house']
            line1 = form.cleaned_data['line1']
            postcode = form.cleaned_data['postcode']
            Address.objects.create(house=house, line1=line1, postcode=postcode, user=user)

            return render(request, 'app/shop.html')
