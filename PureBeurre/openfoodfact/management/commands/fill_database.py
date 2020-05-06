from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from products.models import Category, Product



class Command(BaseCommand):
    help = "command wich fills the database"
    
    def handle(self, *args, **options):
        if len(Product.objects.all()) > 0:
            self.stdout.write("La base de données est déjà remplie")
        else:
            with transaction.atomic():

                Category.objects.fill_categories()
                Product.objects.fill_products()
            
            self.stdout.write("Commande effectuée avec succès")
        