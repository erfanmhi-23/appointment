from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("update/", views.update, name="update"),
    path("delete/", views.delete_account, name="delete_account"),

    path("pwd/change/", views.Change.as_view(), name="password_change"),
    path("pwd/change/done/", views.ChangeDone.as_view(), name="change_done"),
    path("pwd/reset/", views.Reset.as_view(), name="password_reset"),
    path("pwd/sent/", views.ResetDone.as_view(), name="reset_done"),
    path("pwd/new/<uidb64>/<token>/", views.ResetConfirm.as_view(), name="password_reset_confirm"),
    path("pwd/done/", views.ResetComplete.as_view(), name="reset_complete"),

    path("login/email/", views.send_email_otp, name="send_email_otp"),
    path("login/email/verify/", views.verify_email_otp, name="verify_email_otp"),
]
