from django import forms
from .models import Customer
from .models import Address


class CustomerForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Name"
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Email"
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Phone_number"
    )

    class Meta:
        model = Customer
        fields = ["name", "email", "phone_number"]


class AddressForm(forms.ModelForm):
    street = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Street"
    )
    neighborhood = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Neighborhood"
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="City"
    )
    state = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="State"
    )
    zip_code = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-field"}), label="Zip_code"
    )

    class Meta:
        model = Address
        fields = ["street", "neighborhood", "city", "state", "zip_code"]
