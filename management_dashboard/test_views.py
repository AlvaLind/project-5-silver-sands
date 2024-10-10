from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import messages
from products.models import Wine, Category
from checkout.models import Order, OrderLineItem

User = get_user_model()


class ManagementDashboardViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Create a superuser, a category, and a wine product for testing.
        """
        cls.user = User.objects.create_superuser(
            username='admin', password='admin', email='admin@example.com')
        cls.category = Category.objects.create(name='Test Category')
        cls.wine = Wine.objects.create(
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
            category=cls.category
        )
        cls.order = Order.objects.create(
            full_name='John Doe',
            email='john@example.com',
            phone_number='1234567890',
            country='Australia',
            postcode='12345',
            town_or_city='Anytown',
            street_address1='123 Main St',
            street_address2='',
            county='Adelaide',
            status='pending'  # Set status to 'pending' for initial test setup
        )
        cls.order_line_item = OrderLineItem.objects.create(
            order=cls.order,
            wine=cls.wine,
            quantity=2,
            lineitem_total=20.00
        )

    def setUp(self):
        """
        Log in as the superuser for each test.
        """
        self.client.login(username='admin', password='admin')

    def test_add_product_view(self):
        """Test adding a new product."""
        url = reverse('add_product')
        data = {
            'name': 'New Test Wine',
            'sku': 'NTW001',
            'slug': 'new-test-wine',
            'description': 'A new fine test wine.',
            'price': 12.00,
            'vintage': 2021,
            'volume': 750,
            'closure': 'natural cork',
            'abv': 13.5,
            'acidity': 5.0,
            'residual_sugar': 3.0,
            'stock': 15,
            'category': self.category.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertTrue(Wine.objects.filter(name='New Test Wine').exists())

    def test_edit_product_view(self):
        """Test editing an existing product."""
        url = reverse('edit_product', args=[self.wine.id])
        data = {
            'name': 'Updated Test Wine',
            'sku': 'TW001',
            'slug': 'updated-test-wine',
            'description': 'An updated fine test wine.',
            'price': 15.00,
            'vintage': 2022,
            'volume': 750,
            'closure': 'natural cork',
            'abv': 13.5,
            'acidity': 5.0,
            'residual_sugar': 3.0,
            'stock': 20,
            'category': self.category.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.wine.refresh_from_db()
        self.assertEqual(self.wine.name, 'Updated Test Wine')

    def test_delete_product_view(self):
        """Test deleting a product."""
        url = reverse('delete_product', args=[self.wine.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertFalse(Wine.objects.filter(id=self.wine.id).exists())

    def test_manage_orders_view(self):
        """Test viewing and managing orders."""
        url = reverse('manage_orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.order_number)

    def test_order_details_view(self):
        """Test order details view."""
        url = reverse('order_details', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.order_number)

    def test_delete_order_view(self):
        """
        Test deleting an order if status is pending.
        """
        self.order.status = 'pending'  # Ensure order status set to 'pending'
        self.order.save()

        url = reverse('delete_order', args=[self.order.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirects after success

        # Verify the order has been deleted
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())
