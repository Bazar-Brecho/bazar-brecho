from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .utils import cart_data, cookie_cart, guest_order
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
        return requests.get(f"{PRODUCTS_URL}item/{item_id}").json()
    else:
        return requests.get(PRODUCTS_URL).json()


def home(request):
    """
    Returns: a dict with all items from database, the media URL to be used as reference to webpage elements
    """
    all_items = get_products()
    data = cart_data(request)
    cart_items = data["cart_items"]
    return render(
        request,
        "homepage.html",
        {
            "all_items": all_items,
            "media_url": settings.MEDIA_URL,
            "cart_items": cart_items,
        },
    )


def detail_product(request, item_id):
    product = get_products(item_id=item_id)
    data = cart_data(request)
    cart_items = data["cart_items"]
    return render(
        request,
        "product_detail.html",
        {
            "media_url": settings.MEDIA_URL,
            "selected_item": product,
            "cart_items": cart_items,
        },
    )


def product_image_view(request):
    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success")
    else:
        form = ProductImageForm()
    return render(request, "data_upload.html", {"form": form})


def success(request):
    return render(request, "upload_success.html")


def cart(request):

    data = cart_data(request)
    cart_items = data["cart_items"]
    order = data["order"]
    items = data["items"]

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "order": order,
            "cart_items": cart_items,
            "media_url": settings.MEDIA_URL,
        },
    )


def checkout(request):
    data = cart_data(request)

    cart_items = data["cart_items"]
    order = data["order"]
    items = data["items"]

    context = {
        "items": items,
        "order": order,
        "cart_items": cart_items,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "checkout.html", context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data["product_id"]
    action = data["action"]
    print("Action:", action)
    print("Product:", product_id)

    customer = request.user.customer
    product = ProductEntry.objects.get(id=product_id)
    # product = requests.get(f'{PRODUCTS_URL}/item/{item_id}').json() <== TODO change to this
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = Order_item.objects.get_or_create(order=order, product=product)

    if action == "add":
        order_item.quantity = order_item.quantity + 1
    elif action == "remove":
        order_item.quantity = order_item.quantity - 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse("Item was added", safe=False)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guest_order(request, data)

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
