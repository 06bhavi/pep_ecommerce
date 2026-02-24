from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from products.models import Product
from django.contrib import messages

@login_required
def wishlist_detail(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist_detail.html', {'wishlist_items': wishlist_items})

@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        wishlist_item.delete()
        messages.info(request, f"Removed {product.name} from wishlist.")
    else:
        messages.success(request, f"Added {product.name} to wishlist.")
        
    return redirect(request.META.get('HTTP_REFERER', 'wishlist_detail'))
