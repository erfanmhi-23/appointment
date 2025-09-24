from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SelectRoleForm(forms.Form):
    ROLE_CHOICES = (("doctor", "دکتر"), ("patient", "بیمار"))
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="نقش", required=True)

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

class LoginForm(AuthenticationForm):
    pass

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "location", "sex"]

class EmailForm(forms.Form):
    email = forms.EmailField(label="ایمیل", max_length=255)
