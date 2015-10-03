from django.db import models
from django.contrib.auth.models import User


class Tasks(models.Model):
    class Meta:
        app_label = 'taskmng'
    owner = models.ForeignKey(User)
    text = models.TextField()
    due_to = models.DateField()
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    assigned_to = models.ManyToManyField(User, related_name='assigned',
                                         blank=True)
