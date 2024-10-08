import re

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

        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
        
            # Add 'is-invalid' class if there are errors for this field
            if self.errors.get(field):
                self.fields[field].widget.attrs['class'] += ' is-invalid'
            
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
        """ 
        Validate the email field.
        It must not be empty and must be between 6 - 100 characters.
        Must match a valid email format.
        """
        
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required.')
        if len(email) < 6 or len(email) > 100:
            raise ValidationError('Email must be between 6 and 100 characters.')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Enter a valid email address.')
        return email
    
    # Form field validations 
    def clean_full_name(self):
        """ 
        Validate the full name field.
        It must not be empty and must not exceed 40 characters.
        Must only contain letters, spaces, apostrophes and hyphens.
        """
        
        full_name = self.cleaned_data.get('full_name')
        if not full_name:
            print("Full Name is required")
            raise ValidationError('Full Name is required.')
        if len(full_name) > 40:
            raise ValidationError('Full Name must be no longer than 40 characters.')
        if not re.match(r"^[a-zA-Z\s'–-]+$", full_name):
            raise ValidationError('Full Name must contain only letters and spaces.')
        return full_name

    def clean_phone_number(self):
        """ 
        Validate the phone number.
        It must not be empty and must be numeric.
        Must be between 7 and 15 digits long, and 
        """
        
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('Phone number is required.')
        if not phone_number.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        if len(phone_number) < 7 or len(phone_number) > 15:
            raise ValidationError('Phone number must be between 7 and 15 digits long.')
        return phone_number

    def clean_postcode(self):
        """ 
        Validate the postal code.
        It must not be empty and must be numeric.
        It must be between 4 - 10 digits long.
        """
        
        postcode = self.cleaned_data.get('postcode')
        if not postcode:
            raise ValidationError('Postal Code is required.')
        if not postcode.isdigit():
            raise forms.ValidationError('Postal code must contain only digits.')
        if len(postcode) < 4 or len(postcode) > 10:
            raise ValidationError('Postal code must be between 4 and 10 digits long.')
        return postcode
    
    def clean_street_address1(self):
        """ 
        Validate the first street address.
        It must not be empty and must not exceed 50 characters.
        Must not contain special characters.
        """
        
        street_address1 = self.cleaned_data.get('street_address1')
        if not street_address1:
            raise ValidationError('Street Address 1 is required.')
        if len(street_address1) > 50:
            raise ValidationError('Street Address 1 must be no longer than 50 characters.')
        if not re.match(r'^[a-zA-Z0-9\s,.-/&]*$', street_address1):
            raise ValidationError('Street Address 1 can only contain letters, numbers, spaces, and limited punctuation.')
        return street_address1
    
    def clean_street_address2(self):
        """ 
        Validate the second street address.
        It must not exceed 50 characters.
        Must not contain special characters.
        """
        
        street_address2 = self.cleaned_data.get('street_address2')
        if street_address2:
            if street_address2 and len(street_address2) > 50:
                raise ValidationError('Street Address 2 must be no longer than 50 characters.')
            if not re.match(r'^[a-zA-Z0-9\s,.-/&]*$', street_address2):
                raise ValidationError('Street Address 2 can only contain letters, numbers, spaces, and limited punctuation.')
        return street_address2
    
    def clean_county(self):
        """ 
        Validate the county/state/locality field.
        It must not be empty or exceed 40 characters.
        Can only contain letters and spaces.
        """
        
        county = self.cleaned_data.get('county')
        if not county:
            raise ValidationError('County or State is required.')
        if county and len(county) > 40:
            raise ValidationError('County, State or Locality must be no longer than 40 characters.')
        if not re.match(r'^[a-zA-Z\s]+$', county):
            raise ValidationError('County or State must contain only letters and spaces.')
        return county
    
    def clean_town_or_city(self):
        """ 
        Validate the town/city field.
        It must not be empty and cannot exceed 40 characters.
        Can only contain letters and spaces.
        """
        
        town_or_city = self.cleaned_data.get('town_or_city')
        if not town_or_city:
            raise ValidationError('Town or City is required.')
        if town_or_city and len(town_or_city) > 40:
            raise ValidationError('Town or City must be no longer than 40 characters.')
        if not re.match(r'^[a-zA-Z\s]+$', town_or_city):
            raise ValidationError('Town or City must contain only letters and spaces.')
        return town_or_city
