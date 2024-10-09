from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Sum, Q, Avg, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils import timezone

from checkout.models import Order, OrderLineItem
from products.models import Wine
from .forms import ProductForm
from .forms import OrderStatusForm


@login_required
def add_product(request):
    """
    Add a product to the store
    """

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
                messages.error(request, 'Failed to add product. \
                    Please ensure the form is valid.')
        except ValidationError as e:
            messages.error(request, f"Error: {e.message}")
        except IntegrityError:
            messages.error(request, 'Failed to add product. \
                A product with that name already exists.')
    else:
        form = ProductForm()

    template = 'management_dashboard/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, wine_id):
    """
    Edit a product in the store
    """

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
                messages.error(request, 'Failed to update product. \
                    Please ensure the form is valid.')
        except ValidationError as e:
            messages.error(request, f"Error: {e.message}")
        except IntegrityError:
            messages.error(request, 'Failed to update product. \
                A product with that name already exists.')
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
    """
    Delete a product from the store
    """

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


@login_required
def manage_orders(request):
    """
    View all store orders and update order status
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    orders = Order.objects.all().order_by('-date')

    # Calculating order analytics
    total_orders = orders.count()
    total_fulfilled = orders.filter(status='fulfilled').count()
    total_refunded = orders.filter(status='returned').count()
    total_unfulfilled = (
        orders.exclude(status__in=['fulfilled', 'returned']).count())

    # Total sales value and total qty or items sold
    total_sales = (
        orders.filter(~Q(status='returned')).aggregate(Sum('grand_total'))
        ['grand_total__sum'] or 0)
    total_items_sold = (
        OrderLineItem.objects.aggregate(total=Sum('quantity'))['total'] or 0)

    # Calculate total quantity sold for each wine
    most_sold_product = (
        OrderLineItem.objects.values('wine__name').annotate(
            total_quantity_sold=Sum('quantity')).order_by(
                '-total_quantity_sold').first())

    # Extracting the wine name and quantity sold
    most_sold_product_name = (
        most_sold_product['wine__name'] if most_sold_product else None)
    most_sold_product_qty = (
        most_sold_product['total_quantity_sold'] if most_sold_product else 0)

    # Calculate the top selling category by qty sold
    category_sales_by_qty = (
        Wine.objects.values('category__name').annotate(total_quantity_sold=(
            Sum('orderlineitem__quantity'))))
    ordered_categories_by_qty = (
        category_sales_by_qty.order_by('-total_quantity_sold'))
    top_selling_category_by_qty = ordered_categories_by_qty.first()

    # Extracting category name and total quantity sold into separate variables
    top_selling_category_name = (
        top_selling_category_by_qty['category__name'] if
        top_selling_category_by_qty else None)
    top_selling_category_qty = (
        top_selling_category_by_qty['total_quantity_sold'] if
        top_selling_category_by_qty else 0)

    # Calculate todays analytics
    today = timezone.now().date()
    orders_today = orders.filter(date__date=today)
    orders_today_count = orders_today.count()
    todays_sales = (
        orders_today.filter(~Q(status='returned')).aggregate(
            (Sum('grand_total')))['grand_total__sum'] or 0)

    # Calculate the average order value and size
    average_order_value = (
        total_sales / total_orders if total_orders > 0 else 0)
    average_order_size = (
        total_items_sold / total_orders if total_orders > 0 else 0)

    # Apply filters
    status_filter = request.GET.get('status')
    if status_filter:
        if status_filter != '':
            orders = orders.filter(status=status_filter)

    order_status_choices = Order.ORDER_STATUS_CHOICES

    # pagination by 20 orders per page
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

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
        'page_obj': page_obj,
        'total_orders': total_orders,
        'total_fulfilled': total_fulfilled,
        'total_refunded': total_refunded,
        'total_unfulfilled': total_unfulfilled,
        'total_sales': total_sales,
        'order_status_choices': order_status_choices,
        'average_order_value': average_order_value,
        'average_order_size': average_order_size,
        'most_sold_product': most_sold_product,
        'most_sold_product_name': most_sold_product_name,
        'most_sold_product_qty': most_sold_product_qty,
        'top_selling_category_name': top_selling_category_name,
        'top_selling_category_qty': top_selling_category_qty,
        'orders_today_count': orders_today_count,
        'todays_sales': todays_sales,
        'order_status_choices': order_status_choices,
        'status_filter': status_filter,
        'query_params': query_params.urlencode()
    }

    return render(request, 'management_dashboard/manage_orders.html', context)


@login_required
def order_details(request, order_id):
    """
    Get order details for the given order ID
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    order = get_object_or_404(Order, pk=order_id)
    order_line_items = OrderLineItem.objects.filter(order=order)

    items = []
    for item in order_line_items:
        items.append({
            'name': item.wine.name,
            'quantity': item.quantity
        })

    context = {
        'order_number': order.order_number,
        'total_value': order.grand_total,
        'status': order.status,
        'customer_name': order.full_name,
        'customer_email': order.email,
        'customer_street': order.street_address1,
        'customer_town': order.town_or_city,
        'items': items,
    }

    return JsonResponse(context)


@login_required
def delete_order(request, order_id):
    """
    Delete an order only if the status is 'pending'.
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('home')

    order = get_object_or_404(Order, pk=order_id)

    # Only allow deletion if the status is 'pending'
    if order.status != 'pending':
        messages.error(request, 'Order can only be deleted if \
            the status is "Pending".')
        return redirect('manage_orders')

    # Delete the order
    order.delete()
    messages.success(request, 'Order deleted successfully.')
    return redirect('manage_orders')
