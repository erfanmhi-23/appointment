from django.urls import path    
from . import views

urlpatterns = [

    #Show user's wallet
    path("wallet/", views.wallet_view, name="wallet_view"),

    # پرداخت برای یک ویزیت خاص
    path("pay/<int:doctor_id>/", views.pay, name="pay"),
]
