from django.shortcuts import render, redirect
from django.views.generic import DetailView
from .models import Product


class DetailProduct(DetailView):
    """
    This generic view renders detail_product template wich shows informations about a product
    """
    context_object_name = "product"
    model = Product
    template_name = "products/detail_product.html"

# Create your views here.
