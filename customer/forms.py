from django import forms
from .models import Customer
from .models import Address
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import Account


class SignupForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ["username", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(UserChangeForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Nome"
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Email"
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Telefone"
    )

    class Meta:
        model = Account
        fields = ["first_name", "email", "phone_number"]


class CustomUserUpdateForm(UserChangeForm):
    password = None

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Usuario"
    )
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
        model = Account
        fields = ["username", "first_name", "last_name", "email"]


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
