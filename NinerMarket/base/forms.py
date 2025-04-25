from django.forms import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['university', 'name','username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@charlotte.edu'):
            raise forms.ValidationError("Email not valid at this time")
        return email
    

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use! Please try again with a different username.")
        return username


    