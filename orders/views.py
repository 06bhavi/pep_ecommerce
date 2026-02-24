from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import Cart
from products.models import Product
from django.contrib import messages
from django.db import transaction

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('product_list')

    if request.method == 'POST':
        # Simulate payment and order creation
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
                total_price=cart.total_price,
                status='Completed' # Simulated immediate payment success
            )
            
            for item in cart.items.all():
                # Stock validation
                if item.product.stock < item.quantity:
                    messages.error(request, f"Sorry, {item.product.name} is out of stock.")
                    transaction.set_rollback(True)
                    return redirect('cart_detail')
                
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                
                # Reduce stock
                item.product.stock -= item.quantity
                item.product.save()
            
            # Clear cart
            cart.items.all().delete()
            
        messages.success(request, "Order placed successfully!")
        return redirect('order_history')

    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        if product.stock < 1:
            messages.error(request, f"Sorry, {product.name} is out of stock.")
            return redirect('product_detail', slug=product.slug)
            
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
                total_price=product.price,
                status='Completed'
            )
            
            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=1
            )
            
            product.stock -= 1
            product.save()
            
        messages.success(request, "Order placed successfully!")
        return redirect('order_history')

    return render(request, 'orders/checkout.html', {'product': product, 'is_buy_now': True})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'Cancelled':
        with transaction.atomic():
            order.status = 'Cancelled'
            order.save()
            
            # Restock items
            for item in order.items.all():
                if item.product:
                    item.product.stock += item.quantity
                    item.product.save()
                    
        messages.success(request, f"Order #{order.id} has been cancelled.")
    else:
        messages.info(request, "This order is already cancelled.")
        
    return redirect('order_history')

@login_required
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/invoice.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
