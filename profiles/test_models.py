from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Wine, Category
from .models import UserProfile, Favourite
from django.utils import timezone


class UserProfileModelTest(TestCase):
    def setUp(self):
        """Create a user and a corresponding UserProfile for testing."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = UserProfile.objects.get(user=self.user)

    def test_user_profile_creation(self):
        """Test that a UserProfile is created with a User."""
        self.assertIsInstance(self.profile, UserProfile)
        self.assertEqual(self.profile.user.username, 'testuser')

    def test_user_profile_str(self):
        """Test the string representation of the UserProfile."""
        self.assertEqual(str(self.profile), 'testuser')

    def test_default_full_name(self):
        """Test the default full name field."""
        self.profile.default_full_name = 'John Doe'
        self.profile.save()
        self.assertEqual(self.profile.default_full_name, 'John Doe')


class FavouriteModelTest(TestCase):
    def setUp(self):
        """Create a user, wine, and a Favourite for testing."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.wine = Wine.objects.create(
            name='Test Wine',
            sku='TW001',
            slug='test-wine',
            description='A fine test wine.',
            price=10.00,
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
        self.favourite = Favourite.objects.create(user=self.user, wine=self.wine)

    def test_favourite_creation(self):
        """Test that a Favourite is created correctly."""
        self.assertIsInstance(self.favourite, Favourite)
        self.assertEqual(self.favourite.user.username, 'testuser')
        self.assertEqual(self.favourite.wine.name, 'Test Wine')

    def test_favourite_str(self):
        """Test the string representation of the Favourite."""
        self.assertEqual(str(self.favourite), 'testuser favourited Test Wine')

    def test_unique_favourite(self):
        """Test that a user can only favourite the same wine once."""
        with self.assertRaises(Exception):
            Favourite.objects.create(user=self.user, wine=self.wine)

    def test_favourite_added_on(self):
        """Test that the added_on field is set correctly."""
        self.assertIsInstance(self.favourite.added_on, timezone.datetime)
        self.assertTrue(self.favourite.added_on <= timezone.now())
