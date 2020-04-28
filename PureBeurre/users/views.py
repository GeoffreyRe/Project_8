from django.shortcuts import render, redirect
from .forms import SignUpForm 
from pages.views import home
from users.models import User
from django.db.utils import IntegrityError
from django.contrib.auth import login as log

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #TODO créer l'utilisateur et l'insérer dans la base de données
            print(form.cleaned_data)
            try:
                user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password']) 
            except IntegrityError:
                return render(request, 'users/login.html', {"form" : form, "user_exists": True})

            log(request, user)
            return redirect(home)
    else: # if request method is "get"
        form = SignUpForm()
    return render(request, 'users/login.html', {"form" : form, "user_exists" : False})