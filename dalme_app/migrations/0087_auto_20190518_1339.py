# Generated by Django 2.1.7 on 2019-05-18 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0086_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='glottolog_id',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='iso6393_id',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
