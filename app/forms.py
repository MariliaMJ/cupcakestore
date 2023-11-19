from django import forms
from .models import Customer
from .models import Address
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ["username", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Nome"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Sobrenome"
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Email"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CustomerForm(forms.ModelForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Telefone"
    )

    class Meta:
        model = Customer
        fields = ["phone_number"]


class AddressForm(forms.ModelForm):
    street = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Rua"
    )
    neighborhood = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Bairro"
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Cidade"
    )
    state = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Estado"
    )
    zip_code = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="CEP"
    )

    class Meta:
        model = Address
        fields = ["street", "neighborhood", "city", "state", "zip_code"]
