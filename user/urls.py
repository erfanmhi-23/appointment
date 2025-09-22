from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("signup/",  views.signup,      name="signup"),
    path("login/",   views.login_view,  name="login"),
    path("logout/",  views.logout_view, name="logout"),
    path("profile/", views.profile,     name="profile"),
    path("update/",  views.update,      name="update"),
    path("delete/", views.delete_account, name="delete_account"),
    

    path("login/email/", views.send_email_otp, name="send_email_otp"),
    path("login/email/verify/", views.verify_email_otp, name="verify_email_otp"),
]
