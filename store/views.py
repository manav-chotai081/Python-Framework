from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Category, Product, Order, OrderItem, CustomerProfile
from .forms import RegisterForm

# Helper to check if logged in user is wholesale contractor
def is_contractor_user(user):
    if not user.is_authenticated:
        return False
    try:
        return user.customerprofile.customer_type == 'contractor'
    except CustomerProfile.DoesNotExist:
        return False

# 1. Product Catalog / Storefront
def home(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')

    products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    if search_query:
        products = products.filter(name__icontains=search_query)

    is_wholesale = is_contractor_user(request.user)

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'is_wholesale': is_wholesale,
        'search_query': search_query or '',
    })

# 2. Product Detail
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_wholesale = is_contractor_user(request.user)
    current_price = product.wholesale_price if is_wholesale else product.retail_price

    return render(request, 'store/product_detail.html', {
        'product': product,
        'is_wholesale': is_wholesale,
        'current_price': current_price,
    })

# 3. Session-based Cart Management
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})

    qty = int(request.POST.get('quantity', 1))
    if qty < product.min_order_qty:
        qty = product.min_order_qty

    str_pk = str(pk)
    if str_pk in cart:
        cart[str_pk] += qty
    else:
        cart[str_pk] = qty

    request.session['cart'] = cart
    messages.success(request, f"Added {product.name} to cart.")
    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    is_wholesale = is_contractor_user(request.user)

    for pk, qty in cart.items():
        try:
            product = Product.objects.get(pk=pk)
            unit_price = product.wholesale_price if is_wholesale else product.retail_price
            subtotal = unit_price * qty
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': qty,
                'unit_price': unit_price,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'is_wholesale': is_wholesale,
    })

def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    str_pk = str(pk)
    if str_pk in cart:
        del cart[str_pk]
        request.session['cart'] = cart
        messages.info(request, "Item removed from cart.")
    return redirect('cart_view')

# 4. Checkout & Order Placement
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('home')

    is_wholesale = is_contractor_user(request.user)
    cart_items = []
    total = 0
    for pk, qty in cart.items():
        product = get_object_or_404(Product, pk=pk)
        unit_price = product.wholesale_price if is_wholesale else product.retail_price
        subtotal = unit_price * qty
        total += subtotal
        cart_items.append({'product': product, 'qty': qty, 'price': unit_price})

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        fulfillment_type = request.POST.get('fulfillment_type', 'pickup')
        delivery_address = request.POST.get('delivery_address', '')

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            fulfillment_type=fulfillment_type,
            delivery_address=delivery_address,
            total_amount=total,
            status='Pending'
        )

        # Create Order Items & Deduct Stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['qty'],
                price=item['price']
            )
            item['product'].stock = max(0, item['product'].stock - item['qty'])
            item['product'].save()

        # Clear cart
        request.session['cart'] = {}
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('order_detail', pk=order.id)

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })

# 5. Customer Order View / Digital Receipt
@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    # Ensure user can only view their own order (unless staff)
    if not request.user.is_staff and order.user != request.user:
        return redirect('home')

    return render(request, 'store/order_detail.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})

# 6. Shopkeeper Dashboard (Simple admin panel for daily operations)
@login_required
@user_passes_test(lambda u: u.is_staff)
def shopkeeper_dashboard(request):
    orders = Order.objects.all().order_by('-created_at')
    products = Product.objects.all().order_by('stock')
    low_stock_products = [p for p in products if p.is_low_stock]

    # Handle quick stock update from dashboard
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_stock = request.POST.get('stock')
        new_retail = request.POST.get('retail_price')
        new_wholesale = request.POST.get('wholesale_price')

        if product_id:
            prod = get_object_or_404(Product, pk=product_id)
            if new_stock is not None:
                prod.stock = int(new_stock)
            if new_retail:
                prod.retail_price = float(new_retail)
            if new_wholesale:
                prod.wholesale_price = float(new_wholesale)
            prod.save()
            messages.success(request, f"Updated {prod.name} successfully.")
            return redirect('shopkeeper_dashboard')

    return render(request, 'store/dashboard.html', {
        'orders': orders,
        'products': products,
        'low_stock_products': low_stock_products,
    })

# Quick Order Status Update for Shopkeeper
@login_required
@user_passes_test(lambda u: u.is_staff)
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Ready', 'Completed']:
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} marked as {new_status}.")
    return redirect('shopkeeper_dashboard')

# 7. User Authentication Views
def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create CustomerProfile
            CustomerProfile.objects.create(
                user=user,
                customer_type=form.cleaned_data['customer_type'],
                phone=form.cleaned_data['phone'],
                business_name=form.cleaned_data['business_name'],
            )

            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your account is created.")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Logged in as {user.username}.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('home')
