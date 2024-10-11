from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Avg, Value, FloatField, Q
from django.db.models.functions import Coalesce, Lower
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse

from .models import Wine, Category
from profiles.models import Favourite
from reviews.forms import ReviewForm
from reviews.models import Review


def product_list(request):
    """
    View function to display a list of wines with optional filter and sorting.
    Args:
        request (HttpRequest): The HTTP request object containing query
        parameters for filtering and sorting.
    Returns:
        HttpResponse: The rendered 'product_list.html' template with the
        filtered and sorted list of wines and available categories.
    Query Parameters:
        - category (str): Filters wines by the specified category name.
        - rating (str): Optional. Filters wines by rating. Only wines with a
        rating greater than or equal to the specified value are included.
        - sort (str): Optional. Specifies the sorting order of the wines.
        Possible values are:
            - 'rating_desc': Sorts wines by rating in descending order
            (most popular first).
            - 'name_asc': Sorts wines by name in ascending order.
            - 'price_asc': Sorts wines by price in ascending order
            (cheapest first).
    Filters:
        - category_filter: Filters wines based on the category name if provided
        - rating_filter: Filters wines based on the minimum rating if provided.
    Sorting:
        - Orders wines based on the selected sorting option.
    """
    # Fetch all Wine and Category items, and annotate with the average rating,
    # set wine with rating null to 0
    wines = Wine.objects.annotate(
    average_rating=Coalesce(
        Avg('reviews__rating'),
        Value(0.0),
        output_field=FloatField()
    )
)
    categories = Category.objects.all()

    # Fetch all filter inputs
    category_filter = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    available = request.GET.get('available')

    # Apply category, price and availability filters
    if category_filter:
        wines = wines.filter(category__name=category_filter)
    if price_min:
        wines = wines.filter(price__gte=price_min)
    if price_max:
        wines = wines.filter(price__lte=price_max)
    # Handle availability filter
    if available is not None:
        # Only filter by availability if it is explicitly set
        if available.lower() == 'true':
            wines = wines.filter(available=True)
        elif available.lower() == 'false':
            wines = wines.filter(available=False)

    # Get the sorting parameter
    sort = request.GET.get('sort')

    # Apply sorting based on the selected option
    if sort == 'rating_desc':
        wines = wines.order_by('-average_rating')
    elif sort == 'name_asc':
        wines = wines.order_by(Lower('name'))
    elif sort == 'price_asc':
        wines = wines.order_by('price')

    # Pagination
    paginator = Paginator(wines, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'wines': wines,
        'page_obj': page_obj,
        'categories': categories,
        'show_signup_form': True,
        'category_filter': category_filter,
        'price_min': price_min,
        'price_max': price_max,
        'available': available,
        'sort': sort,
    }
    return render(request, 'products/product_list.html', context)


def product_details(request, wine_id):
    """
    View to display the details of a single wine item and handle adding it
    to user basket, and handle the submission of a user review.
    """
    wine = get_object_or_404(Wine, id=wine_id)
    existing_review = None

    # Handle review form submission
    if request.method == 'POST':
        # Check if the user has already reviewed this wine
        existing_review = wine.reviews.filter(user=request.user).first()

        if existing_review:
            # User already has a review, prevent submission
            messages.error(request, 'You have already submitted a review \
                for this wine.')
            return redirect('product_details', wine_id=wine.id)

        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            # Create a new review but don't save to DB yet
            new_review = review_form.save(commit=False)
            new_review.wine = wine
            new_review.user = request.user
            new_review.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your review has been submitted and is awaiting approval'
            )
            print("Review submitted successfully")
            return redirect('product_details', wine_id=wine.id)
    else:
        review_form = ReviewForm()

    # Calculate the average rating for the wine, default to 0 if no reviews
    average_rating = wine.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Get all reviews for the wine (you might want to add pagination later)
    reviews = wine.reviews.filter(approved=True).order_by('-created_at')
    review_count = wine.reviews.filter(approved=True).count()

    in_favourites = False
    if request.user.is_authenticated:
        in_favourites = (
            Favourite.objects.filter(user=request.user, wine=wine).exists())

    context = {
        'wine': wine,
        'average_rating': round(average_rating, 1),  # Rounded to 1 decimal
        'reviews': reviews,
        'review_form': review_form,
        'existing_review': existing_review,
        'review_count': review_count,
        'show_toast_bag': True,
        'show_signup_form': True,
        'in_favourites': in_favourites,
    }
    return render(request, 'products/product_details.html', context)


@login_required
def delete_review(request, wine_id, review_id):
    """
    Delete an individual review related to a wine.

    Args:
        request: The HTTP request object.
        wine_id: The ID of the wine.
        review_id: The ID of the review to delete.
    """
    wine = get_object_or_404(Wine, pk=wine_id)
    review = get_object_or_404(Review, pk=review_id)

    # Ensure the logged-in user is the review owner
    if review.user != request.user:
        print("Error: Review delete failed - not user's review")
        raise PermissionDenied  # Raise 403 Forbidden for unauthorized users

    review.delete()
    messages.success(request, 'Your review has been deleted.')
    print("Review deleted successfully")

    return redirect('product_details', wine_id=wine.id)


@login_required
def edit_review(request, wine_id, review_id):
    """
    Edit an existing review related to a wine.

    Args:
        request: The HTTP request object.
        wine_id: The ID of the wine.
        review_id: The ID of the review to edit.
    """
    wine = get_object_or_404(Wine, pk=wine_id)
    review = get_object_or_404(Review, pk=review_id)

    # Check if the current user is the one who posted the review
    if review.user != request.user:
        messages.error(request, "You are not authorized to edit this review.")
        return redirect('product_details', wine_id=wine.id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.wine = wine
            review.approved = False
            review.save()
            messages.success(request, 'Your review has been updated.')
            print("Review edited successfully")
            return redirect('product_details', wine_id=wine.id)
        else:
            messages.error(request, "Error, unable to update review.")
            print("Error: Failed to edit review")

    return HttpResponseRedirect(
        reverse('products:product_details', args=[wine_id])
    )


def search_products(request):
    """
    Search for products by name and category with optional filter and sorting.
    """
    query = request.GET.get('query', '')
    wines = Wine.objects.all()

    if query:
        # Use Q objects for a more efficient query
        wines = wines.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )

    # Capture filter inputs
    category_filter = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    available = request.GET.get('available')

    # Apply category, price, and availability filters
    if category_filter:
        wines = wines.filter(category__name=category_filter)
    if price_min:
        wines = wines.filter(price__gte=price_min)
    if price_max:
        wines = wines.filter(price__lte=price_max)
    if available is not None:
        # Only filter by availability if it is explicitly set
        if available.lower() == 'true':
            wines = wines.filter(available=True)
        elif available.lower() == 'false':
            wines = wines.filter(available=False)

    # Get the sorting parameter
    sort = request.GET.get('sort')

    # Apply sorting based on the selected option
    if sort == 'rating_desc':
        wines = wines.annotate(
            average_rating=Coalesce(
                Avg('reviews__rating'),
                Value(0.0),
                output_field=FloatField()
            )
        ).order_by('-average_rating')

    elif sort == 'name_asc':
        wines = wines.order_by(Lower('name'))
    elif sort == 'price_asc':
        wines = wines.order_by('price')

    # Pagination: Show 9 wines per page
    paginator = Paginator(wines, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'products/search_products.html', {
        'query': query,
        'page_obj': page_obj,
        'categories': categories,
    })
