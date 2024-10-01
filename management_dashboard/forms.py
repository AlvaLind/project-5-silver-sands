from django import forms
from .widgets import CustomClearableFileInput
from products.models import Wine, Category
from django.core.exceptions import ValidationError

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
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        # Get the instance (if exists) to exclude it from validation
        instance = self.instance
        
        # Check if a Wine with this slug already exists, excluding the current instance
        if Wine.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            raise ValidationError('This slug is already in use. Please choose a different one.')
        
        return slug
