from django import forms
from django.contrib.auth import get_user_model
from patient.models import Patient
from django.core.exceptions import ValidationError

User = get_user_model()

class PatientForm(forms.ModelForm) :
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)    

    class Meta :
        model = Patient
        fields = ['na_id','birth_date']
        widgets = {'birth_date' :forms.DateInput(attrs={"type" : "date"}), }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("این نام کاربری قبلاً ثبت شده است.")
        return username

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
        
        patient = super().save(commit=False)
        patient.user = user
        if commit:
            patient.save()
        return patient