"""
This module contains models of app
"""
from django.db import models
from django.conf import settings
from .managers import FavoriteManager

# Create your models here.


class Favorite(models.Model):
    """
    This is the favorite model wich contains products save as favorites by the user
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="favorites")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE,
                                related_name="favorite_products")
    substitute = models.ForeignKey("products.Product", on_delete=models.CASCADE,
                                   db_column="substitute_barcode",
                                   related_name="favorite_substitutes")
    objects = FavoriteManager()

    class Meta:
        """
        This class is used to pass some meta-datas
        """
        # a user can save only once a product and a substitute together
        unique_together = ["user", "product", "substitute"]

    def __str__(self):
        return "{} remplacé par {}".format(self.product.product_name, self.substitute.product_name)
