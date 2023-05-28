from django.db import models

PRODUCT_SIZES = (
    ("PP", "PP"),
    ("P", "P"),
    ("M", "M"),
    ("G", "G"),
    ("GG", "GG"),
)


class ProductEntry(models.Model):
    product_name = models.CharField(max_length=60, verbose_name="Titulo do Produto")
    product_size = models.CharField(max_length=2, choices=PRODUCT_SIZES, verbose_name="Tamanho")
    product_price = models.DecimalField(decimal_places=2, max_digits=30, verbose_name="Preço")
    product_description = models.CharField(max_length=500,
                                           default="Description not found.", verbose_name="Descrição do Produto")
    product_image = models.ImageField(upload_to="", default="", verbose_name="Imagem (.png)")

    def __str__(self):
        return self.product_name      
