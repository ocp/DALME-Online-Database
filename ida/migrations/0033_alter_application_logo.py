# Generated by Django 4.2.2 on 2024-01-03 17:29
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ida', '0032_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
