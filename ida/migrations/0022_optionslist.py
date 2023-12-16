# Generated by Django 4.2.2 on 2023-12-16 12:30
import django_currentuser.middleware

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ida', '0021_page'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='OptionsList',
                    fields=[
                        ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                        ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                        ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                        ('name', models.CharField(max_length=255)),
                        (
                            'payload_type',
                            models.CharField(
                                choices=[
                                    ('db_records', 'DB Records'),
                                    ('field_choices', 'Field Choices'),
                                    ('static_list', 'Static List'),
                                ],
                                max_length=15,
                            ),
                        ),
                        ('description', models.TextField()),
                        ('payload', models.JSONField()),
                        (
                            'creation_user',
                            models.ForeignKey(
                                default=django_currentuser.middleware.get_current_user,
                                null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name='%(app_label)s_%(class)s_creation',
                                to=settings.AUTH_USER_MODEL,
                            ),
                        ),
                        (
                            'modification_user',
                            models.ForeignKey(
                                default=django_currentuser.middleware.get_current_user,
                                null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name='%(app_label)s_%(class)s_modification',
                                to=settings.AUTH_USER_MODEL,
                            ),
                        ),
                    ],
                    options={
                        'abstract': False,
                    },
                ),
            ],
            database_operations=[],
        ),
    ]
