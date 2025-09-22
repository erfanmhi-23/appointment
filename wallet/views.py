from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wallet
from doctors.models import Doctor, Visittime


@login_required
def wallet_view(request, visit_id=None):
    # گرفتن کیف پول کاربر
    wallet = get_object_or_404(Wallet, user=request.user)

    # اگر پرداخت برای یک ویزیت خاص باشه
    if visit_id:
        visit = get_object_or_404(VisitTime, id=visit_id, patient=request.user.patient)

        # قیمت ویزیت از office
        price = visit.doctor.office.price  

        if wallet.inventory >= price:
            # کم کردن موجودی
            from django.db.models import F

            Wallet.objects.filter(user=request.user).update(inventory=F('inventory') - price)
        

            messages.success(request, "✅ هزینه ویزیت پرداخت شد.")
        else:
            messages.error(request, "❌ موجودی کافی نیست!")

        return redirect("wallet_view")  # برگرد به کیف پول

    return render(request, "wallet/wallet_detail.html", {"wallet": wallet})

# Create your views h
