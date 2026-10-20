from django import forms

from .models import Usuario


class UsuarioForm(forms.ModelForm):
    nome = forms.CharField(label="Nome", max_length=255, strip=True)
    idade = forms.IntegerField(label="Idade", min_value=0)

    class Meta:
        model = Usuario
        fields = ["nome", "idade"]
