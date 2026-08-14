from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=30, required=False)
    country = forms.ChoiceField(choices=User.Country.choices)
    city = forms.CharField(max_length=80, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'country', 'city', 'role', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Caractères alphanumériques et @ . + - _ uniquement'
        self.fields['password1'].help_text = 'Au minimum 8 caractères'
        self.fields['password2'].help_text = 'Confirmez votre mot de passe'
        self.fields['role'].choices = [
            choice for choice in User.Role.choices if choice[0] != User.Role.ADMIN
        ]
        self.fields['role'].label = 'Je souhaite m’inscrire en tant que'


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'country', 'city')
        labels = {'first_name': 'Prénom', 'last_name': 'Nom', 'email': 'E-mail', 'phone': 'Téléphone', 'country': 'Pays', 'city': 'Ville'}
