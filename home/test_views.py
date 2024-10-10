from django.test import TestCase, Client
from django.urls import reverse


class HomeViewsTest(TestCase):

    def setUp(self):
        """
        Set up a test client for use in the tests.
        """
        self.client = Client()

    def test_home_view(self):
        """
        Test the home view renders correctly and context variables are set.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertIn('show_signup_form', response.context)
        self.assertTrue(response.context['show_signup_form'])

    def test_about_us_view(self):
        """
        Test the about us view renders correctly and context variables are set.
        """
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/about_us.html')
        self.assertIn('show_signup_form', response.context)
        self.assertTrue(response.context['show_signup_form'])

    def test_access_denied_view(self):
        """
        Test the access denied view renders correctly.
        """
        response = self.client.get(reverse('access_denied'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/access_denied.html')

    def test_visit_us_view(self):
        """
        Test the visit us view renders correctly and context variables are set.
        """
        response = self.client.get(reverse('visit_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/visit_us.html')
        self.assertIn('show_signup_form', response.context)
        self.assertTrue(response.context['show_signup_form'])
