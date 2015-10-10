from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from taskmng.views import tasks, team
from django.utils import unittest
from taskmng.models import Tasks, Teams, Teammates
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


class TeamViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='tester', email='tester@whitehouse.gov',
            password='top_secret')

    def test_tasks_view(self):
        """
            Response status must be 200.
            Show page only for authorized users.
            Page must have tags for angular apps
        """

        # Show page only for authorized users
        request = self.factory.get(reverse('taskmng:team'))
        request.user = self.user
        response = team(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<team-manage></team-manage>')
        self.assertContains(response, '<invite-friends></invite-friends>')


class TeamModelTests(unittest.TestCase):
    def setUp(self):
        self.user2 = User.objects.create_user(username='test3',
                                              password='test3')
        self.user2.is_superuser = True
        self.user2.save()

    def test_create_new_team_in_db(self):
        """
            Create new team item in db
        """
        team = Teams()
        team.owner = self.user2
        team.text = 'My super team'
        team.created_at = datetime.datetime.now()
        team.save()

        all_teams = Teams.objects.all()
        self.assertEqual(len(all_teams), 1)
        self.assertEqual(all_teams[0], team)


class TeammatesModelTests(unittest.TestCase):
    def setUp(self):
        self.user3 = User.objects.create_user(username='test4',
                                              password='test4')
        self.user3.is_superuser = True
        self.user3.save()

    def test_create_new_team_in_db(self):
        """
            Create new team item in db
        """
        team = Teams()
        team.owner = self.user3
        team.text = 'My super team'
        team.created_at = datetime.datetime.now()
        team.save()

        teammates = Teammates()
        teammates.team = team
        teammates.user = self.user3
        teammates.save()

        all_teammates = Teammates.objects.all()
        self.assertEqual(len(all_teammates), 1)
        self.assertEqual(all_teammates[0], teammates)
