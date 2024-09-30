from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import ProductForm
from django.contrib import messages

from products.models import Wine



def add_product(request):
    """ Add a product to the store """
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'management_dashboard/add_product.html'
    context = {
        'form': form,
        'on_add_product_page': True,
    }
    
    return render(request, template, context)


def edit_product(request, wine_id):
    """ Edit a product in the store """
    
    wine = get_object_or_404(Wine, pk=wine_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=wine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_details', args=[wine_id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=wine)
        messages.info(request, f'You are editing {wine.name}')
    
    template = 'management_dashboard/edit_product.html'
    context = {
        'form': form,
        'wine': wine,
    }
    return render(request, template, context)
