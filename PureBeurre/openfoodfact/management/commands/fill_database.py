from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from products.models import Category, Product
from openfoodfact.api import Api
import json

class Command(BaseCommand):
    help = "command wich fills the database"

    def get_categories_list_from_json(self):
        with open("static/json/categories.json", "r", encoding="utf8") as file:
            categories_list = json.load(file)

        return categories_list
    
    def fill_categories(self):
        categories_list = self.get_categories_list_from_json()
        for category_dict in categories_list:
            category = Category(name=category_dict["category"])
            try:
                category.save()
            except:
                raise CommandError("impossible d'enregistrer la categorie {}".format(category.name))
            for sub_category in category_dict["sub-category"]:
                sub_category = Category(name=sub_category, parent_category=category)
                try:
                    sub_category.save()
                except:
                    raise CommandError("Impossible d'eneregistrer la sous-categorie {}".format(sub_category.name))

    def fill_product(self):
        off = Api()
        results = off.get_request_response_from_api()
        for category_dict in self.get_categories_list_from_json():
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


    def handle(self, *args, **options):
        with transaction.atomic():
            self.fill_categories()
            self.fill_product()
        
        self.stdout.write("Commande effectuée avec succès")
        