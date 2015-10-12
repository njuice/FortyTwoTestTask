from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, AnonymousUser
from taskmng.views import tasks, team, current_user, invitable, team_invitable
from django.utils import unittest
from taskmng.models import Task, Team, Teammate
from social.apps.django_app.default.models import UserSocialAuth
import datetime
import json
from tastypie.test import ResourceTestCase
from tastypie.authentication import BasicAuthentication


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

    def test_tasks_view_no_auth(self):
        """
            Response status must be 302.
        """
        request = self.factory.get(reverse('taskmng:tasks'))
        request.user = AnonymousUser()
        response = tasks(request)
        self.assertEqual(response.status_code, 302)


class TasksModelTests(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test2',
                                             password='test2')
        self.user.is_superuser = True
        self.user.save()
        self.user2 = User.objects.create_user(username='test22',
                                              password='test22')
        self.user2.is_superuser = True
        self.user2.save()

    def test_create_new_task_in_db(self):
        """
            Creates new task item in db
        """
        task = Task()
        task.owner = self.user
        task.text = 'Test task'
        task.due_to = datetime.date.today()
        tasks.assigned_to = self.user
        task.completed = False
        task.priority = 0
        task.save()

        task.assigned_to.add(self.user2)
        task.save()

        all_tasks = Task.objects.all()
        self.assertEqual(len(all_tasks), 1)
        self.assertEqual(all_tasks[0], task)

        task.delete()
        all_tasks = Task.objects.all()
        self.assertEqual(len(all_tasks), 0)


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

    def test_add_new_team(self):
        """
            Add new team instance
        """
        request = self.factory.post(reverse('taskmng:team'),
                                    {"add_team": 1, "name": "My team"})
        request.user = self.user
        team(request)
        self.assertEqual(Team.objects.count(), 1)

    def test_team_view_no_auth(self):
        """
            Response status must be 302.
        """
        request = self.factory.get(reverse('taskmng:team'))
        request.user = AnonymousUser()
        response = team(request)
        self.assertEqual(response.status_code, 302)


class TeamModelTests(unittest.TestCase):
    def setUp(self):
        self.user2 = User.objects.create_user(username='test3',
                                              password='test3')
        self.user2.is_superuser = True
        self.user2.save()

    def test_create_new_team_in_db(self):
        """
            Creates new team item in db
        """
        team = Team()
        team.owner = self.user2
        team.text = 'My super team'
        team.created_at = datetime.datetime.now()
        team.save()

        all_teams = Team.objects.all()
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
            Creates new team item in db
        """
        team = Team()
        team.owner = self.user3
        team.text = 'My super team'
        team.created_at = datetime.datetime.now()
        team.save()

        teammates = Teammate()
        teammates.team = team
        teammates.user = self.user3
        teammates.save()

        all_teammates = Teammate.objects.all()
        self.assertEqual(len(all_teammates), 1)
        self.assertEqual(all_teammates[0], teammates)

        teammates.delete()
        all_teammates = Teammate.objects.all()
        self.assertEqual(len(all_teammates), 0)


class CurrentUserViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='tester', email='tester@whitehouse.gov',
            password='top_secret')

    def test_current_user_view(self):
        """
            Returns current user instance in json
        """
        request = self.factory.get(reverse('taskmng:current_user'))
        request.user = self.user
        response_json = current_user(request)
        response = json.loads(response_json.content)
        self.assertEqual(response[0]['pk'], 1)

    def test_current_user_view_for_no_auth(self):
        """
            Don't Returns any data for non auth user
        """
        request = self.factory.get(reverse('taskmng:current_user'))
        request.user = AnonymousUser()
        response_json = current_user(request)
        response = json.loads(response_json.content)
        self.assertEqual(response['result']['logged'], False)


class InvitableViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='tester', email='tester@whitehouse.gov',
            password='top_secret')

        extra_data = '{"access_token": "CAAFlJJBNXLoBAM41Q2UP5W' \
                     'uJXrPl1CeD9ZC2ZBgk7g412CwE584vY87k0SkbklWz0' \
                     'fJayhsEvgP43EWe7B5TpOLQm2M0zKYuVYYYfuS' \
                     'LMNLtCFRJPpn9nn4DXrKHxRwS8zWrBt1BZBDBbDkYl3' \
                     'UiH7CTZApd5kDc8EUQMZBZBuw8OlZB' \
                     'ayqCbfLMCMfZCZCLY9tMZD", "expires": null, ' \
                     '"id": "1087311591297294"}'

        self.auth = UserSocialAuth.objects.create(user=self.user,
                                                  extra_data=extra_data,
                                                  uid="1087311591297294",
                                                  provider="facebook")
        self.auth.save()

    def test_invitable_view(self):
        """
           Returns invatable fb friends list in json
        """
        request = self.factory.get(reverse('taskmng:invitable'))
        request.user = self.user
        response_json = invitable(request)
        response = json.loads(response_json.content)
        self.assertGreater(len(response), 0)

    def test_team_view_no_auth(self):
        """
            Response status must be 302.
        """
        request = self.factory.get(reverse('taskmng:invitable'))
        request.user = AnonymousUser()
        response = invitable(request)
        self.assertEqual(response.status_code, 302)


class TeamInvitableViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='tester', email='tester@whitehouse.gov',
            password='top_secret')

        self.user2 = User.objects.create_user(username='test',
                                              password='test')
        self.user2.is_superuser = True
        self.user2.save()

        self.user3 = User.objects.create_user(username='test4',
                                              password='test4')
        self.user3.is_superuser = True
        self.user3.save()

        self.team = Team()
        self.team.owner = self.user
        self.team.text = 'My super team'
        self.team.created_at = datetime.datetime.now()
        self.team.save()

        self.teammates = Teammate()
        self.teammates.team = self.team
        self.teammates.user = self.user3
        self.teammates.save()

    def test_team_invitable(self):
        """
           Returns team invitable view
        """
        request = self.factory.get(reverse('taskmng:team_invitable'))
        request.user = self.user
        response_json = team_invitable(request)
        response = json.loads(response_json.content)
        self.assertEqual(len(response), 1)

    def test_teammate_add(self):
        """
            Adds new teammate
        """
        request = self.factory.post(reverse('taskmng:team_invitable'),
                                    {"cmd": "add",
                                     "item": json.dumps({"id": 2})})
        request.user = self.user
        response_json = team_invitable(request)
        response = json.loads(response_json.content)
        self.assertEqual(response['result'], 'ok')

    def test_teammate_remove(self):
        """
            Adds new teammate
        """
        request = self.factory.post(reverse('taskmng:team_invitable'),
                                    {"cmd": "add",
                                     "item": json.dumps({"id": 2})})
        request.user = self.user
        team_invitable(request)

        request = self.factory.post(reverse('taskmng:team_invitable'),
                                    {"cmd": "del", "tmId": 1})
        request.user = self.user
        response_json = team_invitable(request)
        response = json.loads(response_json.content)
        self.assertEqual(response['result'], 'ok')

    def test_team_view_no_auth(self):
        """
            Response status must be 302.
        """
        request = self.factory.get(reverse('taskmng:team_invitable'))
        request.user = AnonymousUser()
        response = team_invitable(request)
        self.assertEqual(response.status_code, 302)


class TeammatesResourceTest(ResourceTestCase):
    def setUp(self):
        super(TeammatesResourceTest, self).setUp()
        self.username = 'test'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username,
                                             'test@example.com',
                                             self.password)

        extra_data = '{"access_token": "CAAFlJJBNXLoBAM41Q2UP5W' \
                     'uJXrPl1CeD9ZC2ZBgk7g412CwE584vY87k0SkbklWz0' \
                     'fJayhsEvgP43EWe7B5TpOLQm2M0zKYuVYYYfuS' \
                     'LMNLtCFRJPpn9nn4DXrKHxRwS8zWrBt1BZBDBbDkYl3' \
                     'UiH7CTZApd5kDc8EUQMZBZBuw8OlZB' \
                     'ayqCbfLMCMfZCZCLY9tMZD", "expires": null, ' \
                     '"id": "1087311591297294"}'
        self.auth = UserSocialAuth.objects.create(user=self.user,
                                                  extra_data=extra_data,
                                                  uid="1087311591297294",
                                                  provider="facebook")

        self.team = Team()
        self.team.owner = self.user
        self.team.text = 'My super team'
        self.team.created_at = datetime.datetime.now()
        self.team.save()

        self.teammates = Teammate()
        self.teammates.team = self.team
        self.teammates.user = self.user
        self.teammates.save()

    def get_credentials(self):
        return self.create_basic(username=self.username,
                                 password=self.password)

    def test_custom_facebook_auth(self):
        """
            Api must return team instance with teammates
        """
        response_json = self.api_client.get(
            '/api/v1/teammates/1/', format='json',
            authentication=self.get_credentials()
        )
        response = json.loads(response_json.content)
        self.assertEqual(response["id"], 1)


class FacebookLoginTest(TestCase):
    def test_fb_login(self):
        """
            Facebook login must return 302 statuc
        """
        response = self.client.get('/login/facebook/?next=')
        self.assertEqual(response.status_code, 302)
