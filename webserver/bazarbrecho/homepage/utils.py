import json

from .models import *


def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES["cart"])
    except:
        cart = {}

    print("Cart from utils file:", cart)
    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0}
    cartItems = order["get_cart_items"]

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            product = ProductEntry.objects.get(id=i)
            total = product.product_price * cart[i]["quantity"]
            order["get_cart_total"] += total
            order["get_cart_items"] += cart[i]["quantity"]
            item = {
                "product": {
                    "id": product.id,
                    "product_name": product.product_name,
                    "product_price": product.product_price,
                    "product_image": product.product_image,
                },
                "quantity": cart[i]["quantity"],
                "get_total": total,
            }
            items.append(item)
        except:
            pass
    return {"cartItems": cartItems, "order": order, "items": items}



def cartData(request):

    cookieData = cookieCart(request)
    cartItems = cookieData["cartItems"]
    order = cookieData["order"]
    items = cookieData["items"]

    return {"cartItems": cartItems, "order": order, "items": items}



def guestOrder(request, data):

    print("User is not logged in...")

    print("COOKIES from Utils file:", request.COOKIES)
    name = data["form"]["name"]
    email = data["form"]["email"]

    cookieData = cookieCart(request)
    items = cookieData["items"]

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = ProductEntry.objects.get(id=item["product"]["id"])

        orderItem = OrderItem.objects.create(
            product=product, order=order, quantity=item["quantity"]
        )

    return customer, order
