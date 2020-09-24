# Generated by Django 2.1.7 on 2019-04-19 13:57

import dalme_app.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0031_auto_20190414_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='DT_fields',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('creation_username', models.CharField(blank=True, default=dalme_app.models._templates.get_current_username, max_length=255, null=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_username', models.CharField(blank=True, default=dalme_app.models._templates.get_current_username, max_length=255, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('render_exp', models.CharField(max_length=255, null=True)),
                ('orderable', models.BooleanField(default=False)),
                ('visible', models.BooleanField(default=False)),
                ('searchable', models.BooleanField(default=False)),
                ('dte_type', models.CharField(max_length=55, null=True)),
                ('dte_options', models.CharField(max_length=255, null=True)),
                ('filter_operator', models.CharField(choices=[('and', 'and'), ('or', 'or')], max_length=55, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DT_list',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('creation_username', models.CharField(blank=True, default=dalme_app.models._templates.get_current_username, max_length=255, null=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_username', models.CharField(blank=True, default=dalme_app.models._templates.get_current_username, max_length=255, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=55)),
                ('description', models.TextField()),
                ('default_headers', models.CharField(max_length=255, null=True)),
                ('extra_headers', models.CharField(max_length=255, null=True)),
                ('api_url', models.CharField(max_length=255)),
                ('form_helper', models.CharField(max_length=255)),
                ('content_types', models.ManyToManyField(to='dalme_app.Content_type')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.RemoveField(
            model_name='content_list',
            name='content_types',
        ),
        migrations.AddField(
            model_name='attribute_type',
            name='source',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Content_list',
        ),
        migrations.AddField(
            model_name='dt_fields',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dalme_app.Attribute_type'),
        ),
        migrations.AddField(
            model_name='dt_fields',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dalme_app.DT_list'),
        ),
    ]
