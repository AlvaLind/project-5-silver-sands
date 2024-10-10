from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse

from .forms import UserProfileForm
from .models import UserProfile, Favourite
from checkout.models import Order
from products.models import Wine


@login_required
def profile(request):
    """
    Display the user's profile.
    """

    user_profile = UserProfile.objects.get(user=request.user)

    orders = user_profile.orders.all().order_by('-date')

    # Show 10 orders per page
    paginator = Paginator(orders, 9)
    # Get the current page number from the query string
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

        else:
            messages.error(request, 'Update failed. Please ensure the \
                form is valid.')
    else:
        form = UserProfileForm(instance=user_profile)
        orders = user_profile.orders.all()

    template = 'profiles/profile.html'
    context = {
            'form': form,
            'orders': page_obj,
            'show_signup_form': True,
        }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def add_to_favourites(request, wine_id):
    """
    Add a product to favourites
    """

    wine = get_object_or_404(Wine, id=wine_id)
    favourite_entry, created = Favourite.objects.get_or_create(
        user=request.user, wine=wine)

    messages.success(request, f'{wine.name} has been added to your favourites')

    return HttpResponseRedirect(reverse('product_details', args=[wine_id]))


@login_required
def remove_from_favourites(request, wine_id):
    """
    Remove a product from favourites
    """

    wine = get_object_or_404(Wine, id=wine_id)
    favourite_entry = (
        get_object_or_404(Favourite, user=request.user, wine=wine))
    favourite_entry.delete()
    messages.success(request, f'{wine.name} has been removed from your \
        favourites')

    referer_url = request.META.get('HTTP_REFERER')
    if not referer_url:
        referer_url = reverse('product_details', args=[wine_id])

    return HttpResponseRedirect(referer_url)


@login_required
def favourites(request):
    """
    View to display the list of wines the user has added to their favourites
    """

    # Get all the favourite wines of the logged-in user
    favourite_wines = (
        Favourite.objects.filter(user=request.user)
        .select_related('wine')
        .order_by('wine__name')
    )
    
    # Paginate the favourite wines, 9 per page
    paginator = Paginator(favourite_wines, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'favourite_wines': favourite_wines,
        'page_obj': page_obj,
    }

    return render(request, 'profiles/favourites.html', context)
