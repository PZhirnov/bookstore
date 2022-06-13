from django import forms
from .models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        fields = ['first_name', 'middle_name', 'last_name', 'age', 'email']
        model = Author
