from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from taskmng.views import tasks
from django.utils import unittest
from taskmng.models import Tasks
import datetime


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


class TasksModelTests(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test2',
                                             password='test2')
        self.user.is_superuser = True
        self.user.save()

    def test_create_new_task_in_db(self):
        """
            Create new task item in db
        """
        task = Tasks()
        task.owner = self.user
        task.text = 'Test task'
        task.due_to = datetime.date.today()
        task.completed = False
        task.priority = 0
        task.save()

        all_tasks = Tasks.objects.all()
        self.assertEqual(len(all_tasks), 1)
        self.assertEqual(all_tasks[0], task)
