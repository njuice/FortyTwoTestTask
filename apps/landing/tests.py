from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser, User
from landing.views import index


class LandingViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='tester', email='tester@whitehouse.gov',
            password='top_secret')

    def test_index_view(self):
        """
            Response status must be 200.
            Page must contain dummy call-to-action button
            Show page only for non-authorized users
        """
        # Show page only for non-authorized users
        request = self.factory.get(reverse('landing:index'))
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign in with Facebook')

        # Redirect for authorized user
        request = self.factory.get(reverse('landing:index'))
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 302)
