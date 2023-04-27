from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

#--------------------- Usuario ---------------------#

class UserCreationFormCustom(UserCreationForm):

    username = forms.CharField(label="Usuario")
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField(required=True,label='Email')
    password1 = forms.CharField(label="Contraseña",
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label="Repetir contraseña",
                                widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class UserChangeFormCustom(UserChangeForm):
   
  password = forms.CharField(
    help_text="",
    widget=forms.HiddenInput(), required=False
  )

  email = forms.CharField(label="Email")
  first_name = forms.CharField(label="Nombre")
  last_name = forms.CharField(label="Apellido")
  password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=False)
  password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput, required=False)

  class Meta:
    model=User
    fields=('first_name', 'last_name', 'email', 'password1', 'password2')

  def clean_password2(self):

    password2 = self.cleaned_data["password2"]
    if password2 != self.cleaned_data["password1"]:
      raise forms.ValidationError("Las contraseñas no coinciden!")
    return password2
  

#--------------------- Libro ---------------------#

class LibroForm(ModelForm):
    class Meta:
        model = Libro
        fields =['titulo','autor']