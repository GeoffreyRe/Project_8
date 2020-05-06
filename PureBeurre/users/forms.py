from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class SignUpForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100)
    email = forms.EmailField(label="Adresse email")
    password = forms.CharField(label="mot de passe", max_length=32, widget=forms.PasswordInput)
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary d-block mt-5 w-min mx-auto'))
    helper.form_method = 'POST'


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100)
    password = forms.CharField(label="mot de passe", max_length=32, widget=forms.PasswordInput)
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary d-block mt-5 w-min mx-auto'))
    helper.form_method = 'POST'

