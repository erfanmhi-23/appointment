from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label="ایمیل", max_length=255)
