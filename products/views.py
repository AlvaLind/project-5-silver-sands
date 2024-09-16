from django.shortcuts import render, get_object_or_404
from .models import Wine, Category
from datetime import datetime


def product_list(request):
    """
    View function to display a list of all wines.
    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: The rendered template with the list of wines.
    """
    # Fetch all Wine and Category items
    wines = Wine.objects.all() 
    categories = Category.objects.all() 

    # Fetch all filter inputs
    category_filter = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    # Apply category, price and availability filters
    if category_filter:
        wines = wines.filter(category__name=category_filter)
    if price_min:
        wines = wines.filter(price__gte=price_min)
    if price_max:
        wines = wines.filter(price__lte=price_max)
        
    context = {
        'wines': wines,
        'categories': categories,
    }
    return render(request, 'product_list.html', context)


def product_details(request, wine_id):
    """
    View to display the details of a single wine item and handle adding it to user basket.
    """
    wine = get_object_or_404(Wine, id=wine_id)
    context = {
        'wine': wine,
    }
    return render(request, 'product_details.html', context)
