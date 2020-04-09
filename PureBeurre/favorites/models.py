from django.db import models
from django.conf import settings
from users.models import User

# Create your models here.

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="favorite_products")
    substitute = models.ForeignKey("products.Product", on_delete=models.CASCADE,db_column="substitute_barcode", related_name="favorite_substitutes")

    class Meta:
        unique_together = ["user", "product", "substitute"]
