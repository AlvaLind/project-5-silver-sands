import re
from decimal import Decimal, InvalidOperation

from django import forms
from django.core.exceptions import ValidationError

from .widgets import CustomClearableFileInput
from checkout.models import Order
from products.models import Wine, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Wine
        fields = '__all__'

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        self.fields['category'].choices = (
            [(category.id, category.name) for category in categories])

        # Adding CSS classes to fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

        # Ensure certain fields are required
        self.fields['name'].required = True
        self.fields['description'].required = True
        self.fields['price'].required = True
        self.fields['vintage'].required = True
        self.fields['volume'].required = True
        self.fields['closure'].required = True
        self.fields['stock'].required = True
        
        # Customize error messages for required fields overwrite html5
        self.fields['name'].error_messages = {
            'required': 'Name is required.'
        }
        self.fields['description'].error_messages = {
            'required': 'Description is required.'
        }
        self.fields['price'].error_messages = {
            'required': 'Price is required.'
        }
        self.fields['vintage'].error_messages = {
            'required': 'Vintage is required.'
        }
        self.fields['volume'].error_messages = {
            'required': 'Volume is required.'
        }
        self.fields['closure'].error_messages = {
            'required': 'Closure is required.'
        }
        self.fields['stock'].error_messages = {
            'required': 'Stock is required.'
        }

        if self.instance.pk:  # Check if the instance exists (is being edited)
            self.fields['slug'].widget.attrs['readonly'] = True
            self.fields['slug'].help_text = (
                "This slug is auto-generated from the wine name and \
                cannot be changed.")
            self.fields['rating'].widget.attrs['readonly'] = True
            self.fields['rating'].help_text = "This rating is \
                auto-generated based on the reviews and cannot be changed."
        else:  # For new instances
            self.fields['slug'].widget.attrs['readonly'] = True
            self.fields['slug'].help_text = "This slug will be \
                auto-generated based on the wine name."
            self.fields['rating'].widget.attrs['readonly'] = True
            self.fields['rating'].help_text = "This rating will be \
                auto-generated based on the reviews."

    def clean_name(self):
        """
        Name must not be empty and name length to be between 3 and 50
        characters. Name can only contain letters, numbers and spaces
        no special characters
        """

        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Name is required.')
        if len(name) > 50:
            raise ValidationError('Name cannot exceed 50 characters.')
        if not re.match(r"^[a-zA-Z0-9\s]*$", name):
            raise ValidationError(
                'Name must contain only letters, numbers and spaces.')
        return name

    def clean_sku(self):
        """
        Sku cannot be greater than 254 characters in length
        """

        sku = self.cleaned_data.get('sku')
        if sku and len(sku) > 254:
            raise ValidationError('SKU cannot exceed 254 characters.')
        return sku

    def clean_description(self):
        """
        Description cannot be empty
        """

        description = self.cleaned_data.get('description')
        if not description:
            raise ValidationError('Description is required.')
        return description

    def clean_price(self):
        """
        Price cannot be empty, must be greater than 0 and must be a number.
        Price will be stored with 2 decimal places if whole number is entered
        """

        price = self.cleaned_data.get('price')
        if not price:
            raise ValidationError('Price is required.')

        try:
            price = Decimal(price)
        except InvalidOperation:
            raise ValidationError('Price must be a valid number.')
        if price <= 0:
            raise ValidationError('Price must be greater than $0.')
        if not re.match(r'^\d+(\.\d{1,2})?$', str(price)):
            raise ValidationError('Price must be a valid decimal \
                number with a max. of two decimal places.')

        return price

    def clean_vintage(self):
        """
        Vintage cannot be empty and must be between 1900 and 2100
        """

        vintage = self.cleaned_data.get('vintage')
        if vintage is None:
            raise ValidationError('Vintage is required.')
        if vintage < 1900 or vintage > 2100:
            raise ValidationError('Vintage must be between the year \
                1900 and 2100.')
        return vintage

    def clean_volume(self):
        """
        Volume cannot be empty and must be between 0 - 5000 ml
        """

        volume = self.cleaned_data.get('volume')
        if volume is None:
            raise ValidationError('Volume is required.')
        if volume <= 0 or volume > 5000:
            raise ValidationError('Volume must be between 0 and 5000 ml.')
        return volume

    def clean_closure(self):
        """
        Closure cannot be empty
        """

        closure = self.cleaned_data.get('closure')
        if not closure:
            raise ValidationError('Closure is required.')
        return closure

    def clean_abv(self):
        """
        Abv must be between 0 - 100 as it is a percentage
        """

        abv = self.cleaned_data.get('abv')
        if abv < 0 or abv > 100:
            raise ValidationError('ABV must be between 0 and 100 percent.')
        return abv

    def clean_acidity(self):
        """
        Acidity must be between 0 - 14, the ph scale
        """

        acidity = self.cleaned_data.get('acidity')
        if acidity and (acidity < 0 or acidity > 14):
            raise ValidationError('Acidity must be between ph 0 and 14.')
        return acidity

    def clean_residual_sugar(self):
        """
        Residual sugar must be greater than 0
        """

        residual_sugar = self.cleaned_data.get('residual_sugar')
        if residual_sugar and (residual_sugar < 0):
            raise ValidationError('Residual sugar cannot be negative.')
        return residual_sugar

    def clean_stock(self):
        """
        Ensure stock is not empty and is between 0 - 99,999
        """

        stock = self.cleaned_data.get('stock')
        if stock is None:
            raise ValidationError('Stock is required.')
        if stock < 0:
            raise ValidationError('Stock cannot be negative.')
        if stock > 99999:
            raise ValidationError('Stock exceeds the max limit of 99,999.')
        return stock

    def clean_slug(self):
        """
        Slug and therefore name must be unique
        """

        slug = self.cleaned_data.get('slug')
        instance = self.instance

        # Check if Wine with this slug exists, excluding current instance
        if Wine.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            raise ValidationError('This Name is already in use. \
                Please choose a different one.')

        return slug


class OrderStatusForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Order.ORDER_STATUS_CHOICES),
        }
