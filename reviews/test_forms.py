from decimal import Decimal

from django import forms
from django.contrib.auth.models import User
from django.test import TestCase

from .forms import ReviewForm
from .models import Review
from products.models import Wine, Category


class ReviewFormTest(TestCase):
    def setUp(self):
        """Set up test data for the ReviewForm tests."""
        # Create a test category
        self.category = Category.objects.create(name='Test Category')

        # Create a test wine instance
        self.wine = Wine.objects.create(
            name='Test Wine',
            sku='TW001',
            slug='test-wine',
            description='A fine test wine.',
            price=Decimal('10.00'),
            vintage=2020,
            volume=750,
            closure='natural cork',
            abv=13.5,
            acidity=5.0,
            residual_sugar=3.0,
            stock=10,
            available=True,
            category=self.category
        )

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='12345')

    def test_review_form_valid(self):
        """Test that the form is valid with correct data."""
        form_data = {
            'rating': 5,
            'comment': 'This wine is amazing!'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form_invalid_rating(self):
        """Test that the form raises a validation error for invalid rating."""
        form_data = {
            'rating': 6,  # Invalid rating
            'comment': 'This wine is amazing!'
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_review_form_rating_boundaries(self):
        """Test that the form raises a validation error for ratings below 1."""
        form_data = {
            'rating': 0,  # Invalid rating
            'comment': 'This wine is terrible!'
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

        form_data['rating'] = 1  # Valid rating
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form_invalid_comment_length(self):
        """Test that the form can handle a comment that is too long."""
        long_comment = 'a' * 151  # Exceeding the max length of 150
        form_data = {
            'rating': 5,
            'comment': long_comment
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors)

    def test_review_form_clean_rating(self):
        """Test the clean_rating method to ensure rating validation works."""
        form_data = {'rating': 3, 'comment': 'Good wine!'}
        form = ReviewForm(data=form_data)
        form.is_valid()  # Call is_valid() before accessing cleaned_data
        self.assertEqual(form.cleaned_data['rating'], 3)

    def test_review_form_clean_rating_boundary(self):
        """Test clean_rating with edge cases."""
        # Test rating below the valid range
        form_data = {'rating': 0, 'comment': 'Invalid rating'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())  # Should be invalid
        self.assertIn('rating', form.errors)  # Check error for 'rating'

        # Test rating above the valid range
        form_data['rating'] = 6  # Invalid rating
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())  # Should be invalid
        self.assertIn('rating', form.errors)  # Check for error for 'rating'

        # Test valid rating on the boundary
        form_data['rating'] = 1  # Valid rating
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())  # Should be valid
        self.assertEqual(form.cleaned_data['rating'], 1)

        form_data['rating'] = 5  # Valid rating at upper boundary
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())  # Should be valid
        self.assertEqual(form.cleaned_data['rating'], 5)
