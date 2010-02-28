
from south.db import db
from django.db import models
from kelp.program_log.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ProgramBlock'
        db.create_table('program_log_programblock', (
            ('id', orm['program_log.ProgramBlock:id']),
            ('start', orm['program_log.ProgramBlock:start']),
            ('end', orm['program_log.ProgramBlock:end']),
        ))
        db.send_create_signal('program_log', ['ProgramBlock'])
        
        # Adding model 'Quarter'
        db.create_table('program_log_quarter', (
            ('id', orm['program_log.Quarter:id']),
            ('begin', orm['program_log.Quarter:begin']),
            ('end', orm['program_log.Quarter:end']),
        ))
        db.send_create_signal('program_log', ['Quarter'])
        
        # Adding model 'Report'
        db.create_table('program_log_report', (
            ('id', orm['program_log.Report:id']),
            ('slug', orm['program_log.Report:slug']),
            ('name', orm['program_log.Report:name']),
        ))
        db.send_create_signal('program_log', ['Report'])
        
        # Adding model 'Entry'
        db.create_table('program_log_entry', (
            ('id', orm['program_log.Entry:id']),
            ('slot', orm['program_log.Entry:slot']),
            ('date', orm['program_log.Entry:date']),
            ('time', orm['program_log.Entry:time']),
            ('notes', orm['program_log.Entry:notes']),
            ('user', orm['program_log.Entry:user']),
        ))
        db.send_create_signal('program_log', ['Entry'])
        
        # Adding model 'Program'
        db.create_table('program_log_program', (
            ('id', orm['program_log.Program:id']),
            ('name', orm['program_log.Program:name']),
            ('url', orm['program_log.Program:url']),
        ))
        db.send_create_signal('program_log', ['Program'])
        
        # Adding model 'ProgramSlot'
        db.create_table('program_log_programslot', (
            ('id', orm['program_log.ProgramSlot:id']),
            ('active', orm['program_log.ProgramSlot:active']),
            ('program', orm['program_log.ProgramSlot:program']),
            ('time', orm['program_log.ProgramSlot:time']),
        ))
        db.send_create_signal('program_log', ['ProgramSlot'])
        
        # Adding ManyToManyField 'Report.program'
        db.create_table('program_log_report_program', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm.Report, null=False)),
            ('program', models.ForeignKey(orm.Program, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ProgramBlock'
        db.delete_table('program_log_programblock')
        
        # Deleting model 'Quarter'
        db.delete_table('program_log_quarter')
        
        # Deleting model 'Report'
        db.delete_table('program_log_report')
        
        # Deleting model 'Entry'
        db.delete_table('program_log_entry')
        
        # Deleting model 'Program'
        db.delete_table('program_log_program')
        
        # Deleting model 'ProgramSlot'
        db.delete_table('program_log_programslot')
        
        # Dropping ManyToManyField 'Report.program'
        db.delete_table('program_log_report_program')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'program_log.entry': {
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['program_log.ProgramSlot']"}),
            'time': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'program_log.program': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'program_log.programblock': {
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {})
        },
        'program_log.programslot': {
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['program_log.Program']"}),
            'time': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['program_log.ProgramBlock']"})
        },
        'program_log.quarter': {
            'begin': ('django.db.models.fields.DateField', [], {}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.SlugField', [], {'max_length': '3', 'unique': 'True', 'primary_key': 'True', 'db_index': 'True'})
        },
        'program_log.report': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'program': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['program_log.Program']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '20', 'unique': 'True', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['program_log']
