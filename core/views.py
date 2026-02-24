from django.shortcuts import render
from products.models import Product, Category
from .models import Banner

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(stock__gt=0).order_by('-created_at')[:8]
    banner = Banner.objects.filter(active=True).first()
    return render(request, 'core/home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'banner': banner
    })
