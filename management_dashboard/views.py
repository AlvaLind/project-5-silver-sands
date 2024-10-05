from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Sum

from products.models import Wine
from checkout.models import Order
from .forms import ProductForm
from .forms import OrderStatusForm


@login_required
def add_product(request):
    """ Add a product to the store """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully added product!')
                return redirect(reverse('add_product'))
            else:
                messages.error(request, 'Failed to add product. Please ensure the form is valid.')
        except ValidationError as e:
            messages.error(request, f"Error: {e.message}")
        except IntegrityError:
            messages.error(request, 'Failed to add product. A product with that name already exists.')
    else:
        form = ProductForm()

    template = 'management_dashboard/add_product.html'
    context = {
        'form': form,   
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
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully updated product!')
                return redirect(reverse('product_details', args=[wine_id]))
            else:
                messages.error(request, 'Failed to update product. Please ensure the form is valid.')
        except ValidationError as e:
            messages.error(request, f"Error: {e.message}")
        except IntegrityError:
            messages.error(request, 'Failed to update product. A product with that name already exists.')
    else:
        form = ProductForm(instance=wine)
        messages.info(request, f'You are editing {wine.name}')

    
    template = 'management_dashboard/edit_product.html'
    context = {
        'form': form,
        'wine': wine,
        'no_bag_on_success': False,
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


from .forms import OrderStatusForm

@login_required
def manage_orders(request):
    """ View all store orders and update order status """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    orders = Order.objects.all().order_by('-date')
    status_filter = request.GET.get('status')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
        
    # Calculating analytics
    total_fulfilled = orders.filter(status='fulfilled').count()
    total_refunded = orders.filter(status='returned').count()
    total_unfulfilled = orders.exclude(status__in=['fulfilled', 'returned']).count()
    total_sales = orders.aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    
    order_status_choices = Order.ORDER_STATUS_CHOICES
        
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        form = OrderStatusForm(request.POST, instance=order)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Order status updated successfully.')
            return redirect('manage_orders')
        else:
            messages.error(request, 'Error updating order status.')

    context = {
        'orders': orders,
        'total_fulfilled': total_fulfilled,
        'total_refunded': total_refunded,
        'total_unfulfilled': total_unfulfilled,
        'total_sales': total_sales,
        'order_status_choices': order_status_choices,
    }
    
    return render(request, 'management_dashboard/manage_orders.html', context)
