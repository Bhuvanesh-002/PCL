# payments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process_payment, name='process_payment'),
    # Add other payment-related URLs as needed
]
