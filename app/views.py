from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def shop(request):
    return render(request, "shop.html")

def basket(request):
    return render(request, "basket.html")
