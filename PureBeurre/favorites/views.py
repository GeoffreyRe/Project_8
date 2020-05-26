from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Favorite
from django.contrib.auth.decorators import login_required
from users.models import User
from products.models import Product
from .import_export_favorites import serialize_favorites_from_user as serialize
# Create your views here.


# user has to be logged if he want to see favorites
@login_required(login_url='login')
def user_favorites(request):
    """
    This view allows user to see favorites linked with his account
    """
    current_user_id = request.session.get(
        "_auth_user_id")  # We retrieve user id
    user = User.objects.get(id=current_user_id)
    user_favorites_set = Favorite.objects.get_favorites_from_user(user)
    return render(request, "favorites/favorites.html", {"favorites": user_favorites_set})


@login_required(login_url='login')
def add_favorite(request, product_id, substitute_id):
    """
    This view allow a specific user to save a favorite into database
    """
    current_user_id = request.session.get(
        "_auth_user_id")  # We retrieve user id
    user = User.objects.get(id=current_user_id)
    try:
        product, substitute = (Product.objects.get(barcode=product_id),
                               Product.objects.get(barcode=substitute_id))
    except IntegrityError:
        # if the product or substitute doesn't exist
        return redirect('/')
    favorite = Favorite(user=user, product=product, substitute=substitute)
    try:
        favorite.save()
    except IntegrityError:
        # if tuple (product, substitute) is already save as favorite
        return redirect('/')

    return redirect("user_favorites")


@login_required(login_url='login')
def export_favorites_from_user(request):
    current_user_id = request.session.get(
        "_auth_user_id")
    user = User.objects.get(id=current_user_id)
    json_file = serialize(user)
    response = HttpResponse(json_file, content_type='text/json')
    response['Content-Disposition'] = 'attachment; filename="favorites_{}.json"'.format(user.username)
    return response