from django import forms
from .models import Usuario
from .models import Endereco


class UserForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-field'}),
        label="Nome"
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-field'}),
        label="Email"
    )
    telefone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-field'}),
        label="Telefone"
    )

    class Meta:
        model = Usuario
        fields = ["nome", "email", "telefone"]

class AddressForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['logradouro', 'rua', 'bairro', 'cidade', 'estado', 'cep']