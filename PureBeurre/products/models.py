from django.db import models
from django.conf import settings
from favorites.models import Favorite

# Create your models here.
class Product(models.Model):
    barcode = models.CharField(max_length=20, primary_key=True)
    product_name = models.CharField(max_length=80)
    brand = models.CharField(max_length=80)
    url = models.URLField()
    nutrition_grade = models.CharField(max_length=1)
    nutrition_score = models.SmallIntegerField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class Category(models.Model):
    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
