from django.urls import path
#from .views import stripe_webhook
from . import views  # Import your view handling the webhook
from .views import (
    AddToPaymentCaseCartView,
    PaymentCaseCartDeleteView, 
    PaymentCaseCartUpdateView,
    PaymentCaseCartListView,
    PaymentCaseListView, 
    PaymentCaseDetailView,  
    PaymentsHistoryListView,
    PaymentsCaseHistoryListView,
    PaymentMenuView,
    CheckoutActionView,
    PaymentSuccessView, 
    PaymentCancelView, 
    stripe_webhook,
)

app_name = 'payments' 

urlpatterns = [
    path('payment-menu/', PaymentMenuView.as_view(), name='payment_menu'),
    path('payment-menu/payment-cases/', PaymentCaseListView.as_view(), name='payment_case_list'),
    path('payment-cases/<slug:slug>/detail/', PaymentCaseDetailView.as_view(), name='payment_case_detail'),
    path('payment-cases/addToPaymentCaseCartView/<slug:slug>/', AddToPaymentCaseCartView.as_view(), name='addToPaymentCaseCart_view'),
    path('payment-cases/paymentCaseCartView/', PaymentCaseCartListView.as_view(), name='paymentCaseCart_view'),
    path('payment-cases/delete/<slug:slug>/', PaymentCaseCartDeleteView.as_view(), name='DeleteCaseCart'),
    path('payment-cases/update/<slug:slug>/', PaymentCaseCartUpdateView.as_view(), name='UpdatedCaseCart'),
    path('payment_history/', PaymentsHistoryListView.as_view(), name='payment_history'),
    path('payment_case_history/', PaymentsCaseHistoryListView.as_view(), name='payment_case_history'),
    path('checkout-action/', CheckoutActionView.as_view(), name='checkout_action'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('cancel/', PaymentCancelView.as_view(), name='cancel'),
    path('webhook/', stripe_webhook, name='webhook'),
    
    #stripe listen --forward-to https://hnkmsm-eotc-lv-production.up.railway.app/webhook 
    #create_checkout_session
    # path('create-checkout-session/<slug:slug>/', views.create_checkout_session, name='create_checkout_session'),
    # path('success/', views.success_view, name='success'),
    # path('cancel/', views.cancel_view, name='cancel'),
    # Add other URL patterns as needed
    #path('confirmation/', PaymentConfirmationView.as_view(), name='payment_confirmation'),
    # path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
]

