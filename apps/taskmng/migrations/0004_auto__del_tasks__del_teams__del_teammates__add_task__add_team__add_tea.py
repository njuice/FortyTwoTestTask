# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Tasks'
        db.delete_table(u'taskmng_tasks')

        # Removing M2M table for field assigned_to on 'Tasks'
        db.delete_table(db.shorten_name(u'taskmng_tasks_assigned_to'))

        # Deleting model 'Teams'
        db.delete_table(u'taskmng_teams')

        # Deleting model 'Teammates'
        db.delete_table(u'taskmng_teammates')

        # Adding model 'Task'
        db.create_table(u'taskmng_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('due_to', self.gf('django.db.models.fields.DateField')()),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('taskmng', ['Task'])

        # Adding M2M table for field assigned_to on 'Task'
        m2m_table_name = db.shorten_name(u'taskmng_task_assigned_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['taskmng.task'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['task_id', 'user_id'])

        # Adding model 'Team'
        db.create_table(u'taskmng_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('taskmng', ['Team'])

        # Adding model 'Teammate'
        db.create_table(u'taskmng_teammate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taskmng.Team'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('taskmng', ['Teammate'])


    def backwards(self, orm):
        # Adding model 'Tasks'
        db.create_table(u'taskmng_tasks', (
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('due_to', self.gf('django.db.models.fields.DateField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('taskmng', ['Tasks'])

        # Adding M2M table for field assigned_to on 'Tasks'
        m2m_table_name = db.shorten_name(u'taskmng_tasks_assigned_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tasks', models.ForeignKey(orm['taskmng.tasks'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tasks_id', 'user_id'])

        # Adding model 'Teams'
        db.create_table(u'taskmng_teams', (
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('taskmng', ['Teams'])

        # Adding model 'Teammates'
        db.create_table(u'taskmng_teammates', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taskmng.Teams'])),
        ))
        db.send_create_signal('taskmng', ['Teammates'])

        # Deleting model 'Task'
        db.delete_table(u'taskmng_task')

        # Removing M2M table for field assigned_to on 'Task'
        db.delete_table(db.shorten_name(u'taskmng_task_assigned_to'))

        # Deleting model 'Team'
        db.delete_table(u'taskmng_team')

        # Deleting model 'Teammate'
        db.delete_table(u'taskmng_teammate')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'taskmng.task': {
            'Meta': {'object_name': 'Task'},
            'assigned_to': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'assigned'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'due_to': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'taskmng.team': {
            'Meta': {'object_name': 'Team'},
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'taskmng.teammate': {
            'Meta': {'object_name': 'Teammate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taskmng.Team']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['taskmng']