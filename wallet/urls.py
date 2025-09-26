from django.urls import path    
from wallet.views import *

urlpatterns = [
    path('wallet', create_wallet, name='create_wallet'),

    #Show user's wallet
    path("wallet/", wallet_view, name="wallet_view"),

   
    
]
