from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(stock__gt=0)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def search(request):
    query = request.GET.get('q', '')
    
    # Simple search in product name and category
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(category__name__icontains=query)
    ).distinct()
    
    # Basic fallback: if no results, search by first word for 'related' items
    if not products and query:
        words = query.split()
        if words:
            first_word = words[0]
            products = Product.objects.filter(
                Q(name__icontains=first_word) | Q(category__name__icontains=first_word)
            ).distinct()

    return render(request, 'products/search.html', {'products': products, 'query': query})
