from django.urls import path
from . import views

urlpatterns = [
    # Storefront & Catalog
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Cart
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),

    # Orders & Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),

    # Shopkeeper Dashboard
    path('dashboard/', views.shopkeeper_dashboard, name='shopkeeper_dashboard'),
    path('order/<int:pk>/status/', views.update_order_status, name='update_order_status'),

    # Authentication
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
