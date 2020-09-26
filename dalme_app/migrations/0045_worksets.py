# Generated by Django 2.1.7 on 2019-04-26 15:05

import dalme_app.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0044_auto_20190424_0914'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worksets',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('creation_username', models.CharField(blank=True, default=dalme_app.models._templates.get_current_username, max_length=255, null=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_username', models.CharField(blank=True, default=dalme_app.models._templates.get_current_username, max_length=255, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=55)),
                ('description', models.TextField()),
                ('query', models.TextField()),
                ('position', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(default=dalme_app.models._templates.get_current_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
