from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .models import *
from .utils import cartData, cookieCart, guestOrder
import json
import datetime


"""
Each function here is a "Route" response to be requested by urls.py
The database interaction is defined on each method, given through 'render()' along with the URL 
"""


def home(request):
    """
    Returns: a dict with all items from database, the media URL to be used as reference to webpage elements
    """
    all_products = ProductEntry.objects.all()
    data = cartData(request)
    cartItems = data["cartItems"]
    return render(
        request,
        "homepage.html",
        {
            "all_items": all_products,
            "media_url": settings.MEDIA_URL,
            "cartItems": cartItems,
        },
    )


def cart(request):

    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "order": order,
            "cartItems": cartItems,
            "media_url": settings.MEDIA_URL,
        },
    )


def detail_product(request, item_id):
    product = ProductEntry.objects.get(id=item_id)
    data = cartData(request)
    cartItems = data["cartItems"]
    return render(
        request,
        "product_detail.html",
        {"media_url": settings.MEDIA_URL, "product": product, "cartItems": cartItems},
    )


def login(request):
    return render(request, "user_login.html")


def database(request):
    all_products = ProductEntry.objects.all()
    data = cartData(request)
    cartItems = data["cartItems"]
    return render(
        request,
        "database_editor.html",
        {
            "all_items": all_products,
            "media_url": settings.MEDIA_URL,
            "cartItems": cartItems,
        },
    )


def add_new_item(request):
    """
    Add new item to the database. The class ProductEntry defines an entry for the database.
    """
    new_item = ProductEntry(
        product_name=request.POST["product_name"],
        product_size=request.POST["product_size"],
        product_price=request.POST["product_price"],
        product_description=request.POST["product_description"],
        product_image=request.POST["product_image_path"],
    )
    new_item.save()
    return HttpResponseRedirect("/")


def delete_item(request, item_id):
    del_item = ProductEntry.objects.get(id=item_id)
    del_item.delete()
    return HttpResponseRedirect("/")


def checkout(request):
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    print("Action:", action)
    print("Product:", productId)

    customer = request.user.customer
    product = ProductEntry.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
        )

    return JsonResponse("Payment Complete", safe=False)
