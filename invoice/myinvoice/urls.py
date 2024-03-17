from django.urls import path
from . import views

urlpatterns = [
    path('invoices/', views.invoicelist, name='invoice'),
    path('invoices/<int:pk>/', views.invoicedetail, name='detail'),
]
