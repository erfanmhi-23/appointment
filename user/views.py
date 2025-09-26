from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, login
from .forms import EmailForm
from .models import EmailOTP
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib import messages
from wallet.models import Wallet

###email otp 
User = get_user_model()

def send_email_otp(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            otp_code = EmailOTP.generate_otp()
            EmailOTP.objects.create(email=email, code=otp_code)
            send_mail(
                "کد ورود شما",
                f"کد ورود شما: {otp_code}",
                "noreply@example.com",
                [email],
                fail_silently=False,
            )
            request.session["email"] = email
            messages.success(request, "کد OTP به ایمیل شما ارسال شد.")
            return redirect("verify_email_otp")
    else:
        form = EmailForm()
    return render(request, "user/email_form.html", {"form": form})


def verify_email_otp(request):
    if request.method == "POST":
        code = request.POST.get("code")
        email = request.session.get("email")
        try:
            otp = EmailOTP.objects.filter(email=email, code=code, is_used=False).latest("created_at")
        except EmailOTP.DoesNotExist:
            messages.error(request, "کد اشتباه است یا پیدا نشد.")
            return redirect("verify_email_otp")
        if otp.is_expired():
            messages.error(request, "کد منقضی شده است.")
            return redirect("send_email_otp")
        otp.is_used = True
        otp.save()
        user, created = User.objects.get_or_create(username=email, defaults={"email": email})
        login(request, user)
        messages.success(request, "ورود موفقیت‌آمیز بود.")
        return redirect("home")
    return render(request, "user/verify_email_otp.html")

def google_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("کد OAuth گوگل پیدا نشد!")

    return HttpResponse(f"ورود با گوگل موفق! کد برگشتی گوگل: {code}")




@login_required
def profile_view(request):
    user = request.user
    wallet = None

    
    try:
        wallet = user.wallet
    except Wallet.DoesNotExist:
        wallet = None

    if request.method == 'POST':
        
        amount = request.POST.get('amount')
        try:
            amount = int(amount)
            if amount > 0:
                if wallet:
                    wallet.inventory = F('inventory') + amount
                    wallet.save()
                    messages.success(request, f'موجودی شما به اندازه {amount} تومان افزایش یافت.')
                else:
                    messages.error(request, 'کیف پول شما موجود نیست.')
            else:
                messages.error(request, 'مقدار باید عدد مثبت باشد.')
        except ValueError:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید.')
        return redirect('profile')

    return render(request, 'user/profile.html', {
        'user': user,
        'wallet': wallet,
    })
