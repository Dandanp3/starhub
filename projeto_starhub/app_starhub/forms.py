from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
from .models import Curriculo

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'sobrenome', 'email', 'senha']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso. Por favor, escolha outro.")
        return email
    
class CurriculoForm(forms.ModelForm):
    class Meta:
        model = Curriculo
        fields = ['arquivo']
