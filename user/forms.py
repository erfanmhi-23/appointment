from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(AuthenticationForm):
    roles = (("doctor", "دکتر"), ("patient", "بیمار"))
    role = forms.ChoiceField(choices=roles, label="نقش")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "location", "sex"]

class EmailForm(forms.Form):
    email = forms.EmailField(label="ایمیل", max_length=255)
