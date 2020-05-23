from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login')
def user_profile(request):
    """
    This view renders profile template wich shows informations about logged user
    """
    return render(request, 'profiles/profile.html')
