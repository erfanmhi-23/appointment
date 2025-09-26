from django.contrib import admin
from wallet.models import Wallet
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user','inventory','cart_num')