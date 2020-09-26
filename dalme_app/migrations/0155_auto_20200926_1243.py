# Generated by Django 3.1 on 2020-09-26 16:43

import dalme_app.models._templates
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0154_auto_20200826_1339'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CityReference',
            new_name='LocaleReference',
        ),
        migrations.CreateModel(
            name='Source_credit',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('type', models.IntegerField(choices=[(1, 'Editor'), (2, 'Corrections'), (3, 'Contributor')])),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='dt_fields',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='dt_fields',
            name='creation_user',
        ),
        migrations.RemoveField(
            model_name='dt_fields',
            name='field',
        ),
        migrations.RemoveField(
            model_name='dt_fields',
            name='list',
        ),
        migrations.RemoveField(
            model_name='dt_fields',
            name='modification_user',
        ),
        migrations.RemoveField(
            model_name='dt_fields',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='dt_list',
            name='content_types',
        ),
        migrations.RemoveField(
            model_name='dt_list',
            name='creation_user',
        ),
        migrations.RemoveField(
            model_name='dt_list',
            name='modification_user',
        ),
        migrations.RemoveField(
            model_name='dt_list',
            name='owner',
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['order']},
        ),
        migrations.RenameField(
            model_name='agent',
            old_name='std_name',
            new_name='standard_name',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='attribute_type',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='attributereference',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='concept',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='content_attributes',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='content_class',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='content_type',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='countryreference',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='entity_phrase',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='headword',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='languagereference',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='object',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='object_attribute',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='page',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='place',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='rightspolicy',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='scope',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='set_x_content',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='source_pages',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='task',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='token',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='transcription',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='owner',
        ),
        migrations.AddField(
            model_name='agent',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attribute',
            name='value_JSON',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='content_attributes',
            name='unique',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='groupproperties',
            name='description',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='languagereference',
            name='lang_type',
            field=models.IntegerField(choices=[(1, 'Language'), (2, 'Dialect')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='primary_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AddField(
            model_name='source',
            name='is_private',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='source',
            name='primary_dataset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_query_name='set_members', to='dalme_app.set'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='value_TXT',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='attribute_type',
            name='data_type',
            field=models.CharField(choices=[('DATE', 'DATE (date)'), ('INT', 'INT (integer)'), ('STR', 'STR (string)'), ('TXT', 'TXT (text)'), ('FK-UUID', 'FK-UUID (DALME record)'), ('FK-INT', 'FK-INT (DALME record)')], max_length=15),
        ),
        migrations.AlterField(
            model_name='rightspolicy',
            name='rights_notice',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='dalme_app.source'),
        ),
        migrations.AlterUniqueTogether(
            name='source',
            unique_together={('type', 'name')},
        ),
        migrations.DeleteModel(
            name='DT_fields',
        ),
        migrations.DeleteModel(
            name='DT_list',
        ),
        migrations.AddField(
            model_name='source_credit',
            name='agent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credits', to='dalme_app.agent'),
        ),
        migrations.AddField(
            model_name='source_credit',
            name='creation_user',
            field=models.ForeignKey(default=dalme_app.models._templates.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dalme_app_source_credit_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='source_credit',
            name='modification_user',
            field=models.ForeignKey(default=dalme_app.models._templates.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dalme_app_source_credit_modification', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='source_credit',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credits', to='dalme_app.source'),
        ),
        migrations.AlterField(
            model_name='localereference',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dalme_app.countryreference'),
        ),
        migrations.AlterField(
            model_name='localereference',
            name='creation_user',
            field=models.ForeignKey(default=dalme_app.models._templates.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dalme_app_localereference_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='localereference',
            name='modification_user',
            field=models.ForeignKey(default=dalme_app.models._templates.get_current_user, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dalme_app_localereference_modification', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='localereference',
            unique_together={('name', 'administrative_region')},
        ),
    ]
