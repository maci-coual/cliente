from .models import Cliente
from django import forms
from django.contrib.auth.models import User

class ClienteForm(forms.ModelForm):
    nome =            forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cpf =             forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone =        forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    datanascimento =  forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Cliente
        fields = '__all__'

class UserForm(forms.ModelForm):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password']