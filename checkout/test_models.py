from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User

from checkout.models import Order, OrderLineItem
from products.models import Wine, Category
from profiles.models import UserProfile

class TestOrderModel(TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        Create a user, wine, and order instance to be used in tests.
        This method is called once for the entire class.
        """
        super().setUpClass()  # Call the base class's setUpClass
        
        # Create a test user and user profile
        cls.user = User.objects.create_user(
            username='testuser', password='password123')
        cls.user_profile, created = UserProfile.objects.get_or_create(user=cls.user)

        # Create a category instance
        cls.category = Category.objects.create(
            name="Red Wine",
            description="A category for red wines"
        )

        # Create a wine instance with all required fields
        cls.wine = Wine.objects.create(
            name="Test Wine",
            sku="TW001",
            slug="test-wine",
            description="A fine test wine.",
            price=19.99,
            vintage=2020,
            volume=750,
            closure="natural cork",
            abv=13.5,
            stock=10,
            available=True,
            category=cls.category
        )

        # Create an order object
        cls.order = Order.objects.create(
            user_profile=cls.user_profile,
            full_name='Test User',
            email='testuser@example.com',
            phone_number='123456789',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test Street',
            delivery_cost=Decimal('5.00'),
            order_total=Decimal('0.00'),
            grand_total=Decimal('0.00'),
            original_bag='{"1": 1}',
            stripe_pid='test_pid_123',
        )

    def test_order_number_is_generated(self):
        """
        Test that an order number is generated when saving an order.
        """
        self.assertIsNotNone(self.order.order_number)
        self.assertTrue(self.order.order_number.startswith('ORD-'))

    def test_update_total_below_threshold(self):
        """
        Test that the update_total method correctly calculates order totals
        when below the free delivery threshold.
        """
        # Create a line item for the order
        OrderLineItem.objects.create(
            order=self.order,
            wine=self.wine,
            quantity=2
        )

        # Call the method to update totals
        self.order.update_total()

        # Check if order totals are correctly updated, Total price = 19.99 * 2 = 39.98
        # Delivery 10% of 39.98, total = order_total + delivery_cost
        self.assertEqual(self.order.order_total, Decimal('39.98'))
        self.assertEqual(self.order.delivery_cost, Decimal('4.00'))
        self.assertEqual(self.order.grand_total, Decimal('43.98'))

    def test_update_total_above_threshold(self):
        """
        Test that the update_total method correctly calculates order totals
        when above the free delivery threshold.
        """
        # Set up an order with high total
        Order.objects.create(
            user_profile=self.user_profile,
            full_name='Test User',
            email='testuser@example.com',
            phone_number='123456789',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test Street',
            delivery_cost=Decimal('0.00'),
            order_total=Decimal('0.00'),
            grand_total=Decimal('0.00'),
            original_bag='{"1": 1}',
            stripe_pid='test_pid_123',
        )

        # Create a line item for the order with high total
        OrderLineItem.objects.create(
            order=self.order,
            wine=self.wine,
            quantity=7  # Total price = 19.99 * 7 = 139.93
        )

        # Call the method to update totals
        self.order.update_total()

        # Check if order total is updated correctly, Total price = 19.99 * 7 = 139.93
        # Delivery = free, total = order_total + delivery_cost
        self.assertEqual(self.order.order_total, Decimal('139.93'))
        self.assertEqual(self.order.delivery_cost, Decimal('0.00'))
        self.assertEqual(self.order.grand_total, Decimal('139.93'))


class TestOrderLineItemModel(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Create a user, wine, and order instance to be used in tests.
        This method is called once for the entire class.
        """
        super().setUpClass()  # Call the base class's setUpClass
        
        # Create a test user and user profile
        cls.user = User.objects.create_user(
            username='testuser2', password='password456')
        cls.user_profile, created = UserProfile.objects.get_or_create(user=cls.user)

        # Create a category instance
        cls.category = Category.objects.create(
            name="Red Wine",
            description="A category for red wines"
        )

        # Create a wine instance with all required fields
        cls.wine = Wine.objects.create(
            name="Test Wine",
            sku="TW001",
            slug="test-wine",
            description="A fine test wine.",
            price=19.99,
            vintage=2020,
            volume=750,
            closure="natural cork",
            abv=13.5,
            stock=10,
            available=True,
            category=cls.category
        )

        # Create an order object
        cls.order = Order.objects.create(
            user_profile=cls.user_profile,
            full_name='Test User',
            email='testuser@example.com',
            phone_number='123456789',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test Street',
            delivery_cost=Decimal('0.00'),
            order_total=Decimal('0.00'),
            grand_total=Decimal('0.00'),
            original_bag='{"1": 1}',
            stripe_pid='test_pid_123',
        )

    def test_lineitem_total(self):
        """
        Test that the lineitem total is calculated correctly.
        """
        # Create a line item for the order
        lineitem = OrderLineItem.objects.create(
            order=self.order,
            wine=self.wine,
            quantity=2
        )

        # Check if line item total is correct, 2 * 19.99 = 39.98
        self.assertEqual(lineitem.lineitem_total, Decimal('39.98'))

    def test_lineitem_saves_updates_order_total(self):
        """
        Test that saving a line item updates the order total correctly.
        """
        # Create a line item for the order
        lineitem = OrderLineItem.objects.create(
            order=self.order,
            wine=self.wine,
            quantity=2
        )

        # Call the method to update totals
        self.order.update_total()

        # Check if order total is updated correctly, 2 * 19.99 = 39.98
        # Delivery = 10% of 39.98, total = order_total + delivery_cost
        self.assertEqual(self.order.order_total, Decimal('39.98'))
        self.assertEqual(self.order.delivery_cost, Decimal('4.00'))
        self.assertEqual(self.order.grand_total, Decimal('43.98'))
