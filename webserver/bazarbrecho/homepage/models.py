from django.db import models


PRODUCT_SIZES = (
    ("PP", "PP"),
    ("P", "P"),
    ("M", "M"),
    ("G", "G"),
    ("GG", "GG"),
)


# Create your models here.
class product_entry_example(models.Model):
    content = models.TextField()


class ProductEntry(models.Model):
    product_image = models.ImageField(upload_to="templates/roupas", default="")
    product_name = models.CharField(max_length=60)
    product_size = models.CharField(max_length=2, choices=PRODUCT_SIZES)
    product_price = models.FloatField()
