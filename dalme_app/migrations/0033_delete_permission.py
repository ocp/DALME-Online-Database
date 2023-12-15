# Generated by Django 4.2.2 on 2023-12-15 23:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('dalme_app', '0032_delete_publicregister'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Permission',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='Permission',
                    table='ida_permission',
                ),
            ],
        )
    ]
