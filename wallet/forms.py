from django import forms
from django.core.validators import RegexValidator
from wallet.models import Wallet

class WalletCreateForm(forms.ModelForm):
    cart_num = forms.CharField(
        label="شماره کارت",
        max_length=30,  
        validators=[RegexValidator(r'^[\d\s-]+$', message="فقط ارقام، فاصله و خط‌تیره مجاز است.")],
        widget=forms.TextInput(attrs={'placeholder': 'مثال: 6219 1234 5678 9012'})
    )

    class Meta:
        model = Wallet
        fields = ['cart_num']

    def clean_cart_num(self):
        raw = self.cleaned_data.get('cart_num', '')
        
        digits = ''.join(ch for ch in raw if ch.isdigit())

        if len(digits) != 16:
            raise forms.ValidationError("شماره کارت باید شامل ۱۶ رقم باشد. لطفاً فقط ارقام را وارد کنید یا از فرمت بدون فاصله استفاده کنید.")

        
        try:
            return int(digits)
        except ValueError:
            raise forms.ValidationError("شماره کارت نامعتبر است.")
