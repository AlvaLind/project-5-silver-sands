from django import forms
from django.core.exceptions import ValidationError

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'default_full_name': 'Full Name',
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs.update({
                'class': 'border-black rounded-0 profile-form-input'
            })
            self.fields[field].label = False

    def clean_default_full_name(self):
        """
        Validate the full name field.
        It must not be empty and must not exceed 40 characters.
        """
        full_name = self.cleaned_data.get('default_full_name')

        # Check for empty value
        if not full_name:
            raise ValidationError('Full Name is required.')

        # Check length
        if len(full_name) > 40:
            raise ValidationError('Full Name must be no longer \
                than 40 characters.')

        return full_name

    def clean_default_phone_number(self):
        """
        Validate the phone number.
        It must not be empty and must be numeric and no longer than 15 digits.
        """
        phone_number = self.cleaned_data.get('default_phone_number')

        # Check for empty value
        if not phone_number:
            raise ValidationError('Phone number is required.')

        # Check if phone number is numeric
        if not phone_number.isdigit():
            raise ValidationError('Phone number must be numeric.')

        # Check length
        if len(phone_number) > 15:
            raise ValidationError('Phone number must be no longer \
                than 15 digits.')

        return phone_number

    def clean_default_postcode(self):
        """
        Validate the postal code.
        It must not be empty and must be numeric and no longer than 10 digits.
        """
        postcode = self.cleaned_data.get('default_postcode')

        # Check for empty value
        if not postcode:
            raise ValidationError('Postal Code is required.')

        # Check if postcode is numeric
        if not postcode.isdigit():
            raise ValidationError('Postal code must be numeric.')

        # Check length
        if len(postcode) > 10:
            raise ValidationError('Postal code must be no longer \
                than 10 digits.')

        return postcode

    def clean_default_street_address1(self):
        """
        Validate the first street address.
        It must not be empty and must not exceed 50 characters.
        """
        street_address1 = self.cleaned_data.get('default_street_address1')

        # Check for empty value
        if not street_address1:
            raise ValidationError('Street Address 1 is required.')

        # Check length
        if len(street_address1) > 50:
            raise ValidationError('Street Address 1 must be no longer \
                than 50 characters.')

        return street_address1

    def clean_default_street_address2(self):
        """
        Validate the second street address.
        It must not exceed 50 characters.
        """
        street_address2 = self.cleaned_data.get('default_street_address2')

        # Check length
        if street_address2 and len(street_address2) > 50:
            raise ValidationError('Street Address 2 must be no longer \
                than 50 characters.')

        return street_address2

    def clean_default_county(self):
        """
        Validate the county/state/locality field.
        It must not be empty or exceed 40 characters.
        """
        county = self.cleaned_data.get('default_county')

        # Check for empty value
        if not county:
            raise ValidationError('County or State is required.')

        # Check length
        if county and len(county) > 40:
            raise ValidationError('County, State or Locality must be no \
                longer than 40 characters.')

        return county

    def clean_default_town_or_city(self):
        """
        Validate the town/city field.
        It must not be empty and cannot exceed 40 characters.
        """
        town_or_city = self.cleaned_data.get('default_town_or_city')

        # Check for empty value
        if not town_or_city:
            raise ValidationError('Town or City is required.')

        # Check length
        if town_or_city and len(town_or_city) > 40:
            raise ValidationError('Town or City must be no longer \
                than 40 characters.')

        return town_or_city
