from rest_framework import serializers
from .models import ProductEntry


class ProductSerializer(serializers.ModelSerializer):
    # product_image = serializers.ImageField(required=False)
    product_image = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True, required=False)

    class Meta:
        model = ProductEntry
        # fields = ['id', 'product_image', 'product_name', 'product_size', 'product_price', 'product_description']
        fields = '__all__'
