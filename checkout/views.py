from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Wine
from bag.contexts import bag_contents

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    # If user submits checkout form
    if request.method == 'POST':
        print("POST checkout form activated")
        
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in bag.items():
                try:
                    wine = Wine.objects.get(id=item_id)
                    # Directly use item_data as the quantity
                    quantity = item_data  # item_data will be an integer
                    if quantity > 0:  # Only create order line item if quantity is greater than 0
                        order_line_item = OrderLineItem(
                            order=order,
                            wine=wine,
                            quantity=quantity,
                        )
                        order_line_item.save()
                except Wine.DoesNotExist:
                    messages.error(request, (
                        "One of the wines in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST # Save the users profile info to the session 
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
                        
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "Your bag is empty at the moment!")
            return redirect(reverse('wine_list'))
        
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount = stripe_total,
            currency = settings.STRIPE_CURRENCY,
        )
        client_secret = intent.client_secret
        
    order_form = OrderForm()
    
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')
        
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle a users successful checkout
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Congratulations your order was successful! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')
    if 'bag' in request.session:
        del request.session['bag']
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)