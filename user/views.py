from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, NoReverseMatch
from django.contrib import messages
from django.core.mail import send_mail

from .forms import EmailForm 
from .models import EmailOTP 

from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeView, PasswordChangeDoneView,)

User = get_user_model()

def signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("user:login")
    return render(request, "registration/signup.html", {"form": form})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        request.session["role"] = form.cleaned_data["role"]
        return redirect("user:update") 
    return render(request, "registration/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("user:login")

@login_required
def profile(request):
    form = UserForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("user:profile")
    return render(request, "user/profile.html", {"form": form})

@login_required
def update(request):
    role = request.session.get("role")
    try:
        if role == "doctor":
            return redirect("doctors:profile") 
        if role == "patient":
            return redirect("patient:profile")
    except NoReverseMatch:
        pass
    return redirect("user:profile")

class Reset(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.txt"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("user:reset_done")

class ResetDone(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"

class ResetConfirm(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("user:reset_complete")

class ResetComplete(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"

class Change(PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("user:change_done")

class ChangeDone(PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"

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
