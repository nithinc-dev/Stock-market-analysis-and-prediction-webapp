     
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        

        
# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email',)

# class CustomAuthenticationForm(AuthenticationForm):
#     email = forms.EmailField(label='Email')  # Custom email field

#     class Meta:
#         model = CustomUser
#         fields = ('email', 'password')
        