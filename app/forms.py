from django import forms
from .models import Usuario
from .models import Endereco


class UserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nome", "email", "telefone"]

class AddressForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['logradouro', 'rua', 'bairro', 'cidade', 'estado', 'cep']