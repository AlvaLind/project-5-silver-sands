from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Wine, Category
from reviews.models import Review


class ProductViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data that will be used across multiple tests.
        """
        # Create a Category and two Wine instances
        cls.category = Category.objects.create(name='Test Category')
        
        cls.wine1 = Wine.objects.create(
            name='Test Wine 1',
            sku='TW001',
            slug='test-wine-1',
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
        
        cls.wine2 = Wine.objects.create(
            name='Test Wine 2',
            sku='TW002',
            slug='test-wine-2',
            description='A second fine test wine.',
            price=Decimal('20.00'),
            vintage=2019,
            volume=750,
            closure='natural cork',
            abv=13.0,
            acidity=5.0,
            residual_sugar=3.0,
            stock=0,
            available=False,
            category=cls.category
        )
        
        # Create a test user
        cls.user = User.objects.create_user(username='testuser', password='12345')

        # Create a review for wine1 by the user
        cls.review = Review.objects.create(wine=cls.wine1, user=cls.user, rating=4)

    def test_product_list_view(self):
        """Test product listing view with filters and sorting"""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertContains(response, 'Test Wine 1')
        self.assertContains(response, 'Test Wine 2')

        # Test category filter
        response = self.client.get(reverse('product_list'), {'category': 'Test Category'})
        self.assertContains(response, 'Test Wine 1')
        self.assertContains(response, 'Test Wine 2')

        # Test sorting by price ascending
        response = self.client.get(reverse('product_list'), {'sort': 'price_asc'})
        wines = response.context['page_obj'].object_list
        self.assertEqual(wines[0].price, Decimal('10.00'))  # Cheapest wine should come first
        self.assertEqual(wines[1].price, Decimal('20.00'))

    def test_product_details_view(self):
        """Test product details view and review submission"""
        response = self.client.get(reverse('product_details', args=[self.wine1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_details.html')
        self.assertContains(response, 'Test Wine 1')
        self.assertContains(response, 'A fine test wine.')

        # Test average rating
        self.assertEqual(response.context['average_rating'], 4.0)

        # Test posting a new review (while logged in)
        self.client.login(username='testuser', password='12345')
        review_data = {
            'rating': 5,
            'commnet': 'Amazing Wine',
        }
        response = self.client.post(reverse('product_details', args=[self.wine1.id]), review_data)
        self.assertRedirects(response, reverse('product_details', args=[self.wine1.id]))

    def test_delete_review(self):
        """Test review deletion for the owner"""
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_review', args=[self.wine1.id, self.review.id]))
        self.assertRedirects(response, reverse('product_details', args=[self.wine1.id]))
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_delete_review_not_authorized(self):
        """Ensure users cannot delete others' reviews"""
        another_user = User.objects.create_user(username='anotheruser', password='password')
        self.client.login(username='anotheruser', password='password')
        response = self.client.post(reverse('delete_review', args=[self.wine1.id, self.review.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_edit_review(self):
        """Test review editing by the owner and it becomes unapproved"""
        self.client.login(username='testuser', password='12345')
        edit_data = {
            'rating': 3,
            'comment': 'Edited Review',
        }
        response = self.client.post(reverse('edit_review', args=[self.wine1.id, self.review.id]), edit_data)
        self.assertRedirects(response, reverse('product_details', args=[self.wine1.id]))
        updated_review = Review.objects.get(id=self.review.id)
        self.assertEqual(updated_review.comment, 'Edited Review')
        self.assertEqual(updated_review.approved, False)

    def test_search_products(self):
        """Test search functionality for wines"""
        response = self.client.get(reverse('search_products'), {'query': 'Test Wine'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/search_products.html')
        self.assertContains(response, 'Test Wine 1')
        self.assertContains(response, 'Test Wine 2')

        # Test price filter
        response = self.client.get(reverse('search_products'), {'price_min': '15'})
        self.assertContains(response, 'Test Wine 2')
        self.assertNotContains(response, 'Test Wine 1')
