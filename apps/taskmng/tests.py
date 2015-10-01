from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from taskmng.views import tasks


class TaskmngViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='tester', email='tester@whitehouse.gov',
            password='top_secret')

    def test_tasks_view(self):
        """
            Response status must be 200.
            Show page only for authorized users.
            Page must have logout button
        """

        # Show page only for authorized users
        request = self.factory.get(reverse('taskmng:tasks'))
        request.user = self.user
        response = tasks(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/logout/?next=/')
