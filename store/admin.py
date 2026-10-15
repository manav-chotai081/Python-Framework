from django.contrib import admin
from .models import Category, Product, Order, OrderItem, CustomerProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'retail_price', 'wholesale_price', 'stock', 'low_stock_limit')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'brand')
    list_editable = ('retail_price', 'wholesale_price', 'stock')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'fulfillment_type', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'fulfillment_type')
    inlines = [OrderItemInline]

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer_type', 'business_name', 'phone')
    list_filter = ('customer_type',)
