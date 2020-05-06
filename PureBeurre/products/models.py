from django.db import models, Error, IntegrityError, transaction
from django.conf import settings
from favorites.models import Favorite
from openfoodfact.api import Api
import json

#with add a method to the manager (objects) of Product 
class ProductManager(models.Manager):
    def fill_products(self):
        off = Api()
        results = off.get_request_response_from_api()
        with open("static/json/categories.json", "r", encoding="utf8") as file:
            categories_list = json.load(file)
        for category_dict in categories_list:
            for sub_category in category_dict["sub-category"]:
                products_of_category = results[sub_category]
                sub_cat = Category.objects.get(name=sub_category)
                for product_infos in products_of_category:
                    product = Product(barcode=product_infos["_id"],
                                        product_name=product_infos["product_name"],
                                        brand=product_infos["brands"],
                                        url_page=product_infos["url"],
                                        image_url=product_infos["image_url"],
                                        image_nutrition_url=product_infos["image_nutrition_url"],
                                        nutrition_grade=product_infos["nutrition_grades"],
                                        nutrition_score=product_infos["nutrition-score-fr"],
                                        category=sub_cat)

                    with transaction.atomic():
                        try:
                            product.save(force_insert=True)
                        except IntegrityError:
                            pass


# We add a method to the manager (objects) of Category
class CategoryManager(models.Manager):
    def fill_categories(self):
        with open("static/json/categories.json", "r", encoding="utf8") as file:
            categories_list = json.load(file)
        for category_dict in categories_list:
            category = Category(name=category_dict["category"])
            try:
                category.save()
            except:
                raise Error("impossible d'enregistrer la categorie {}".format(category.name))
            for sub_category in category_dict["sub-category"]:
                sub_category = Category(name=sub_category, parent_category=category)
                try:
                    sub_category.save()
                except:
                    raise Error("Impossible d'eneregistrer la sous-categorie {}".format(sub_category.name))

# Create your models here.
class Product(models.Model):
    barcode = models.CharField(max_length=20, primary_key=True)
    product_name = models.CharField(max_length=80)
    brand = models.CharField(max_length=80)
    url_page = models.URLField()
    image_url = models.URLField()
    image_nutrition_url = models.URLField()
    nutrition_grade = models.CharField(max_length=1)
    nutrition_score = models.SmallIntegerField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    objects = ProductManager()

    def __str__(self):
        return self.product_name

class Category(models.Model):
    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name
