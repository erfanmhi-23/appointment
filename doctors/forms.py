from django import forms
from django.contrib.auth import get_user_model
from .models import Doctor , Office , Timesheet


User = get_user_model()

class DoctorCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150 , label="نام کاربری")
    password = forms.CharField(widget=forms.PasswordInput, label="رمز")
    first_name = forms.CharField(max_length=30, label="نام")
    last_name = forms.CharField(max_length=150, label="نام خانوادگی")
    email = forms.EmailField(required=False, label="ایمیل")

    class Meta:
        model = Doctor
        fields = ['field', 'expertise', 'np', 'image']
        labels = {
            'field': 'رشته',
            'expertise': 'تخصص',
            'np': 'شماره نظام پزشکی',
            'image': 'عکس',
        }

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

class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['location', 'phone_num', 'price']
        labels = {
            'location':'مکان',
            'phone_num': 'شماره تلفن',
            'price':'قیمت'
        }

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['start', 'end', 'duration']
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duration': forms.NumberInput(attrs={'min': 0}),
        }
    

