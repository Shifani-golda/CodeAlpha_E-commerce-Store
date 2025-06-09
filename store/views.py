from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .models import CartItem



@login_required(login_url='login')
def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'store/index.html', {
        'products': products,
        'categories' : categories,
        'show_sidebar' : True,})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # default quantity = 1

    # Get or create active order (cart)
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)

    # Get or create order item
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if not created:
        order_item.quantity += quantity
    else:
        order_item.quantity = quantity

    # <== IMPORTANT: Set price here!
    order_item.price = product.price  # Save current product price to OrderItem.price

    order_item.save()

    return redirect('view_cart')

from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

@login_required
def view_cart(request):
    order = Order.objects.filter(user=request.user, is_completed=False).first()
    cart_items = OrderItem.objects.filter(order=order) if order else []

    # ✅ Add subtotal to each cart item (price × quantity)
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity

    # ✅ Total sum of all subtotals
    total = sum(item.subtotal for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# store/views.py
from django.shortcuts import render

def register(request):
    return render(request, 'store/register.html')

def update_cart(request):
    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('quantity_'):
                item_id = key.split('_')[1]
                quantity = int(request.POST[key])
                item = OrderItem.objects.get(id=item_id)
                item.quantity = quantity
                item.save()
    return redirect('view_cart')

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import redirect
from .models import Product


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Order, OrderItem

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        order = Order.objects.get(user=request.user, is_completed=False)
        order_item = OrderItem.objects.get(order=order, product=product)
        order_item.delete()
    except (Order.DoesNotExist, OrderItem.DoesNotExist):
        pass

    return redirect('view_cart')

from store.models import Category

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products, 'categories': categories})

from django.shortcuts import get_object_or_404


def store_by_category(request, category_id):
    categories = Category.objects.all()
    selected_category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=selected_category)

    context = {
        'products': products,
        'categories': categories,
        'show_sidebar': True,
    }

    # Use the main product listing template
    return render(request, 'store/index.html', context)

from django.shortcuts import render

def welcome(request):
    return render(request, 'store/welcome.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

@login_required
def checkout(request):
    try:
        order = Order.objects.get(user=request.user, is_completed=False)
    except Order.DoesNotExist:
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('view_cart')

    cart_items = OrderItem.objects.filter(order=order)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('view_cart')

    if request.method == 'POST':
        # Mark the order as completed
        order.is_completed = True
        order.save()

        return render(request, 'store/checkout_success.html', {'order': order})

    # For GET request: calculate subtotal for each item using saved price in OrderItem
    for item in cart_items:
        item.subtotal = item.price * item.quantity  # <-- Use item.price here

    total = sum(item.subtotal for item in cart_items)

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })
