from decimal import Decimal
from time import sleep

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from products.models import Wine, Category
from reviews.models import Review


class ReviewModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up initial test data for the entire test case.
        """
        # Create a Category and a Wine instance for the reviews
        cls.category = Category.objects.create(name='Test Category')
        cls.wine = Wine.objects.create(
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
            category=cls.category
        )

        # Create a User instance for the reviews
        cls.user = User.objects.create_user(
            username='testuser', password='12345')

    def test_create_review(self):
        """
        Test creating a valid review for a wine.
        """
        review = Review.objects.create(
            wine=self.wine,
            user=self.user,
            rating=5,
            comment="Great wine!",
            approved=True
        )
        self.assertEqual(review.wine, self.wine)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great wine!")
        self.assertTrue(review.approved)

    def test_rating_out_of_range(self):
        """
        Test that a rating outside the valid range
        (1-5) raises a ValidationError.
        """
        # Invalid rating
        review = Review(wine=self.wine, user=self.user, rating=6)
        with self.assertRaises(ValidationError):
            review.full_clean()  # This triggers model validation

        review.rating = 0  # Another invalid rating
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_approved_default_value(self):
        """
        Test that the default value of the approved field is False.
        """
        review = Review.objects.create(
            wine=self.wine, user=self.user, rating=3)
        self.assertFalse(review.approved)

    def test_created_at_and_updated_at(self):
        """
        Test that created_at and updated_at fields are set correctly.
        """
        review = Review.objects.create(
            wine=self.wine, user=self.user, rating=4)
        self.assertIsNotNone(review.created_at)
        self.assertIsNotNone(review.updated_at)

        # Update the review to test the updated_at field
        sleep(1)  # Ensure enough time passes for a visible change in timestamp
        review.comment = "Updated comment"
        review.save()  # This should trigger an update
        self.assertNotEqual(review.created_at, review.updated_at)

    def test_review_ordering(self):
        """
        Test that reviews are ordered by
        their creation date in descending order.
        """
        review1 = Review.objects.create(
            wine=self.wine, user=self.user, rating=4)
        sleep(1)  # Delay to differentiate the timestamps
        review2 = Review.objects.create(
            wine=self.wine, user=self.user, rating=5)
        reviews = Review.objects.all()
        self.assertEqual(reviews[0].id, review2.id)  # Latest review first
        self.assertEqual(reviews[1].id, review1.id)  # Older review second
