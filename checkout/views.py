import json

import stripe
from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Wine
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'We are sorry, but there seems to be an issue\
            with processing your payment. \
            Please try again after a few minutes.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty at the moment!")
        return redirect(reverse('product_list'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    client_secret = intent.client_secret

    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()
        if profile:
            order_form = OrderForm(initial={
                'full_name': profile.default_full_name,
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
                'country': profile.default_country,
                'postcode': profile.default_postcode,
                'town_or_city': profile.default_town_or_city,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'county': profile.default_county,
            })
        else:
            order_form = OrderForm()
    else:
        order_form = OrderForm()

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'country': request.POST.get('country', ''),
            'postcode': request.POST.get('postcode', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'county': request.POST.get('county', ''),
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            # Validate stock before saving the order
            out_of_stock = False
            insufficient_stock = False

            for item_id, quantity in bag.items():
                # Use filter and first to avoid exception
                wine = Wine.objects.filter(id=item_id).first()

                if wine is None:
                    messages.error(
                        request, "One of the wines in your bag wasn't found \
                        in our database. Please contact us for assistance.")
                    return redirect(reverse('view_bag'))

                # Check if the wine is in stock and available
                if not wine.available or wine.stock == 0:
                    out_of_stock = True
                    messages.error(request, f'Sorry, \
                    {wine.name} is unfortunately out of stock.')
                    break

                # Check if the requested quantity exceeds available stock
                if quantity > wine.stock:
                    insufficient_stock = True
                    messages.error(request, f'Sorry, there are only \
                        {wine.stock} of {wine.name} left in stock. \
                        Please update your bag.')
                    break

            if out_of_stock or insufficient_stock:
                return redirect(reverse('view_bag'))

            # If all items pass the stock check, proceed with order creation
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()

            for item_id, quantity in bag.items():
                wine = Wine.objects.get(id=item_id)
                order_line_item = OrderLineItem(
                    order=order,
                    wine=wine,
                    quantity=quantity,
                )
                order_line_item.save()

                # Reduce stock of product after successful order line creation
                wine.stock -= quantity
                wine.save()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse(
                'checkout_success', args=[order.order_number]))
        else:
            messages.error(
                request, 'Failed to complete checkout. \
                Please ensure the form is valid')

    if not stripe_public_key:
        messages.warning(
            request, 'Oh no, something happened. Please contact us.')

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
    if 'bag' not in request.session:
        return redirect('home')

    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                'default_full_name': order.full_name,
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

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
