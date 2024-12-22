from django.views import View
from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(60 * 15, key_prefix="home")
def index(request):
    return render(request, "home/index.html")
    

def terms(request):
    return render(request, "home/terms.html")