from django import forms
from .models import Author


class AuthorForm(forms.ModelForm):
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
