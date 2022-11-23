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
    database,
    cart,
    detail_product,
    add_new_item,
    delete_item,
    login,
    checkout,
)


urlpatterns = [
    path("login/", login),
    path("", home, name="home"),
    path("home", home, name="homepage"),
    path("cart/", cart, name="cart"),
    path("detail/<int:item_id>/", detail_product, name="detail"),
    path("database/", database, name="database"),
    path("add_new_item/", add_new_item),
    path("delete_item/<int:item_id>/", delete_item),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
