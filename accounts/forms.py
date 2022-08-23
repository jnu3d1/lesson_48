from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
