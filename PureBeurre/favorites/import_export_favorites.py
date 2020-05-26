from .models import Favorite
from json import dumps


def serialize_favorites_from_user(user):
    user_favorites = Favorite.objects.get_favorites_from_user(user)
    favorites_list = []

    for fav in user_favorites:
        fav_dict = {}
        fav_dict["Code barre produit"] = fav.product.barcode
        fav_dict["Nom produit"] = fav.product.product_name
        fav_dict["Marque produit"] = fav.product.brand
        fav_dict["Code barre substitut"] = fav.substitute.barcode
        fav_dict["Nom substitut"] = fav.substitute.product_name
        fav_dict["Marque substitut"] = fav.substitute.brand
        favorites_list.append(fav_dict)

    return dumps(favorites_list, indent=4, ensure_ascii=False).encode('utf8')