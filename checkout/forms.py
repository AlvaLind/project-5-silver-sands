from django import forms
from django.core.exceptions import ValidationError
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on the first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }
        
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field not in ['country', 'phone_number', 'postcode', 'email']:
                self.fields[field].widget.attrs['maxlength'] = '60'

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
            
        self.fields['phone_number'].widget.attrs.update({
            'pattern': '[0-9]*',
            'inputmode': 'numeric',
            'maxlength': '15',
            'minlength': '7',
        })
        self.fields['postcode'].widget.attrs.update({
            'pattern': '[0-9]*',
            'inputmode': 'numeric',
            'maxlength': '10',
            'minlength': '4',
        })
        self.fields['country'].widget.attrs['class'] = 'form-control'
        
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Example: Validate minimum length for email
        if len(email) < 6:
            raise forms.ValidationError("Email is too short. Please enter a valid email address.")
        
        if len(email) > 100:
            raise forms.ValidationError("Email cannot be longer than 100 characters. Please enter a shorter email address.")

        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Check for numeric input
        if not phone_number.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')

        # Check length requirements
        if len(phone_number) < 7:
            raise forms.ValidationError('Phone number must be at least 7 digits long.')
        if len(phone_number) > 15:
            raise forms.ValidationError('Phone number cannot be longer than 15 digits.')

        return phone_number

    def clean_postcode(self):
        postcode = self.cleaned_data.get('postcode')

        if not postcode.isdigit():
            raise forms.ValidationError('Postal code must contain only digits.')

        if len(postcode) < 4:
            raise forms.ValidationError('Postal code must be at least 4 digits long.')
        if len(postcode) > 10:
            raise forms.ValidationError('Postal code cannot be longer than 10 digits.')

        return postcode
