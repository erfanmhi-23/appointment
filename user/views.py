from django import forms
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, NoReverseMatch
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm

from .forms import SelectRoleForm, SignupForm, LoginForm, UserForm
from .forms import EmailForm 
from .models import EmailOTP 
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeView, PasswordChangeDoneView,)

User = get_user_model()

def select_role(request):
    if request.method == "POST":
        form = SelectRoleForm(request.POST)
        if form.is_valid():
            request.session["pending_role"] = form.cleaned_data["role"]
            return redirect("user:signup")
    else:
        form = SelectRoleForm()
    return render(request, "user/select_role.html", {"form": form})

def signup(request):
    if not request.session.get("pending_role"):
        return redirect("user:select_role")

    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        user.role = request.session.get("pending_role")
        user.save(update_fields=["role"])
        login(request, user)
        request.session.pop("pending_role", None)
        return redirect("user:post_login_router")
    return render(request, "registration/signup.html", {"form": form})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        pending_role = request.session.get("pending_role")
        if not getattr(user, "role", None) and pending_role:
            user.role = pending_role
            user.save(update_fields=["role"])
        login(request, user)
        request.session.pop("pending_role", None)
        return redirect("user:post_login_router")
    return render(request, "registration/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("user:select_role")

@login_required
def post_login_router(request):
    role = getattr(request.user, "role", None)
    try:
        if role == "doctor":
            return redirect("doctors:profile")
        if role == "patient":
            return redirect("patient:profile")
    except NoReverseMatch:
        pass
    return redirect("user:profile")

@login_required
def profile(request):
    form = UserForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "پروفایل ذخیره شد.")
        return redirect("user:profile")
    return render(request, "user/profile.html", {"form": form})

class DeleteAccountForm(forms.Form):
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)

@login_required
def delete_account(request):
    form = DeleteAccountForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if not request.user.check_password(form.cleaned_data["password"]):
            form.add_error("password", "رمز عبور اشتباه است.")
        else:
            u = request.user
            logout(request)
            u.delete()
            messages.success(request, "حساب شما حذف شد.")
            return redirect("user:select_role")
    return render(request, "user/delete_account.html", {"form": form})

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
            return redirect("user:post_login_router")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "user/change_password.html", {"form": form})



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


class DeleteAccountForm(forms.Form):
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    
@login_required
def delete_account(request):
    form = DeleteAccountForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if not request.user.check_password(form.cleaned_data["password"]):
            form.add_error("password", "رمز عبور اشتباه است.")
        else:
            logout(request)
            request.user.delete()
            return redirect("user:signup")
    return render(request, "user/delete_account.html", {"form": form})
