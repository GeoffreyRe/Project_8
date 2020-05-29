from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from .models import Favorite
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import User
from products.models import Product
from .import_export_favorites import serialize_favorites_from_user as serialize
from .import_export_favorites import find_favorites_from_json, add_favorites_from_json
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
    response = HttpResponse(json_file, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="favorites_{}.json"'.format(user.username)
    return response

@login_required(login_url='login')
def import_json_file(request):
    if request.method == 'POST':
        try:
            json_file = request.FILES['imported_file']
        except (MultiValueDictKeyError, KeyError):
            messages.error(request, "Aucun fichier n'a été uploadé")
            return redirect('user_favorites')
        if not json_file.name.endswith(".json"):
            messages.error(request, "Le fichier uploadé n'est pas un fichier json")
            return redirect('user_favorites')
        binary_datas = json_file.read()
        #import pdb; pdb.set_trace()
        fav_list_to_add = find_favorites_from_json(binary_datas)
        if type(fav_list_to_add) is tuple:
            if fav_list_to_add[0] is False:
                messages.error(request, fav_list_to_add[1])
                return redirect('user_favorites')
            else:
                messages.warning(request, fav_list_to_add[1])
                fav_list_to_add = fav_list_to_add[2]
        if len(fav_list_to_add) == 0:
            messages.error(request, "Aucun produit à ajouter")
            return redirect('user_favorites')
        results_dtb = add_favorites_from_json(request, fav_list_to_add)
        for info in results_dtb:
            messages.info(request, info)
        return redirect('user_favorites')
        