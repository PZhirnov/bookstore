from django import forms
from .models import Author
from django.contrib import admin
from .validators import validate_last_name, valid_email


class AuthorForm(forms.ModelForm):
    last_name = forms.CharField(validators=[validate_last_name])
    email = forms.EmailField(validators=[valid_email])

    class Meta:
        fields = ['first_name', 'middle_name', 'last_name', 'age', 'email']
        model = Author

    # def get_context(self):
    #     context = super(AuthorForm, self).get_context()
    #     # self.fields['first_name'].widget.attrs['class'] = 'form-control'
    #     for field in self.fields:
    #         print(self.fields[field].label)   # скорректировать подписи полей
    #         self.fields[field].widget.attrs['class'] = 'form-control'  # добавить атрибуты полям
    #     return context

    # clean_nameoffield # validation
    def clean_first_name(self):
        name = self.cleaned_data.get("first_name")
        print(name)
        if name.upper() == "HELLO":
            raise forms.ValidationError("Not a valid name")
        return name
