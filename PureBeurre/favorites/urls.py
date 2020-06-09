from django.urls import path

from . import views

# -tc- voir avec la longueur des lignes si on choisit 79 ou 99
urlpatterns = [path("<product_id>/<substitute_id>", views.add_favorite, name="add_favorite"),
               path("", views.user_favorites, name="user_favorites")]
