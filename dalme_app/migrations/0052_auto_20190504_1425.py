# Generated by Django 2.1.7 on 2019-05-04 18:25

import dalme_app.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0051_auto_20190429_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='dt_list',
            name='preview_helper',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(default=dalme_app.models._templates.get_current_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='taskcomment',
            name='author',
            field=models.ForeignKey(blank=True, default=dalme_app.models._templates.get_current_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
