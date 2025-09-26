from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .models import Wallet
from doctors.models import Doctor,Office,Visittime  # مطمئن شو اسم مدل درست است
from wallet.forms import WalletCreateForm  

@login_required
def create_wallet(request):
    user = request.user
    
    if hasattr(user, 'wallet'):
        messages.info(request, "کیف پول شما قبلاً ساخته شده است.")
        return redirect('profile')

    if request.method == "POST":
        form = WalletCreateForm(request.POST)
        if form.is_valid():
            cart_num = form.cleaned_data['cart_num']  
            
            Wallet.objects.create(user=user, cart_num=cart_num, inventory=0)
            messages.success(request, "کیف پول با موفقیت ساخته شد.")
            return redirect('profile')
    else:
        form = WalletCreateForm()

    return render(request, 'create_wallet.html', {'form': form})








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