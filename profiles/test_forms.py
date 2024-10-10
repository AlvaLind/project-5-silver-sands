from django import forms
from django.test import TestCase
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfileFormTest(TestCase):
    def setUp(self):
        """
        Set up test data for the UserProfileForm tests.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.profile_data = {
            'default_full_name': 'Test User',
            'default_phone_number': '1234567890',
            'default_postcode': '12345',
            'default_town_or_city': 'Test City',
            'default_street_address1': '123 Test St',
            'default_street_address2': '',
            'default_county': 'Test County',
            'default_country': 'GB',
        }

    def test_user_profile_form_valid(self):
        """
        Test that the form is valid with correct data.
        """
        form = UserProfileForm(data=self.profile_data)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_invalid_empty_full_name(self):
        """
        Test that form is invalid if full name is empty.
        """
        data = self.profile_data.copy()
        data['default_full_name'] = ''
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_full_name', form.errors)

    def test_user_profile_form_invalid_too_long_full_name(self):
        """
        Test that form is invalid if full name exceeds 40 characters.
        """
        data = self.profile_data.copy()
        data['default_full_name'] = 'T' * 41  # 41 characters
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_full_name', form.errors)

    def test_user_profile_form_invalid_empty_phone_number(self):
        """
        Test that form is invalid if phone number is empty.
        """
        data = self.profile_data.copy()
        data['default_phone_number'] = ''
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_phone_number', form.errors)

    def test_user_profile_form_invalid_non_numeric_phone_number(self):
        """
        Test that form is invalid if phone number is non-numeric.
        """
        data = self.profile_data.copy()
        data['default_phone_number'] = 'abc123'
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_phone_number', form.errors)

    def test_user_profile_form_invalid_too_long_phone_number(self):
        """
        Test that form is invalid if phone number exceeds 15 digits.
        """
        data = self.profile_data.copy()
        data['default_phone_number'] = '1' * 16  # 16 digits
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_phone_number', form.errors)

    def test_user_profile_form_invalid_non_numeric_postcode(self):
        """
        Test that form is invalid if postal code is non-numeric.
        """
        data = self.profile_data.copy()
        data['default_postcode'] = 'abc123'
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_postcode', form.errors)

    def test_user_profile_form_invalid_too_long_postcode(self):
        """
        Test that form is invalid if postal code exceeds 10 digits.
        """
        data = self.profile_data.copy()
        data['default_postcode'] = '1' * 11  # 11 digits
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_postcode', form.errors)

    def test_user_profile_form_invalid_empty_street_address1(self):
        """
        Test that form is invalid if street address 1 is empty.
        """
        data = self.profile_data.copy()
        data['default_street_address1'] = ''
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_street_address1', form.errors)

    def test_user_profile_form_invalid_too_long_street_address1(self):
        """
        Test that form is invalid if street address 1 exceeds 50 characters.
        """
        data = self.profile_data.copy()
        data['default_street_address1'] = 'A' * 51  # 51 characters
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_street_address1', form.errors)

    def test_user_profile_form_invalid_empty_county(self):
        """
        Test that form is invalid if county is empty.
        """
        data = self.profile_data.copy()
        data['default_county'] = ''
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_county', form.errors)

    def test_user_profile_form_invalid_too_long_county(self):
        """
        Test that form is invalid if county exceeds 40 characters.
        """
        data = self.profile_data.copy()
        data['default_county'] = 'C' * 41  # 41 characters
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_county', form.errors)

    def test_user_profile_form_invalid_empty_town_or_city(self):
        """
        Test that form is invalid if town or city is empty.
        """
        data = self.profile_data.copy()
        data['default_town_or_city'] = ''
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_town_or_city', form.errors)

    def test_user_profile_form_invalid_too_long_town_or_city(self):
        """
        Test that form is invalid if town or city exceeds 40 characters.
        """
        data = self.profile_data.copy()
        data['default_town_or_city'] = 'T' * 41  # 41 characters
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_town_or_city', form.errors)

    def test_user_profile_form_invalid_street_address2_too_long(self):
        """
        Test that form is invalid if street address 2 exceeds 50 characters.
        """
        data = self.profile_data.copy()
        data['default_street_address2'] = 'A' * 51  # 51 characters
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('default_street_address2', form.errors)
