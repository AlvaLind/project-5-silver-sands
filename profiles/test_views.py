import uuid
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Favourite
from checkout.models import Order, OrderLineItem
from products.models import Wine, Category


class ProfilesViewsTest(TestCase):
    def setUp(self):
        """Set up test data for the Profiles views tests."""
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create a user profile
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)

        # Create a test category
        self.category = Category.objects.create(name='Test Category')

        # Create a test wine associated with the category
        self.wine1 = Wine.objects.create(
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

        # Create an order for the user profile
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='Test User',
            email='testuser@example.com',
            phone_number='1234567890',
            country='GB',  # Example country code
            postcode='AB12 3CD',
            town_or_city='Test City',
            street_address1='123 Test St',
            street_address2='Apt 1',
            county='Test County',
            delivery_cost=Decimal('5.00'),  # Example delivery cost
            order_total=Decimal('10.00'),  # Example order total
            grand_total=Decimal('15.00'),  # Example grand total
            original_bag='{}',  # Example JSON or string representation of the order's bag
            stripe_pid='test_stripe_pid',  # Example Stripe payment ID
        )

        # Create an order line item associated with the order
        OrderLineItem.objects.create(
            order=self.order,
            wine=self.wine1,
            quantity=1  # Assuming one item in the order
        )

        # Log in the user
        self.client.login(username='testuser', password='password123')

    def test_profile_view(self):
        """Test the profile view for logged-in users."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_order_history_view(self):
        """Test the order history view."""
        response = self.client.get(reverse('order_history', args=[self.order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')

    def test_add_to_favourites(self):
        """Test adding a wine to favourites."""
        response = self.client.post(reverse('add_to_favourites', args=[self.wine1.id]), follow=True)
        self.assertEqual(response.status_code, 200)  # Check for successful redirect
        self.assertTrue(Favourite.objects.filter(user=self.user, wine=self.wine1).exists())
        self.assertContains(response, f'{self.wine1.name} has been added to your favourites')

    def test_favourites_view(self):
        """Test the favourites view."""
        Favourite.objects.create(user=self.user, wine=self.wine1)
        response = self.client.get(reverse('favourites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/favourites.html')
        self.assertContains(response, self.wine1.name)

    def tearDown(self):
        """Clean up after tests."""
        self.user.delete()
        self.category.delete()
        self.wine1.delete()
        self.order.delete()
