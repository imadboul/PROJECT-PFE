
from django.contrib import admin
from django.urls import path
from .views import getbalance, payments , validatePayment, get_payment
urlpatterns = [
    path('balance/',getbalance),
    path('payments/', payments),
    path('validatePayment/', validatePayment),
    path('payments/<int:id>', get_payment),
    
]
