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
from .import_export_favorites import file_imported_and_is_json, analyse_fav_to_add
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
    """
    This view will export a json file that contains
    favorites of user
    """
    # we retrieve user of current session
    current_user_id = request.session.get(
        "_auth_user_id")
    user = User.objects.get(id=current_user_id)
    json_file = serialize(user)
    # we send file and we specify that the response contains a file to download
    response = HttpResponse(json_file, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="favorites_{}.json"'.format(user.username)
    return response

@login_required(login_url='login')
def import_json_file(request):
    """
    This method handle import of json file and recording
    of new products
    """
    if request.method == 'POST':
        # we check if a file is imported and if it is a json file
        json_file = file_imported_and_is_json(request)
        # if methods returns false, we redirects user
        if json_file is False:
            return redirect('user_favorites')
        binary_datas = json_file.read()
        # we retrieve informations about products inside file
        fav_list_to_add = find_favorites_from_json(binary_datas)
        fav_list_to_add = analyse_fav_to_add(request, fav_list_to_add)
        if fav_list_to_add is False:
            return redirect('user_favorites')
        # we try to record new products into dtb and we display messages
        results_dtb = add_favorites_from_json(request, fav_list_to_add)
        for info in results_dtb:
            messages.info(request, info)
        return redirect('user_favorites')
        