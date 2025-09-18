from django import forms
from django.contrib.auth import get_user_model
from .models import Doctor

User = get_user_model()

class DoctorCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)

    class Meta:
        model = Doctor
        fields = ['field', 'expertise', 'np', 'image']

    def save(self, commit=True):
        user_data = {
            'username': self.cleaned_data['username'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'email': self.cleaned_data.get('email', '')
        }
        password = self.cleaned_data['password']
        user = User(**user_data)
        user.set_password(password)
        if commit:
            user.save()
        
        doctor = super().save(commit=False)
        doctor.user = user
        if commit:
            doctor.save()
        return doctor
