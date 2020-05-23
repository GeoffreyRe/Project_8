from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.sign_up, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout')
]
