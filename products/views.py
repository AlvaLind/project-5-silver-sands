from django.shortcuts import render, get_object_or_404
from .models import Wine
from datetime import datetime


def product_list(request):
    """
    View function to display a list of all wines.
    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: The rendered template with the list of wines.
    """
    wines = Wine.objects.all()  
    context = {
        'wines': wines,
        'current_year': datetime.now().year,
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
