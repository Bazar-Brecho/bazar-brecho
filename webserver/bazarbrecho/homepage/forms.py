from django import forms
from products.models import ProductEntry


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductEntry
        fields = ['id', 'product_name', 'product_size', 'product_price', 'product_description', 'product_image']
