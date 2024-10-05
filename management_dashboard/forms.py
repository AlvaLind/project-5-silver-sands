from django import forms
from django.core.exceptions import ValidationError

from .widgets import CustomClearableFileInput
from products.models import Wine, Category
from checkout.models import Order


class ProductForm(forms.ModelForm):

    class Meta:
        model = Wine
        fields = '__all__'
        
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput())
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        self.fields['category'].choices = [(category.id, category.name) for category in categories]
        
        # Adding CSS classes to fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
            
        if self.instance.pk:  # Check if the instance exists (is being edited)
            self.fields['slug'].widget.attrs['readonly'] = True
            self.fields['slug'].help_text = "This slug is auto-generated from the wine name and cannot be changed."
            self.fields['rating'].widget.attrs['readonly'] = True
            self.fields['rating'].help_text = "This rating is auto-generated based on the reviews and cannot be changed."
        else:  # For new instances
            self.fields['slug'].widget.attrs['readonly'] = True
            self.fields['slug'].help_text = "This slug will be auto-generated based on the wine name."
            self.fields['rating'].widget.attrs['readonly'] = True
            self.fields['rating'].help_text = "This rating will be auto-generated based on the reviews."
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        # Get the instance (if exists) to exclude it from validation
        instance = self.instance
        
        # Check if a Wine with this slug already exists, excluding the current instance
        if Wine.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            raise ValidationError('This slug is already in use. Please choose a different one.')
        
        return slug


class OrderStatusForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Order.ORDER_STATUS_CHOICES),
        }