"""bazarbrecho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    login,
    home,
    product_image_view,
    cart,
    detail_product,
    checkout,
    update_item,
    success,
)


urlpatterns = [
    path("login/", login),
    path("", home, name="home"),
    path("home", home, name="homepage"),
    path("cart/", cart, name="cart"),
    path("detail/<int:item_id>/", detail_product, name="detail"),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path("update_item/", update_item, name="update_item"),
    path("data_upload", product_image_view, name="data_upload"),
    path("success", success, name="success"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
