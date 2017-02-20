from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from models import Item
import xml.etree.ElementTree

# Create your views here.


def home(request):
    return render(request, "app/home.html")


def about(request):
    return render(request, "app/about.html")


def signup(request):
    return render(request, "app/signup.html")


def login(request):
    return render(request, "app/login.html")


def shop(request):
    return render(request, "app/shop.html")


def basket(request):
    return render(request, "app/basket.html")


def setup_shop(request):
    e = xml.etree.ElementTree.parse('movies.xml').getroot()

    for element in e.findall('programme'):
        print element[0].text, element[1].text
        if Item.objects.create(name=element[0].text, desc=element[2].text, img=element[1].text, price=10, quantity=100):
            print "added to database"
        else:
            print 'not added to database'

    return render(request, "app/shop.html")


def get_items(request):
    items = Item.objects.all()
    return HttpResponse(serializers.serialize('json', items), content_type='application/json')
