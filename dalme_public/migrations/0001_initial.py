# Generated by Django 2.2.4 on 2020-08-17 17:04

import dalme_public.blocks
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import taggit.managers
import wagtail.contrib.routable_page.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.core.models
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtail.images.models
import wagtail.search.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('dalme_app', '0146_auto_20200813_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('short_title', models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True)),
                ('body', wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('inline_image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('document', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock()), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock()), ('institution', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False))]))], null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='Collections',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('short_title', models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True)),
                ('body', wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('inline_image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('document', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock()), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock()), ('institution', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False))]))], null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='DALMEImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.images.models.get_upload_to, verbose_name='file', width_field='width')),
                ('width', models.IntegerField(editable=False, verbose_name='width')),
                ('height', models.IntegerField(editable=False, verbose_name='height')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('focal_point_x', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_y', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_width', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_height', models.PositiveIntegerField(blank=True, null=True)),
                ('file_size', models.PositiveIntegerField(editable=False, null=True)),
                ('file_hash', models.CharField(blank=True, editable=False, max_length=40)),
                ('caption', models.CharField(blank=True, max_length=255, null=True)),
                ('collection', models.ForeignKey(default=wagtail.core.models.get_root_collection_id, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Collection', verbose_name='collection')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags')),
                ('uploaded_by_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by user')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pages', wagtail.core.fields.StreamField([('page', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('page', wagtail.core.blocks.PageChooserBlock())]))], null=True)),
                ('copyright', models.CharField(blank=True, max_length=255, null=True)),
                ('social', wagtail.core.fields.StreamField([('social', wagtail.core.blocks.StructBlock([('fa_icon', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock())]))], null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('short_title', models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True)),
                ('body', wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('inline_image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('document', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock()), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock()), ('institution', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False))]))], null=True)),
                ('header_image', models.ForeignKey(blank=True, help_text='The image that will display in the header.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='dalme_public.DALMEImage')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('short_title', models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True)),
                ('body', wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('inline_image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('document', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock()), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock()), ('institution', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False))]))], null=True)),
                ('sponsors', wagtail.core.fields.StreamField([('sponsors', wagtail.core.blocks.StructBlock([('logo', wagtail.images.blocks.ImageChooserBlock()), ('url', wagtail.core.blocks.URLBlock())]))], null=True)),
                ('header_image', models.ForeignKey(blank=True, help_text='The image that will display in the header.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='dalme_public.DALMEImage')),
                ('learn_more_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('short_title', models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True)),
                ('body', wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('inline_image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('document', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock()), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock()), ('institution', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False))]))], null=True)),
                ('show_contact_form', models.BooleanField(default=False, help_text='Check this box to show a contact form on the page.')),
                ('header_image', models.ForeignKey(blank=True, help_text='The image that will display in the header.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='dalme_public.DALMEImage')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Features',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('short_title', models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True)),
                ('body', wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('inline_image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('document', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock()), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock()), ('institution', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False))]))], null=True)),
                ('header_image', models.ForeignKey(blank=True, help_text='The image that will display in the header.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='dalme_public.DALMEImage')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FeaturedObject',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('inline_image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('document', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock()), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock()), ('institution', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False))]))], null=True)),
                ('alternate_author', models.CharField(blank=True, help_text='An optional name field that will be displayed as the author of this page instead of the user who created it.', max_length=127, null=True)),
                ('header_image', models.ForeignKey(blank=True, help_text='The image that will display in the header.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='dalme_public.DALMEImage')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='featured_objects', to='dalme_app.Source')),
                ('source_set', models.ForeignKey(blank=True, help_text='Optional, select a particular public set for the source associated with this object. The source must be a member of the set chosen or the page will not validate.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='featured_objects', to='dalme_app.Set')),
            ],
            options={
                'verbose_name': 'Object',
                'verbose_name_plural': 'Objects',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FeaturedInventory',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('inline_image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('document', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock()), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock()), ('institution', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False))]))], null=True)),
                ('alternate_author', models.CharField(blank=True, help_text='An optional name field that will be displayed as the author of this page instead of the user who created it.', max_length=127, null=True)),
                ('header_image', models.ForeignKey(blank=True, help_text='The image that will display in the header.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='dalme_public.DALMEImage')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='featured_inventories', to='dalme_app.Source')),
                ('source_set', models.ForeignKey(blank=True, help_text='Optional, select a particular public set for the source associated with this inventory. The source must be a member of the set chosen or the page will not validate.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='featured_inventories', to='dalme_app.Set')),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventories',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Essay',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('inline_image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('document', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock()), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock()), ('institution', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False))]))], null=True)),
                ('alternate_author', models.CharField(blank=True, help_text='An optional name field that will be displayed as the author of this page instead of the user who created it.', max_length=127, null=True)),
                ('header_image', models.ForeignKey(blank=True, help_text='The image that will display in the header.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='dalme_public.DALMEImage')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='essays', to='dalme_app.Source')),
                ('source_set', models.ForeignKey(blank=True, help_text='Optional, select a particular public set for the source associated with this essay. The source must be a member of the set chosen or the page will not validate.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='essays', to='dalme_app.Set')),
            ],
            options={
                'verbose_name': 'Mini Essay',
                'verbose_name_plural': 'Mini Essays',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title', models.CharField(max_length=255)),
                ('description', wagtail.core.fields.RichTextField()),
                ('collections', modelcluster.fields.ParentalManyToManyField(related_name='corpora', to='dalme_public.Collection')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='corpora', to='dalme_public.Collections')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='collections',
            name='header_image',
            field=models.ForeignKey(blank=True, help_text='The image that will display in the header.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='dalme_public.DALMEImage'),
        ),
        migrations.AddField(
            model_name='collection',
            name='header_image',
            field=models.ForeignKey(blank=True, help_text='The image that will display in the header.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='dalme_public.DALMEImage'),
        ),
        migrations.AddField(
            model_name='collection',
            name='source_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='public_collections', to='dalme_app.Set'),
        ),
        migrations.CreateModel(
            name='CustomRendition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_spec', models.CharField(db_index=True, max_length=255)),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.images.models.get_rendition_upload_to, width_field='width')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(blank=True, default='', editable=False, max_length=16)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renditions', to='dalme_public.DALMEImage')),
            ],
            options={
                'unique_together': {('image', 'filter_spec', 'focal_point_key')},
            },
        ),
    ]
