from django.shortcuts import render
from .forms import ProductForm


def add_product(request):
    """ Add a product to the store """
    
    form = ProductForm()
    template = 'management_dashboard/add_product.html'
    context = {
        'form': form,
    }
    
    return render(request, template, context)
