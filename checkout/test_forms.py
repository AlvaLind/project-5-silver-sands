from django.test import TestCase
from .forms import OrderForm


class OrderFormTest(TestCase):

    def test_valid_form(self):
        """
        Test that a valid form is accepted.
        """
        form_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Main St',
            'street_address2': 'Apt 4B',
            'town_or_city': 'Anytown',
            'postcode': '12345',
            'country': 'AU',
            'county': 'Adelaide',
        }
        form = OrderForm(data=form_data)
        if not form.is_valid():
            print(form.errors) 
        self.assertTrue(form.is_valid())
        
    def test_invalid_email(self):
        """
        Test that an invalid email raises an error.
        """
        form_data = {
            'full_name': 'John Doe',
            'email': 'invalid-email',
            'phone_number': '1234567890',
            'street_address1': '123 Main St',
            'street_address2': 'Apt 4B',
            'town_or_city': 'Anytown',
            'postcode': '12345',
            'country': 'AU',
            'county': 'Adelaide',
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
    def test_invalid_street_address(self):
        """
        Test that street address cannot contain special characters.
        """
        form_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Main St #1',
            'street_address2': 'Apt 4B',
            'town_or_city': 'Anytown',
            'postcode': '12345',
            'country': 'AU',
            'county': 'Adelaide',
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('street_address1', form.errors)
        
    def test_full_name_required(self):
        """
        Test that full name is required.
        """
        form_data = {
            'full_name': '',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Main St',
            'street_address2': 'Apt 4B',
            'town_or_city': 'Anytown',
            'postcode': '12345',
            'country': 'AU',
            'county': 'Adelaide',
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        
    def test_email_required(self):
        """
        Test that email is required.
        """
        form_data = {
            'full_name': 'John Doe',
            'email': '',
            'phone_number': '1234567890',
            'street_address1': '123 Main St',
            'street_address2': 'Apt 4B',
            'town_or_city': 'Anytown',
            'postcode': '12345',
            'country': 'AU',
            'county': 'Adelaide',
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
                
    def test_full_name_length(self):
        """
        Test that full name cannot exceed 40 characters.
        """
        form_data = {
            'full_name': 'A' * 41,
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Main St',
            'street_address2': 'Apt 4B',
            'town_or_city': 'Anytown',
            'postcode': '12345',
            'country': 'AU',
            'county': 'Adelaide',
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        
    def test_street_address1_length(self):
        """
        Test that street address 1 cannot exceed 50 characters.
        """
        form_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'street_address1': 'A' * 51,
            'street_address2': 'Apt 4B',
            'town_or_city': 'Anytown',
            'postcode': '12345',
            'country': 'AU',
            'county': 'Adelaide',
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('street_address1', form.errors)
