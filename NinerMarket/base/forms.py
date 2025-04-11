from django.forms import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name','username', 'email', 'password1', 'password2']

        def email_validation(self):
            email = self.cleaned_data.get('email')
            if not email.endswith('@charlotte.edu'):
                raise forms.ValidationError("Email not valid at this time")
            return email