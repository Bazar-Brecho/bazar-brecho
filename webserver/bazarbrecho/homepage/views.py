from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import product_entry


def home(request):
    return render(request, "homepage.html")


def login(request):
    return render(request, "user_login.html")


def clothes_list(request):
    all_clothes = product_entry.objects.all()
    return render(request, "clothes_list.html", {"all_items": all_clothes})


def add_item(request):
    new_item = product_entry(content=request.POST["content"])
    new_item.save()
    return HttpResponseRedirect("/clothes_list/")


def delete_item(request, item_id):
    del_item = product_entry.objects.get(id=item_id)
    del_item.delete()
    return HttpResponseRedirect("/clothes_list/")

def cart(request):
    return render(request, "cart.html")    
