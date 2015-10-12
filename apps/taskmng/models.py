from django.db import models
from django.contrib.auth.models import User
import datetime


class Task(models.Model):
    class Meta:
        app_label = 'taskmng'
    owner = models.ForeignKey(User)
    text = models.TextField()
    due_to = models.DateField()
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    assigned_to = models.ManyToManyField(User, related_name='assigned',
                                         blank=True)


class Team(models.Model):
    class Meta:
        app_label = 'taskmng'
    owner = models.ForeignKey(User)
    name = models.TextField()
    created_at = models.DateField(default=datetime.datetime.now)


class Teammate(models.Model):
    class Meta:
        app_label = 'taskmng'
    team = models.ForeignKey(Team)
    user = models.ForeignKey(User)
