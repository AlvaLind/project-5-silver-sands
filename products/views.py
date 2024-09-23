from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Wine, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from reviews.models import Review
from datetime import datetime
from reviews.forms import ReviewForm
from django.db.models import Avg

def product_list(request):
    """
    View function to display a list of wines with optional filtering and sorting.
    Args:
        request (HttpRequest): The HTTP request object containing query parameters for filtering and sorting.
    Returns:
        HttpResponse: The rendered 'product_list.html' template with the filtered and sorted list of wines and available categories.
    Query Parameters:
        - category (str): Optional. Filters wines by the specified category name.
        - rating (str): Optional. Filters wines by rating. Only wines with a rating greater than or equal to the specified value are included.
        - sort (str): Optional. Specifies the sorting order of the wines. Possible values are:
            - 'rating_desc': Sorts wines by rating in descending order (most popular first).
            - 'name_asc': Sorts wines by name in ascending order.
            - 'price_asc': Sorts wines by price in ascending order (cheapest first).
    Filters:
        - category_filter: Filters wines based on the category name if provided.
        - rating_filter: Filters wines based on the minimum rating if provided.
    Sorting:
        - Orders wines based on the selected sorting option.
    """
    # Fetch all Wine and Category items
    wines = Wine.objects.all() 
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
        wines = wines.order_by('-rating')
    elif sort == 'name_asc':
        wines = wines.order_by('name')
    elif sort == 'price_asc':
        wines = wines.order_by('price')
        
    context = {
        'wines': wines,
        'categories': categories,
    }
    return render(request, 'product_list.html', context)


def product_details(request, wine_id):
    """
    View to display the details of a single wine item and handle adding it to user basket,
    and handle the submission of a user review.
    """
    wine = get_object_or_404(Wine, id=wine_id)
    existing_review = None
    
    # Handle review form submission
    if request.method == 'POST':
        # Check if the user has already reviewed this wine
        existing_review = wine.reviews.filter(user=request.user).first()
    
        if existing_review:
            # User already has a review, prevent submission
            messages.error(request, 'You have already submitted a review for this wine.')
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
            return redirect('product_details', wine_id=wine.id)  # Redirect to avoid duplicate submissions
    else:
        review_form = ReviewForm()
        
    # Calculate the average rating for the wine, default to 0 if no reviews
    average_rating = wine.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Get all reviews for the wine (you might want to add pagination later)
    reviews = wine.reviews.filter(approved=True).order_by('-created_at')


    context = {
        'wine': wine,
        'average_rating': round(average_rating, 1),  # Rounded to 1 decimal
        'reviews': reviews,
        'review_form': review_form,
        'existing_review': existing_review,
    }
    return render(request, 'product_details.html', context)


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
    if review.user == request.user:
        review.delete()
        messages.success(request, 'Your review has been deleted.')
        print("Review deleted successfully")
    else:
        messages.error(request, 'You can only delete your own reviews.')
        print("Error: Review delete failed - not user's review")

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
        return redirect('product_details', wine_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.wine = wine
            review.approved = False
            review.save()
            messages.success(request, 'Your review has been updated.')
            print("Review edited successfully")
            return redirect('product_details', wine_id)
        else:
            messages.error(request, "Error, unable to update review.")
            print("Error: Failed to edit review")

    return HttpResponseRedirect(reverse('product_details', args=[wine_id]))
