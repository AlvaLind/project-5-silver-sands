from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Order
from products.models import Wine, Category

class CheckoutViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Test Category")
        cls.user = User.objects.create_user(username='testuser', password='testpass')

        cls.wine = Wine.objects.create(
            name="Test Wine",
            sku="TW001",
            slug="test-wine",
            description="A fine test wine.",
            price=10,
            vintage=2020,
            volume=750,
            closure="natural cork",
            abv=13.5,
            stock=5,
            available=True,
            category=cls.category
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_cache_checkout_data(self):
        response = self.client.post(reverse('cache_checkout_data'), {
            'client_secret': 'test_client_secret',
            'save_info': True,
        })
        # Expecting a 200 response for successful cache checkout data
        self.assertEqual(response.status_code, 200)

    def test_checkout_redirect_empty_bag(self):
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse('product_list'))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any(str(msg) == "Your bag is empty at the moment!" for msg in messages_list))

    def test_checkout_success(self):
        self.client.session['bag'] = {self.wine.id: 2}
        self.client.session.save()

        response = self.client.post(reverse('checkout'), {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'country': 'Australia',
            'postcode': '12345',
            'town_or_city': 'Anytown',
            'street_address1': '123 Main St',
            'street_address2': '',
            'county': 'Adelaide',
        })

        # Debugging output
        print(f'Checkout response status: {response.status_code}, response content: {response.content}')

        # Expecting a redirect and checking if order exists in context
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertIn('order', response.context, "Expected 'order' in response context.")
        order = response.context['order']
        self.assertRedirects(response, reverse('checkout_success', args=[order.order_number]))

    def test_checkout_insufficient_stock(self):
        self.client.session['bag'] = {self.wine.id: 10}  # More than available stock
        self.client.session.save()

        response = self.client.post(reverse('checkout'), {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'country': 'Australia',
            'postcode': '12345',
            'town_or_city': 'Anytown',
            'street_address1': '123 Main St',
            'street_address2': '',
            'county': 'Adelaide',
        })

        # Expect to redirect to the bag view
        self.assertRedirects(response, reverse('view_bag'))
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any(str(msg) == 'Sorry, there are only 5 of Test Wine left in stock.' for msg in messages_list))

    def test_checkout_success_view(self):
        order = Order.objects.create(
            full_name='John Doe',
            email='john@example.com',
            phone_number='1234567890',
            country='Australia',
            postcode='12345',
            town_or_city='Anytown',
            street_address1='123 Main St',
            street_address2='',
            county='Adelaide',
        )
        response = self.client.get(reverse('checkout_success', args=[order.order_number]))
        
        # Expecting a 200 response for successful view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
