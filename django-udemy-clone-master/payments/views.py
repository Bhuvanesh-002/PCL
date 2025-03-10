from django.shortcuts import render


# payments/views.py

from django.shortcuts import render, redirect
from .models import Payment
from .forms import PaymentForm  
def process_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process the payment here
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            return redirect('payment_success')
    else:
        form = PaymentForm()
    return render(request, 'payments/payment_form.html', {'form': form})
