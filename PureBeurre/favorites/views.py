from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Favorite
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

# -tc- séparer les imports de bibliothèque des imports du projet avec une ligne vide
from users.models import User
from products.models import Product
# Create your views here. -tc- à éliminer


# user has to be logged if he want to see favorites
@login_required(login_url='login')
def user_favorites(request):
    """
    This view allows user to see favorites linked with his account
    """
    # -tc- le user peut être simplement récupéré avec request.user
    current_user_id = request.session.get( #
        "_auth_user_id")  # We retrieve user id
    user = User.objects.get(id=current_user_id)
    user_favorites_set = Favorite.objects.get_favorites_from_user(user)
    return render(request, "favorites/favorites.html", {"favorites": user_favorites_set})


@login_required(login_url='login')
def add_favorite(request, product_id, substitute_id):
    """
    This view allow a specific user to save a favorite into database
    """
    # -tc- le user peut être simplement récupéré avec request.user
    current_user_id = request.session.get(
        "_auth_user_id")  # We retrieve user id
    user = User.objects.get(id=current_user_id)
    try:
        product, substitute = (Product.objects.get(barcode=product_id),
                               Product.objects.get(barcode=substitute_id))
    except (IntegrityError, Product.DoesNotExist):
        # if the product or substitute doesn't exist
        messages.info(request, "Produit ou substitut inexistant !")
        return redirect('/')
    favorite = Favorite(user=user, product=product, substitute=substitute)
    try:
        favorite.save()
    except IntegrityError:
        # if tuple (product, substitute) is already save as favorite
        messages.info(request, "Ce favori existe déjà !")
        return redirect('/')

    return redirect("user_favorites")
