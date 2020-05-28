import textwrap

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, F, Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse

from bs4 import BeautifulSoup as BSoup
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks, hooks
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtailmodelchooser import register_model_chooser, Chooser
from wagtailmodelchooser.edit_handlers import ModelChooserPanel

from dalme_app.models import Set as DALMESet, Source
from dalme_app.serializers import SourceSerializer
from dalme_public import forms
from dalme_public.blocks import (
    DocumentBlock,
    ExternalResourceBlock,
    IFrameBlock,
    PersonBlock,
    SubsectionBlock,
)


# https://github.com/django/django/blob/3bc4240d979812bd11365ede04c028ea13fdc8c6/django/urls/converters.py#L26
UUID_RE = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


@hooks.register('before_serve_page')
def redirects(page, request, serve_args, serve_kwargs):
    if page.is_root():
        home = page.get_children().live().first()
        return redirect(home.url, permanent=False)
    if page._meta.label == 'dalme_public.Section':
        return redirect(page.get_children().live().first().url, permanent=False)


@register_model_chooser
class SourceChooser(Chooser):
    model = Source

    def get_queryset(self, request):
        qs = super().get_queryset(request).order_by('name')
        if request.GET.get('q'):
            # TODO: OR this with an ID filter
            qs = qs.filter(name__icontains=request.GET['q'])
        return qs


class DALMEImage(AbstractImage):
    caption = models.CharField(max_length=255, null=True, blank=True)

    admin_form_fields = Image.admin_form_fields + ('caption',)


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        DALMEImage, on_delete=models.CASCADE, related_name='renditions'
    )

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )

class CarouselMixin(Orderable):
    carousel_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [ImageChooserPanel('carousel_image')]


class DALMEPage(Page):
    header_image = models.ForeignKey(
        'dalme_public.DALMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The image that will display in the header.'
    )
    short_title = models.CharField(
        max_length=63,
        null=True,
        blank=True,
        help_text='An optional short title that will be displayed in certain contexts.'
    )
    body = StreamField([
        ('main_image', ImageChooserBlock()),
        ('inline_image', ImageChooserBlock()),   # pull left and right?
        ('text', blocks.RichTextBlock()),
        ('heading', blocks.CharBlock()),
        ('pullquote', blocks.RichTextBlock(icon='openquote')),
        ('document', DocumentBlock()),
        ('person', PersonBlock()),
        ('external_resource', ExternalResourceBlock()),
        ('embed', EmbedBlock(icon='media')),
        ('iframe', IFrameBlock()),
        ('subsection', SubsectionBlock()),
    ])

    class Meta:
        abstract = True

    @property
    def main_image(self):
        try:
            return self.carousel.first().carousel_image
        except AttributeError:
            try:
                return next(
                    field for field in self.body
                    if field.block.name == 'main_image'
                ).value
            except StopIteration:
                return None

    @property
    def title_switch(self):
        """Utility to reduce OR coalescing in templates.
        Prefer the short_title if a Page has one, if not fallback to title.
        """
        try:
            return self.short_title or self.title
        except AttributeError:
            return self.title


class FeaturedPage(DALMEPage):
    @property
    def author(self):
        return f'{self.owner.first_name} {self.owner.last_name}'

    @property
    def nav_title(self):
        return self._meta.verbose_name_plural

    @property
    def snippet(self):
        try:
            text = next(
                field for field in self.body
                if field.block.name == 'text'
            )
        except StopIteration:
            return ''
        return textwrap.shorten(
            BSoup(text.value.source, 'html.parser').get_text(),
            width=300,
            placeholder=' [...]'
        )

    class Meta:
        abstract = True


class Home(DALMEPage):
    subpage_types = [
        'dalme_public.Section',
        'dalme_public.Features',
        'dalme_public.Collections'
    ]

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['featured_object'] = FeaturedObject.objects.live().last()
        context['featured_inventory'] = FeaturedInventory.objects.live().last()
        context['essay'] = Essay.objects.live().last()
        return context


class Section(DALMEPage):
    parent_page_types = ['dalme_public.Home']
    subpage_types = ['dalme_public.Flat']

    content_panels = DALMEPage.content_panels + [
        FieldPanel('short_title'),
    ]


class Flat(DALMEPage):
    show_contact_form = models.BooleanField(
        default=False,
        help_text='Check this box to show a contact form on the page.'
    )

    parent_page_types = ['dalme_public.Section']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('title'),
        FieldPanel('short_title'),
        FieldPanel('show_contact_form'),
        StreamFieldPanel('body'),
    ]

    def serve(self, request):
        if self.show_contact_form:
            form = forms.ContactForm(label_suffix='')
            if request.method == 'POST':
                form = forms.ContactForm(request.POST, label_suffix='')
                if form.is_valid():
                    form.save()
                    messages.success(
                        request, 'Your message has been delivered.'
                    )
                    return HttpResponseRedirect(self.url)
            return render(
                request, 'dalme_public/flat.html', {'page': self, 'form': form}
            )
        return super().serve(request)


class Features(DALMEPage):
    parent_page_types = ['dalme_public.Home']
    subpage_types = [
        'dalme_public.FeaturedObject',
        'dalme_public.FeaturedInventory',
        'dalme_public.Essay'
    ]

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('short_title'),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        from dalme_public.filters import FeaturedFilter
        context = super().get_context(request)
        filtered = FeaturedFilter(
            request.GET,
            queryset=self.get_children().live().specific()
        )
        context['featured'] = filtered.qs
        return context


class FeaturedObjectCarousel(CarouselMixin):
    page = ParentalKey('dalme_public.FeaturedObject', related_name='carousel')


class FeaturedObject(FeaturedPage):
    short_title = 'Object'
    source = models.ForeignKey(
        'dalme_app.Source',
        related_name='featured_objects',
        on_delete=models.PROTECT
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        ModelChooserPanel('source'),
        MultiFieldPanel(
            [InlinePanel('carousel', label='Image')],
            heading='Carousel Images',
        ),
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Object'
        verbose_name_plural = 'Objects'


class FeaturedInventory(FeaturedPage):
    short_title = 'Inventory'
    source = models.ForeignKey(
        'dalme_app.Source',
        related_name='featured_inventories',
        on_delete=models.PROTECT
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        ModelChooserPanel('source'),
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'


class Essay(FeaturedPage):
    short_title = 'Essay'
    source = models.ForeignKey(
        'dalme_app.Source',
        related_name='essays',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    parent_page_types = ['dalme_public.Features']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('source'),
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Mini Essay'
        verbose_name_plural = 'Mini Essays'


class Collection(Orderable, ClusterableModel):
    title = models.CharField(max_length=255)
    description = RichTextField()

    page = ParentalKey('dalme_public.Collections', related_name='collections')
    sets = ParentalManyToManyField('dalme_public.Set')

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('sets')
    ]


class Collections(DALMEPage):
    parent_page_types = ['dalme_public.Home']
    subpage_types = ['dalme_public.Set']

    content_panels = DALMEPage.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('short_title'),
        StreamFieldPanel('body'),
        MultiFieldPanel(
            [InlinePanel('collections', min_num=1, label='Collection')],
            heading='Collections',
        ),
    ]


class Set(RoutablePageMixin, DALMEPage):
    set_type = DALMESet.COLLECTION
    source_set = models.ForeignKey(
        'dalme_app.Set',
        related_name='public_sets',
        on_delete=models.PROTECT
    )

    parent_page_types = ['dalme_public.Collections']
    subpage_types = []

    content_panels = DALMEPage.content_panels + [
        FieldPanel('source_set'),
        ImageChooserPanel('header_image'),
        StreamFieldPanel('body'),
    ]

    @route(r'^inventories/$', name='inventories')
    def inventories(self, request):
        context = self.get_context(request)
        context.update({
            'inventories': True,
            'set_id': self.source_set.id,
        })
        return TemplateResponse(
          request, 'dalme_public/inventories.html', context
        )

    @route(rf'^inventories/({UUID_RE})/$', name='inventory')
    def inventory(self, request, pk):
        qs = Source.objects.filter(pk=pk)
        if not qs.exists():
            raise Http404()

        qs = qs.annotate(
            no_folios=Count('pages', filter=Q(pages__source__isnull=False))
        )
        source = qs.first()
        pages = source.source_pages.all().values(
            pageId=F('page__pk'),
            pageName=F('page__name'),
            transcriptionId=F('transcription__pk')
        )

        context = self.get_context(request)
        context.update({
            'inventory': True,
            'set_id': self.source_set.id,
            'title': source.name,
            'data': {
                'folios': list(pages),
                **SourceSerializer(source).data,
            },
        })
        return TemplateResponse(
          request, 'dalme_public/inventory.html', context
        )

    @property
    def count(self):
        return self.source_set.get_member_count

    @property
    def alias_type(self):
        try:
            return self.source_set.set_type
        except AttributeError:
            return None

    @property
    def sources(self):
        return self.source_set.members.all()

    def clean(self):
        if self.alias_type is not None and self.set_type != self.alias_type:
            mismatch = f'{self.set_type} != {self.alias_type}'
            raise ValidationError(
                f'{self._meta.model.__name__}.set_type mismatch: {mismatch}'
            )
        return super().clean()
