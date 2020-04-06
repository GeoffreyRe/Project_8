from django.db import models

# Create your models here.
class Product(models.Model):
    barcode = models.CharField(max_length=20, primary_key=True)
    product_name = models.CharField(max_length=80)
    brand = models.CharField(max_length=80)
    url = models.URLField()
    nutrition_grade = models.CharField(max_length=1)
    nutrition_score = models.SmallIntegerField()

    def __str__(self):
        return self.product_name