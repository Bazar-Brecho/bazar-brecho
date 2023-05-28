from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import *
import json


"""
Each function here is a "Route" response to be requested by urls.py
The database interaction is defined on each method, given through 'render()' along with the URL 
"""


# class MyModelViewSet(viewsets.ModelViewSet):
#     queryset = MyModel.objects.order_by('-creation_date')
#     serializer_class = MyModelSerializer
#     parser_classes = (MultiPartParser, FormParser)
#     permission_classes = [
#         permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)


def get_products(item_id=None):
    if not item_id:
        return ProductSerializer(ProductEntry.objects.all(), many=True)
    if item_id:
        return ProductSerializer(ProductEntry.objects.get(id=item_id))


@api_view(['GET', 'POST'])
def product_list(request):

    if request.method == 'GET':
        products_serializer = get_products()
        return JsonResponse({'products': products_serializer.data})

    if request.method == 'POST':
        print(request.data)
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)


@api_view(['GET'])
def detail_product(request, item_id):
    product_serializer = get_products(item_id=item_id)
    return JsonResponse({'product': product_serializer.data})
