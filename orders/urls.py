from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
]
