from django.test import TestCase
from django.core.exceptions import ValidationError

from .forms import ProductForm, OrderStatusForm
from products.models import Wine, Category
from checkout.models import Order


class ProductFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Create a category to be used for Wine instances
        """
        cls.category = Category.objects.create(name="Test Category")

    def test_valid_product_form(self):
        """
        Test valid ProductForm submission
        """
        form_data = {
            'name': 'Test Wine',
            'sku': 'TW001',
            'slug': 'test-wine',
            'description': 'A fine test wine.',
            'price': '10.00',
            'vintage': 2020,
            'volume': 750,
            'closure': 'natural cork',
            'abv': 13.5,
            'acidity': 5.0,
            'residual_sugar': 3.0,
            'stock': 10,
            'category': self.category.id,
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_product_form_empty_name(self):
        """
        Test ProductForm validation for empty name
        """
        form_data = {
            'name': '',
            'sku': 'TW001',
            'slug': 'test-wine',
            'description': 'A fine test wine.',
            'price': '10.00',
            'vintage': 2020,
            'volume': 750,
            'closure': 'natural cork',
            'abv': 13.5,
            'acidity': 5.0,
            'residual_sugar': 3.0,
            'stock': 10,
            'category': self.category.id,
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ['Name is required.'])

    def test_invalid_product_form_name_too_long(self):
        """
        Test the ProductForm for name exceeding max length.
        """
        form_data = {
            'name': 'A' * 51,
            'sku': 'TW001',
            'description': 'A fine test wine.',
            'price': 10,
            'vintage': 2020,
            'volume': 750,
            'closure': 'natural cork',
            'abv': 13.5,
            'acidity': 3.0,
            'residual_sugar': 1.0,
            'stock': 5,
            'slug': 'test-wine',
            'category': self.category.id,
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertGreater(len(form.errors), 0)

    def test_invalid_product_form_non_alphanumeric_name(self):
        """
        Test ProductForm validation for non-alphanumeric characters in name
        """
        form_data = {
            'name': 'Test Wine @#',
            'sku': 'TW001',
            'slug': 'test-wine',
            'description': 'A fine test wine.',
            'price': '10.00',
            'vintage': 2020,
            'volume': 750,
            'closure': 'natural cork',
            'abv': 13.5,
            'acidity': 5.0,
            'residual_sugar': 3.0,
            'stock': 10,
            'category': self.category.id,
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['name'],
            ['Name must contain only letters, numbers and spaces.'])

    def test_invalid_product_form_price_negative(self):
        """
        Test ProductForm validation for negative price
        """
        form_data = {
            'name': 'Test Wine',
            'sku': 'TW001',
            'slug': 'test-wine',
            'description': 'A fine test wine.',
            'price': '-10.00',  # Invalid price
            'vintage': 2020,
            'volume': 750,
            'closure': 'natural cork',
            'abv': 13.5,
            'acidity': 5.0,
            'residual_sugar': 3.0,
            'stock': 10,
            'category': self.category.id,
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['price'],
            ['Price must be greater than $0.'])

    def test_invalid_product_form_stock_exceeds_limit(self):
        """
        Test ProductForm validation for stock exceeding max limit
        """
        form_data = {
            'name': 'Test Wine',
            'sku': 'TW001',
            'slug': 'test-wine',
            'description': 'A fine test wine.',
            'price': '10.00',
            'vintage': 2020,
            'volume': 750,
            'closure': 'natural cork',
            'abv': 13.5,
            'acidity': 5.0,
            'residual_sugar': 3.0,
            'stock': 100000,  # Exceeds limit
            'category': self.category.id,
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['stock'],
            ['Stock exceeds the max limit of 99,999.'])

    def test_order_status_form_valid(self):
        """
        Test valid OrderStatusForm submission
        """
        order = Order.objects.create(
            full_name='John Doe', email='john@example.com',
            phone_number='1234567890', country='Australia',
            postcode='12345', town_or_city='Anytown',
            street_address1='123 Main St', street_address2='',
            county='Adelaide')
        form_data = {
            'status': 'pending',
        }
        form = OrderStatusForm(data=form_data, instance=order)
        self.assertTrue(form.is_valid(), form.errors)

    def test_order_status_form_invalid(self):
        """
        Test OrderStatusForm validation with invalid status
        """
        order = Order.objects.create(
            full_name='John Doe', email='john@example.com',
            phone_number='1234567890', country='Australia',
            postcode='12345', town_or_city='Anytown',
            street_address1='123 Main St', street_address2='',
            county='Adelaide')
        form_data = {
            'status': '',  # Invalid as it's empty
        }
        form = OrderStatusForm(data=form_data, instance=order)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['status'], ['This field is required.'])
