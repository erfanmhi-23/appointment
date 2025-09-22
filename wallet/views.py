from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .models import Wallet
from doctors.models import Visittime  # مطمئن شو اسم مدل درست است

@login_required
def wallet_view(request, visit_id=None):
    # گرفتن کیف پول کاربر
    wallet = get_object_or_404(Wallet, user=request.user)
    visit = None  # مقدار پیش‌فرض

    if visit_id:
        visit = get_object_or_404(Visittime, id=visit_id, patient=request.user.patient)
        price = visit.doctor.office.price  

        if wallet.inventory >= price:
            # کم کردن موجودی
            Wallet.objects.filter(user=request.user).update(inventory=F('inventory') - price)
            messages.success(request, "✅ هزینه ویزیت پرداخت شد.")
        else:
            messages.error(request, "❌ موجودی کافی نیست!")

        return redirect("wallet_view")  # بعد پرداخت برگرد به کیف پول

    return render(request, "wallet.html", {"wallet": wallet, "visit": visit})