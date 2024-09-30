from django.shortcuts import render, redirect, reverse
from .forms import ProductForm
from django.contrib import messages



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
