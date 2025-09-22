from django.urls import path    
from . import views

urlpatterns = [

    #Show user's wallet
    path("wallet/", views.wallet_view, name="wallet_view"),

    # پرداخت برای یک ویزیت خاص
    path("wallet/pay/<int:visit_id>/", views.wallet_view, name="wallet_pay"),
]
