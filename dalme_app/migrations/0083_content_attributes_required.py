# Generated by Django 2.1.7 on 2019-05-15 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0082_remove_dt_fields_nowrap'),
    ]

    operations = [
        migrations.AddField(
            model_name='content_attributes',
            name='required',
            field=models.BooleanField(default=False),
        ),
    ]
