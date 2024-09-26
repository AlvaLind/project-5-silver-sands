from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty at the moment!")
        return redirect(reverse('product_list'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Q3J6UD04dApxxYMXPq2lx1fn1E1ddFc9asXBqb44oMdc16vzAj7WJ169cIHcghN1RidtPBXk80mIabx0DDJtjN500PeMQih6t',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
