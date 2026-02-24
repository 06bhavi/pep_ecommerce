from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product
from django.contrib import messages

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Increased quantity of {product.name}.")
    else:
        messages.success(request, f"Added {product.name} to cart.")
    
    return redirect('cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(cart=cart, product=product).delete()
    messages.info(request, f"Removed {product.name} from cart.")
    return redirect('cart_detail')

@login_required
def cart_update(request, product_id, action):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    if action == 'increment':
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, "Not enough stock available.")
    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            
    return redirect('cart_detail')
