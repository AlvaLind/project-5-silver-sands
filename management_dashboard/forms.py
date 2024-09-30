from django import forms
from products.models import Wine, Category


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Wine
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        self.fields['category'].choices = [(category.id, category.name) for category in categories]
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
