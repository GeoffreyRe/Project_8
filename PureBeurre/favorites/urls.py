from django.urls import path

from . import views

urlpatterns = [path("<product_id>/<substitute_id>", views.add_favorite, name="add_favorite"),
               path("", views.user_favorites, name="user_favorites")]
