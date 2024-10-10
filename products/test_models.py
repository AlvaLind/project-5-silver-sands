from decimal import Decimal

from django.test import TestCase
from django.core.exceptions import ValidationError

from products.models import Category, Wine


class CategoryModelTest(TestCase):
    """
    Tests for the Category model.
    """

    def setUp(self):
        """
        Create a Category instance for testing.
        """
        self.category = Category.objects.create(
            name='Test Category',
            description='A category for testing wines.'
        )

    def test_category_unique_name(self):
        """
        Test that creating a Category with a duplicate name raises an error.
        """
        # Attempt to create a new instance with the same name
        duplicate_category = Category(name='Test Category')  # Same name

        # Check that full_clean raises a ValidationError
        with self.assertRaises(ValidationError):
            duplicate_category.full_clean()


class WineModelTest(TestCase):
    """
    Tests for the Wine model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a Category and Wine instance for testing.
        """
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

    def test_slug_generation(self):
        """
        Test that the slug is generated correctly.
        """
        wine = Wine(
            name='New Wine Name',
            category=self.category,
            description='A new fine test wine.',
            price=Decimal('12.00'),
            vintage=2021,
            volume=750,
            closure='natural cork',
            abv=13.5,
            acidity=5.0,
            residual_sugar=3.0,
            stock=15,
        )
        wine.save()
        self.assertEqual(wine.slug, 'new-wine-name')

    def test_unique_slug_validation(self):
        """
        Test that saving a Wine with a non-unique slug raises an error.
        """
        Wine.objects.create(
            name='Unique Wine',
            category=self.category,
            sku='UW001',
            slug='unique-wine',
            description='A unique wine.',
            price=Decimal('10.00'),
            vintage=2021,
            volume=750,
            closure='screw cap',
            abv=12.0,
            acidity=4.0,
            residual_sugar=2.0,
            stock=20,
        )

        # Attempt to create a wine with a duplicate slug
        duplicate_wine = Wine(
            name='Duplicate Wine',
            category=self.category,
            sku='DW001',
            slug='unique-wine',  # Same slug as the existing wine
            description='This wine should not be created.',
            price=Decimal('20.00'),
            vintage=2022,
            volume=750,
            closure='natural cork',
            abv=13.5,
            acidity=5.0,
            residual_sugar=3.0,
            stock=10,
        )

        with self.assertRaises(ValidationError):
            duplicate_wine.full_clean()

    def test_wine_creation_with_blank_slug(self):
        """
        Test that a Wine can be created without
        providing a slug, and it generates one.
        """
        wine = Wine(
            name='Blank Slug Wine',
            category=self.category,
            description='This wine should generate a slug.',
            price=Decimal('10.00'),
            vintage=2021,
            volume=750,
            closure='natural cork',
            abv=13.5,
            acidity=5.0,
            residual_sugar=3.0,
            stock=10,
        )
        wine.save()
        self.assertEqual(wine.slug, 'blank-slug-wine')
