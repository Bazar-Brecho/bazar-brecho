import datetime
import json

from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .models import ProductEntry, product_entry_example
from .utils import cartData, cookieCart, guestOrder

"""
Each function here is a "Route" response to be requested by urls.py
The database interaction is defined on each method, given through 'render()' along with the URL 
"""


def home(request):
    """
    Returns: a dict with all items from database, the media URL to be used as reference to webpage elements
    """
    all_products = ProductEntry.objects.all()
    return render(
        request,
        "homepage.html",
        {"all_items": all_products, "media_url": settings.MEDIA_URL},
    )


def database(request):
    all_products = ProductEntry.objects.all()
    return render(
        request,
        "database_editor.html",
        {"all_items": all_products, "media_url": settings.MEDIA_URL},
    )


def login(request):
    return render(request, "user_login.html")


def clothes_list(request):
    all_clothes = product_entry_example.objects.all()
    return render(request, "clothes_list.html", {"all_items": all_clothes})


def add_new_item(request):
    """
    Add new item to the database. The class ProductEntry defines an entry for the database.
    """
    new_item = ProductEntry(
        product_name=request.POST["product_name"],
        product_size=request.POST["product_size"],
        product_price=request.POST["product_price"],
        product_image=request.POST["product_image_path"],
    )
    new_item.save()
    return HttpResponseRedirect("/")


def delete_item(request, item_id):
    del_item = ProductEntry.objects.get(id=item_id)
    del_item.delete()
    return HttpResponseRedirect("/")


def cart(request):

    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "cart.html", context)
