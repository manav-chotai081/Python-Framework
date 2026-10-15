from django.db import models
from django.contrib.auth.models import User

# 1. User Profile for Retail vs Wholesale (Electrician/Contractor)
class CustomerProfile(models.Model):
    CUSTOMER_TYPE_CHOICES = (
        ('retail', 'Retail Customer'),
        ('contractor', 'Electrician / Contractor (Wholesale)'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='retail')
    phone = models.CharField(max_length=15, blank=True)
    business_name = models.CharField(max_length=100, blank=True, help_text="Firm / Electrician Name")
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_customer_type_display()})"


# 2. Product Category (Switches, Wires, Lights, etc.)
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# 3. Product Model with Dual-Tier Pricing and Stock
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, default='General')
    description = models.TextField(blank=True)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Regular Customer Price")
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Contractor/Electrician Price")
    stock = models.IntegerField(default=10, help_text="Current available stock")
    low_stock_limit = models.IntegerField(default=5, help_text="Alert shopkeeper when stock reaches this limit")
    min_order_qty = models.IntegerField(default=1, help_text="Minimum Order Quantity (MOQ)")
    unit = models.CharField(max_length=20, default='Piece', help_text="Piece, Meter, Box, Coil")

    def __str__(self):
        return f"{self.name} - {self.brand}"

    @property
    def is_low_stock(self):
        return self.stock <= self.low_stock_limit


# 4. Order Model with Delivery vs In-Store Pickup
class Order(models.Model):
    FULFILLMENT_CHOICES = (
        ('pickup', 'In-Store Pickup (Quick Counter)'),
        ('delivery', 'Home Delivery'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Ready', 'Ready / Packed'),
        ('Completed', 'Completed / Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    fulfillment_type = models.CharField(max_length=20, choices=FULFILLMENT_CHOICES, default='pickup')
    delivery_address = models.TextField(blank=True, help_text="Required if Home Delivery selected")
    payment_method = models.CharField(max_length=50, default='Cash on Delivery / Pay at Counter')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - Rs.{self.total_amount}"


# 5. Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.quantity * self.price
