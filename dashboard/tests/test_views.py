from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User





class DashboardViewTest(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')


    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('dashboard:dashboard'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'dashboard.html', 'base_generic.html')
