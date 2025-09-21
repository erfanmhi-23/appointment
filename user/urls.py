from django.urls import path
from . import views

urlpatterns = [
    path('login/email/', views.send_email_otp, name='send_email_otp'),
    path('login/email/verify/', views.verify_email_otp, name='verify_email_otp'),
    path('google/callback/', views.google_callback , name='google_callback'),
]
