from django.shortcuts import render

# Create your views here.
def home(request):
    """ A view to return the home page """
    
    return render(request, 'home/index.html')


def about_us(request):
    """ A view to return the about us or our story page """
    
    return render(request, 'home/about_us.html')


def access_denied(request):
    """A view to return access denied page"""
    
    return render(request, 'home/access_denied.html')
