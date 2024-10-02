from django.shortcuts import render, redirect, reverse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from products.models import Wine

# Create your views here.
def view_bag(request):
    """ A view to renders the bag contents page """
    
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    
    wine = get_object_or_404(Wine, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    
    # Get the current quantity of the product in the user's bag (if any)
    current_bag_quantity = bag.get(item_id, 0)
    
    # Validate the wine is stock and or availability
    if wine.stock == 0 or not wine.available:
        messages.error(request, f'Sorry, {wine.name} is currently out of stock and unavailable.')
        return redirect(redirect_url)
    
    # Check if the total quantity (current + new) exceeds available stock
    if current_bag_quantity + quantity > wine.stock:
        messages.error(request, f'Sorry, there are only {wine.stock} {wine.name} left in stock.')
        return redirect(redirect_url)
        
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {wine.name} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request,f'Successfully added {wine.name} to your bag')
        
    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""
    
    wine = get_object_or_404(Wine, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    # Validate the wine is in stock and available
    if not wine.available or wine.stock == 0:
        messages.error(request, f'Sorry, {wine.name} is currently out of stock and unavailable.')
        return redirect(reverse('view_bag'))

    # Check if the requested quantity exceeds available stock
    if quantity > wine.stock:
        messages.error(request, f'Sorry, there are only {wine.stock} {wine.name} left in stock.')
        return redirect(reverse('view_bag'))

    # If quantity is valid and within the stock limits
    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request, f'Updated {wine.name} quantity to {bag[item_id]}')
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {wine.name} from your bag')
        
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    
    wine = get_object_or_404(Wine, pk=item_id)
    
    try:
        bag = request.session.get('bag', {})
        # Remove the item by its ID
        if item_id in bag:
            bag.pop(item_id)
            messages.success(request, f'Removed {wine.name} from your bag')

        # Update the session
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
    