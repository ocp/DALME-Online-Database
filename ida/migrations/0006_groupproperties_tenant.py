# Generated by Django 4.2.2 on 2023-12-13 15:07
from django.db import migrations


def noop(apps, schema_editor):
    """Stubbed noop migration.

    After discovering an inconsistency in the complex IDA migration this
    function is just to perform surgery on the overall migration flow without
    having to completely refactor the dependency chain of the migrations.

    It does nothing, and having removed the corresponding field from the Group
    model it *would* have added, the sum total should be nothing and a
    consistent model of the tables.

    """
    print('IDA migration 0006 no-op')  # noqa: T201


class Migration(migrations.Migration):
    dependencies = [
        ('ida', '0005_groupproperties'),
    ]

    operations = [
        migrations.RunPython(noop),
    ]
