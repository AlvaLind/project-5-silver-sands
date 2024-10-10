from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from products.models import Wine, Category


class BagViewsTestCase(TestCase):
    def setUp(self):
        # Create a category instance
        self.category = Category.objects.create(
            name="Red Wine",
            description="A category for red wines"
        )

        # Create a wine instance with all required fields
        self.wine = Wine.objects.create(
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
            category=self.category
        )

    def tearDown(self):
        # Clean up by deleting the wine and category instances
        self.wine.delete()
        self.category.delete()

    def test_view_bag(self):
        """Test that the view_bag page renders correctly."""
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

        # Check that 'on_bag_page' is in the response context
        self.assertIn('on_bag_page', response.context)

    def test_add_to_bag_success(self):
        """Test adding a product to the bag successfully."""
        response = self.client.post(
            reverse('add_to_bag', args=[self.wine.pk]),
            {'quantity': 1, 'redirect_url': '/'})
        self.assertEqual(response.status_code, 302)  # Check for a redirect

        # Verify the item was added to the session bag
        self.assertIn(str(self.wine.pk), self.client.session['bag'])
        self.assertEqual(self.client.session['bag'][str(self.wine.pk)], 1)

        # Check success message
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn(
            f'Successfully added {self.wine.name} to your bag', messages)

    def test_add_to_bag_out_of_stock(self):
        """Test adding a product that is out of stock."""
        # Set the wine stock to 0
        self.wine.stock = 0
        self.wine.available = False
        self.wine.save()

        response = self.client.post(
            reverse('add_to_bag', args=[self.wine.pk]),
            {'quantity': 1, 'redirect_url': '/'})
        self.assertEqual(response.status_code, 302)  # Check for redirect

        # Check for error message
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn(
            f'Sorry, {self.wine.name} is currently out of stock \
            and unavailable.', messages)

    def test_add_to_bag_exceeds_stock(self):
        """Test adding a quantity that exceeds available stock."""
        response = self.client.post(
            reverse('add_to_bag', args=[self.wine.pk]),
            {'quantity': 15, 'redirect_url': '/'})
        self.assertEqual(response.status_code, 302)  # Check for redirect

        # Check for error message about stock
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn(
            f'Sorry, there are only {self.wine.stock} {self.wine.name} \
            left in stock.', messages)

    def test_adjust_bag_success(self):
        """Test adjusting the quantity of a product in the bag."""
        self.client.post(
            reverse('add_to_bag', args=[self.wine.pk]),
            {'quantity': 1, 'redirect_url': '/'})  # Add item to the bag
        response = self.client.post(
            reverse('adjust_bag', args=[self.wine.pk]), {'quantity': 2})

        self.assertEqual(response.status_code, 302)  # Check for a redirect
        self.assertEqual(self.client.session['bag'][str(self.wine.pk)], 2)

        # Check success message
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn(f'Updated {self.wine.name} quantity to \
            {self.client.session["bag"][str(self.wine.pk)]}', messages)

    def test_adjust_bag_out_of_stock(self):
        """Test adjusting quantity of a product that is out of stock."""
        self.client.post(
            reverse('add_to_bag', args=[self.wine.pk]),
            {'quantity': 1, 'redirect_url': '/'})  # Add item to the bag
        self.wine.stock = 0
        self.wine.available = False
        self.wine.save()

        response = self.client.post(
            reverse('adjust_bag', args=[self.wine.pk]), {'quantity': 2})
        self.assertEqual(response.status_code, 302)  # Check for a redirect

        # Check for error message about stock
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn(
            f'Sorry, {self.wine.name} is currently out of stock \
            and unavailable.', messages)

    def test_remove_from_bag(self):
        """Test removing an item from the bag."""
        self.client.post(
            reverse('add_to_bag', args=[self.wine.pk]),
            {'quantity': 1, 'redirect_url': '/'})  # Add item to the bag
        self.assertIn(str(self.wine.pk), self.client.session['bag'])

        response = self.client.post(
            reverse('remove_from_bag', args=[self.wine.pk]))
        self.assertEqual(response.status_code, 200)  # Check for a 200 OK

        # Check that the item was removed
        self.assertNotIn(str(self.wine.pk), self.client.session['bag'])

        # Check success message
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn(f'Removed {self.wine.name} from your bag', messages)

    def test_remove_from_bag_not_in_bag(self):
        """Test trying to remove an item that isn't in the bag."""
        response = self.client.post(
            reverse('remove_from_bag', args=[self.wine.pk]))
        self.assertEqual(response.status_code, 200)  # Check for a 200 OK

        # Check that no error occurs
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertNotIn(f'Removed {self.wine.name} from your bag', messages)
