from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.contrib import messages

from products.models import Wine


@login_required
def add_product(request):
    """ Add a product to the store """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
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


@login_required
def edit_product(request, wine_id):
    """ Edit a product in the store """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    wine = get_object_or_404(Wine, pk=wine_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=wine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_details', args=[wine_id]))
    else:
        form = ProductForm(instance=wine)
        messages.info(request, f'You are editing {wine.name}')

    
    template = 'management_dashboard/edit_product.html'
    context = {
        'form': form,
        'wine': wine,
    }
    return render(request, template, context)


@login_required
def delete_product(request, wine_id):
    """ Delete a product from the store """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    wine = get_object_or_404(Wine, pk=wine_id)
    wines = Wine.objects.all() 
    wine.delete()
    messages.success(request, 'Product deleted!')
        
    context = {
        'wines': wines,
    }
    return render(request, 'products/product_list.html', context)
