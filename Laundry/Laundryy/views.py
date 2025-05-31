from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Service, Order, UserP, Payment
from django.views.decorators.http import require_POST
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def Admin(request):
    return render(request, 'Admin.html')

def service(request):
    return render(request, 'services.html')

def order_confirmation(request):
    return render(request, 'order_confirmation.html')

def logout_view(request):
    logout(request)
    return redirect('home')
def clear_cart(request):
    request.session['cart'] = []
    messages.success(request, "All items removed from cart")
    return redirect('order_page')

def order_page(request):
    services = Service.objects.all()
    cart = request.session.get('cart', [])
    
    # Convert cart items to order preview
    order_preview = []
    grand_total = 0
    for item in cart:
        service = get_object_or_404(Service, id=item['service_id'])
        quantity = item['quantity']
        total = service.price * quantity
        order_preview.append({
            'service': service,
            'quantity': quantity,
            'total': total
        })
        grand_total += total

    return render(request, 'order_page.html', {
        'services': services,
        'orders': order_preview,
        'total': grand_total
    })

@require_POST
def add_to_cart(request):
    service_id = request.POST.get('service')
    quantity = request.POST.get('quantity', 1)
    
    try:
        service = get_object_or_404(Service, id=service_id)
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        cart = request.session.get('cart', [])
        # Check if service already in cart
        for item in cart:
            if item['service_id'] == int(service_id):
                item['quantity'] += quantity
                break
        else:
            cart.append({
                'service_id': int(service_id),
                'quantity': quantity
            })
            
        request.session['cart'] = cart
        messages.success(request, f"Added {quantity} x {service.name} to your order")
    except (ValueError, Service.DoesNotExist) as e:
        messages.error(request, f"Error: {str(e)}")
    
    return redirect('order_page')

# views.py
@require_POST
def remove_from_cart(request, service_id):
    if service_id == 'all':
        request.session['cart'] = []
        messages.success(request, "All items removed from cart")
        return redirect('order_page')
    
    cart = request.session.get('cart', [])
    request.session['cart'] = [item for item in cart if item['service_id'] != int(service_id)]
    messages.success(request, "Item removed from cart")
    return redirect('order_page')

def payment(request):
    cart = request.session.get('cart', [])
    if not cart:
        messages.error(request, "Your cart is empty")
        return redirect('order_page')

    # Build cart_items with service objects
    cart_items = []
    grand_total = 0
    
    for item in cart:
        service = get_object_or_404(Service, id=item['service_id'])
        quantity = item['quantity']
        total = service.price * quantity
        cart_items.append({
            'service': service,
            'quantity': quantity,
            'total': total
        })
        grand_total += total

    if request.method == 'POST':
        payment_method = request.POST.get('payment-method')
        transaction_id = request.POST.get('transaction_id', '')
        
        try:
            # Create payment
            payment = Payment.objects.create(
                user=request.user,
                amount=grand_total,
                method=payment_method,
                transaction_id=transaction_id,
                is_successful=True
            )
            
            # Create orders
            for item in cart:
                service = get_object_or_404(Service, id=item['service_id'])
                Order.objects.create(
                    user=request.user,
                    service=service,
                    quantity=item['quantity'],
                    payment=payment,
                    is_completed=True
                )
            
            # Clear cart
            request.session['cart'] = []
            messages.success(request, "Payment successful! Your order has been placed.")
            return redirect('order_confirmation')
            
        except Exception as e:
            messages.error(request, f"Payment failed: {str(e)}")
            return redirect('payment')

    # Pass cart_items to template
    return render(request, 'payment.html', {
        'cart_items': cart_items,
        'total': grand_total
    })
# NEW: Function to send order notification to admin
def send_order_notification(user, payment, cart_items, total):
    subject = f'New Order #{payment.id}'
    message_lines = [
        f'New order received from {user.username} ({user.email})',
        f'Payment ID: {payment.id}',
        f'Amount: ${total:.2f}',
        f'Method: {payment.get_method_display()}',
        f'Date: {timezone.now().strftime("%Y-%m-%d %H:%M")}',
        '',
        'Order Details:'
    ]
    
    for item in cart_items:
        message_lines.append(
            f'- {item["service"].name}: {item["quantity"]} x ${item["service"].price:.2f} = ${item["total"]:.2f}'
        )
def remove_from_cart(request, service_id):
    if service_id == 'all':  # Handle 'all' case
        if 'cart' in request.session:
            del request.session['cart']
            request.session.modified = True
    elif service_id.isdigit():  # Handle numeric ID
        service_id = int(service_id)
        cart = request.session.get('cart', {})
        if str(service_id) in cart:
            del cart[str(service_id)]
            request.session['cart'] = cart
            request.session.modified = True
    
    return redirect('order_page')

def clear_cart(request):
    if request.method == 'POST':
        # Clear the cart session
        if 'cart' in request.session:
            del request.session['cart']
            request.session.modified = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
  
def sign_up_or_sign_in(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'Sign In':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('order_page')
            else:
                return render(request, 'sign_up_or_sign_in.html', {'error': 'Invalid credentials'})

        elif action == 'Register':
            fname = request.POST.get('firstname')
            lname = request.POST.get('lastname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('password')

            if not User.objects.filter(username=email).exists():
                user = User.objects.create_user(
                    username=email, first_name=fname, last_name=lname, email=email, password=password
                )
                UserP.objects.create(user=user, phone=phone)
                login(request, user)
                return redirect('order_page')
            else:
                return render(request, 'sign_up_or_sign_in.html', {'error': 'User already exists'})

    return render(request, 'sign_up_or_sign_in.html')