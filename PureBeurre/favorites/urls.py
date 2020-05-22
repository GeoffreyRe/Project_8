from django.urls import path

from . import views

urlpatterns = [path("<product_id>/<substitute_id>", views.add_favorite, name="add_favorite"), #link a route with add_favorite method
                path("", views.user_favorites, name="user_favorites")] # idem but with user_favorites method

