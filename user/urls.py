from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("select-role/", views.select_role, name="select_role"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("after-login/", views.post_login_router, name="post_login_router"),

    path("profile/", views.profile, name="profile"),
    path("profile/delete/", views.delete_account, name="delete_account"),
    path("password/change/", views.change_password, name="change_password"),
    
    path("login/email/", views.send_email_otp, name="send_email_otp"),
    path("login/email/verify/", views.verify_email_otp, name="verify_email_otp"),

    path("password/reset/", views.Reset.as_view(), name="reset"),
    path("password/reset/done/", views.ResetDone.as_view(), name="reset_done"),
    path("password/reset/confirm/<uidb64>/<token>/", views.ResetConfirm.as_view(), name="reset_confirm"),
    path("password/reset/complete/", views.ResetComplete.as_view(), name="reset_complete"),
    path("password/change/done/", views.ChangeDone.as_view(), name="change_done"),
]
