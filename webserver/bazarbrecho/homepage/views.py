from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .models import *
from .utils import cartData, cookieCart, guestOrder
from .forms import ProductImageForm
from products.models import ProductEntry
import requests
import json
import datetime


"""
Each function here is a "Route" response to be requested by urls.py
The database interaction is defined on each method, given through 'render()' along with the URL 
"""
PRODUCTS_URL = "http://127.0.0.1:8000/products/"


def login(request):
    return render(request, "user_login.html")


def get_products(item_id=None):
    if item_id:
        return requests.get(f'{PRODUCTS_URL}item/{item_id}').json()
    else:
        return requests.get(PRODUCTS_URL).json()


def home(request):
    """
    Returns: a dict with all items from database, the media URL to be used as reference to webpage elements
    """
    all_items = get_products()
    data = cartData(request)
    cartItems = data["cartItems"]
    return render(
        request,
        "homepage.html",
        {
            "all_items": all_items,
            "media_url": settings.MEDIA_URL,
            "cartItems": cartItems,
        },
    )


def detail_product(request, item_id):
    product = get_products(item_id=item_id)
    data = cartData(request)
    cartItems = data["cartItems"]
    return render(
        request,
        "product_detail.html",
        {"media_url": settings.MEDIA_URL, "selected_item": product, "cartItems": cartItems},
    )


def product_image_view(request):
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ProductImageForm()
    return render(request, 'data_upload.html', {'form': form})


def success(request):
    return render(request, 'upload_success.html')


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
    # product = requests.get(f'{PRODUCTS_URL}/item/{item_id}').json() <== TODO change to this
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
