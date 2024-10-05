from django.shortcuts import render

def home(request):
    """ A view to return the home page """
    
    return render(request, 'home/index.html', {'show_signup_form': True})


def about_us(request):
    """ A view to return the about us or our story page """
    
    return render(request, 'home/about_us.html', {'show_signup_form': True})


def access_denied(request):
    """A view to return access denied page"""
    
    return render(request, 'home/access_denied.html')

def visit_us(request):
    """A view to return visit us page"""
    
    return render(request, 'home/visit_us.html', {'show_signup_form': True})
