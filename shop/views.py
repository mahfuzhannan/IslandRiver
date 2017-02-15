from django.shortcuts import render

# Create your views here.
def shop(request):
    return render(request, "shop.html")

def basket(request):
    return render(request, "basket.html")
