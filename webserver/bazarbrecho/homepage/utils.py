import json
from products.models import ProductEntry

def cookie_cart(request):

    try:
        cart = json.loads(request.COOKIES["cart"])
    except:
        cart = {}

    print("Cart from utils file:", cart)
    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0}
    cart_items = order["get_cart_items"]

    for i in cart:
        try:
            cart_items += cart[i]["quantity"]
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
    return {"cart_items": cart_items, "order": order, "items": items}


def cart_data(request):

    cookie_data = cookie_cart(request)
    cart_items = cookie_data["cart_items"]
    order = cookie_data["order"]
    items = cookie_data["items"]

    return {"cart_items": cart_items, "order": order, "items": items}


def guest_order(request, data):

    print("User is not logged in...")

    print("COOKIES from Utils file:", request.COOKIES)
    name = data["form"]["name"]
    email = data["form"]["email"]

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    return customer, order
