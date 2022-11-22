# Generated by Django 3.2.16 on 2022-11-18 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("homepage", "0003_productentry_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productentry",
            name="product_size",
            field=models.CharField(
                choices=[
                    ("PP", "PP"),
                    ("P", "P"),
                    ("M", "M"),
                    ("G", "G"),
                    ("GG", "GG"),
                ],
                max_length=2,
            ),
        ),
    ]
