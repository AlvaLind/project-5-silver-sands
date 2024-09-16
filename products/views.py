from django.shortcuts import render
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