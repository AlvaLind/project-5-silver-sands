from django import forms
from products.models import Wine, Category
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Wine
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        self.fields['category'].choices = [(category.id, category.name) for category in categories]
        
        # Adding CSS classes to fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
    
    def clean_slug(self):  # Assuming 'slug' is the name of your slug field
        slug = self.cleaned_data.get('slug')
        if Wine.objects.filter(slug=slug).exists():  # Check if the slug already exists
            raise ValidationError('This slug already exists. Please choose a different one.')
        return slug
