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

from .views import add_new_item, cart, clothes_list, database, delete_item, home, login, checkout

urlpatterns = [
    path("login/", login),
    path("", home, name="home"),
    path("clothes_list/", clothes_list),
    path("database/", database, name="database"),
    path("add_new_item/", add_new_item),
    path("delete_item/<int:item_id>/", delete_item),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
