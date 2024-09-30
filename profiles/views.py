from django.shortcuts import render
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm


def profile(request):
    """ Display the user's profile. """
    
    user_profile = UserProfile.objects.get(user=request.user)
     
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            
    form = UserProfileForm(instance=user_profile)
    orders = user_profile.orders.all()

    template = 'profiles/profile.html'
    context = {
            'form': form,
            'orders': orders,
            'on_profile_page': True
        }
    
    return render(request, template, context)
