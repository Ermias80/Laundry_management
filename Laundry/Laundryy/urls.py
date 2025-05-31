from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('Admin/', views.Admin, name='Admin'),
    path('auth/', views.sign_up_or_sign_in, name='sign_up_or_sign_in'),
    path('order/', views.order_page, name='order_page'),
    path('order/add/', views.add_to_cart, name='add_to_cart'),
    path('order/remove/<str:service_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/clear/', views.clear_cart, name='clear_cart'),  # New URL for clearing cart
    path('payment/', views.payment, name='payment'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),  # Added
    path('logout/', views.logout_view, name='logout'),
]