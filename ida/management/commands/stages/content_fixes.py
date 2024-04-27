"""Create entries necessary for new data schemas."""

import copy
import json
import os
import re
import uuid
from functools import cached_property

import markdown
from bs4 import BeautifulSoup
from django_tenants.utils import schema_context
from wagtail.log_actions import log

from django.apps import apps
from django.db import connection, transaction

from ida.models import (
    Project,
    SavedSearch,
    Tenant,
    ZoteroCollection,
)

from .base import BaseStage

REFERENCE_HREF = re.compile(r'(?:(?:http|https)://dalme.org)?/?/project/bibliography/#([A-Z0-9]{8})')

REF_CITATIONS = {
    '6YDI5HL6': '(Smith, 2020)',
    'WJLVYXYP': '(Sibon, 2011)',
    'LYJR5IHM': '(Coulet, 2004)',
    'TS749RWH': '(Baratier, 1961)',
    '6NUFKTEG': '(Mély & Bishop, 1892)',
    'F2FFVVX8': '(Volkert, 1982)',
    '3GJ5F9HJ': '(Coulet, 2004)',
    'ER34URS8': '(Le Roux de Lincy, 1846)',
    '5QK2S98X': '(Barnel, 1999)',
    'L9ALQFNF': '(Ripert, Barnel, Bresc, Herbeth, & Colin, 1993)',
    'BZ53KGMW': '(Stouff, 1996)',
    'IFRJ2YQ6': '(Smail, Pizzorno, & Hay, 2020)',
    'UH5EUVZC': '(Villard, 1907)',
    'NY7H8NIH': '(Ferrand, 2017)',
    'DBB2IVEC': '(Livi, 1928)',
    'SA6QKDAR': '(Longhi, 2020)',
    'YX4Y4RRJ': '(Barry, 1898)',
    'XAQBR8XE': '(Teaching Medieval Slavery and Captivity, n.d.)',
    'VZQ5BBTG': '(Origo, 1955)',
    'JHH4LIGY': '(Fernandes, Liberato, Marques, & Cunha, 2017)',
    '6VZUI7JY': '(Oliver, 2016)',
    'ZZXGLVMZ': '(Rigaud, 1996)',
    'ZUMTQ5B9': '(Reitzel, 1980)',
    '2RUWVY7B': '(Howell, 1996)',
    'SNB4JFJ9': '(Braun, 1907)',
    'SBBLYP96': '(Davril, Thibodeau, & Guyot, 1995)',
    'TNEXXNIQ': '(Braun, 1937)',
    'UCVN8LWL': '(Miller, 2014)',
    'TQVX23W6': '(Berthod, 2001)',
    'QZNHF7Q3': '(Piponnier, 1989)',
    'Q62RN9ND': '(Fircks, 2018)',
    'TBIJ9DYD': '(Deregnaucourt, 1981)',
    'J9BYMBP2': '(Deregnaucourt, 1982)',
    'Y44RIA8Q': '(Mane & Piponnier, 1992)',
    'XL9F9RTZ': '(Carroll-Clark, 2005)',
    'MJWEGUKG': '(Blaschitz, Hundsbichler, Jaritz, & Vavra, 1992)',
    'XXD7JM9D': '(Baumgarten, 2014)',
}


class Stage(BaseStage):
    """Fixes after finishing all data migrations."""

    name = '11 Content fixes'
    FN_REGISTER = {}  # register to keep track of footnote indices

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.adjust_id_columns()
        self.create_project_and_library_entries()
        self.content_conversions()
        self.update_footnote_state()
        self.fix_biblio_page()
        self.migrate_people()
        self.process_images()

    @transaction.atomic
    def adjust_id_columns(self):
        """Adjust autogenerated id sequences."""
        app_labels = [
            'taggit',
            'wagtailadmin',
            'wagtailcore',
            'wagtaildocs',
            'wagtailembeds',
            'wagtailforms',
            'wagtailimages',
            'wagtailredirects',
            'wagtailusers',
            'public',
        ]

        for label in app_labels:
            self.logger.info('Processing "%s" models', label)
            app_config = apps.get_app_config(label)
            if app_config.models_module is not None:
                for model in app_config.get_models():
                    model_name = model.__name__.lower()
                    qualified_name = f'{label}_{model_name}'
                    self.logger.info('Copying "%s"', qualified_name)

                    with connection.cursor() as cursor:
                        cursor.execute(f'SELECT * FROM dalme.{qualified_name};')
                        rows = self.map_rows(cursor)
                        id_list = [int(row['id']) for row in rows if row.get('id')]
                        if id_list:
                            new_seq_start = max(id_list) + 1
                            cursor.execute(
                                f'ALTER TABLE dalme.{qualified_name} ALTER COLUMN id RESTART WITH {new_seq_start};'
                            )

    @transaction.atomic
    def create_project_and_library_entries(self):
        # DALME
        self.logger.info('Creating project and library entries for DALME')
        collections = [
            {
                'id': 'A4QHN348',
                'label': 'Editions',
                'has_biblio_sources': True,
            },
            {
                'id': 'BKW2PVCM',
                'label': 'Glossaries and dictionaries',
                'has_biblio_sources': False,
            },
            {
                'id': 'QM9AZNT3',
                'label': 'Methodology',
                'has_biblio_sources': False,
            },
            {
                'id': 'SLIT6LID',
                'label': 'Studies',
                'has_biblio_sources': False,
            },
            {
                'id': 'FRLVXUWL',
                'label': 'Other resources',
                'has_biblio_sources': False,
            },
        ]
        tenant = Tenant.objects.get(name='DALME')
        new_project = Project.objects.create(
            name='DALME',
            description='The Documentary Archaeology of Late Medieval Europe',
            zotero_library_id=int(os.environ['ZOTERO_LIBRARY_ID']),
            zotero_api_key=os.environ['ZOTERO_API_KEY'],
            tenant=tenant,
        )

        for collection in collections:
            collection.update(project=new_project)
            z_col = ZoteroCollection.objects.create(**collection)

            with schema_context('dalme'):
                log(instance=z_col, action='wagtail.create')

        # GP
        self.logger.info('Creating project and library entries for GP')
        tenant = Tenant.objects.get(name='Pharmacopeias')
        new_project = Project.objects.create(
            name='Pharmacopeias',
            description='Pharmacopeias',
            zotero_library_id=int(os.environ['ZOTERO_LIBRARY_ID_GP']),
            zotero_api_key=os.environ['ZOTERO_API_KEY_GP'],
            tenant=tenant,
        )

    # FIX JSON CONTENT - UTILITY FUNCTIONS

    def markdown_to_html(self, content):
        # <span data-footnote=\"For Bons-Enfants, houses of poor grammar-school students attested across northern France and francophone Flanders (as Douai),
        # Joan M. Reitzel, &quot;[The Medieval House of Bons-Enfants](http://dalme.org/project/bibliography/#ZUMTQ5B9),&quot; _Viator_ 11 (1980): 179-207.\"
        # data-note_id=\"1fe36ff5-2e03-4890-82b1-71090d6333d7\">✱</span>
        soup = BeautifulSoup(markdown.markdown(content), features='lxml')
        references = soup.find_all('a', href=REFERENCE_HREF)
        if references:
            soup = self.convert_references(soup)

        return ''.join(str(b) for b in soup.body.findChildren(recursive=False))

    def convert_references(self, soup):
        for ref in soup.find_all('a', href=REFERENCE_HREF):
            # format: <a data-biblio="54" data-id="R476GUY2" data-reference="(Telliez, 2011)" linktype="reference">consumption</a>
            match = REFERENCE_HREF.fullmatch(ref['href'])
            if match:
                ref['data-biblio'] = self.biblio_page_id
                ref_id = match.group(1)
                try:
                    citation = REF_CITATIONS[ref_id]
                except KeyError:
                    citation = ''
                    self.logger.info('Reference id: %s not in citation list!', ref_id)
                ref['data-id'] = ref_id
                ref['data-reference'] = citation  # TODO: figure out a better way to get the citation!
                ref['linktype'] = 'reference'
                del ref['href']

        return soup

    def fix_entities(self, text, obj, is_rev=False):
        soup = BeautifulSoup(text, features='lxml')

        # references
        references = soup.find_all('a', href=REFERENCE_HREF)
        if references:
            soup = self.convert_references(soup)

        # footnotes
        footnotes = soup.find_all('span', attrs={'data-footnote': True})
        if footnotes:
            with schema_context('dalme'):
                from wagtail.models import Page

                from public.extensions.footnotes.models import Footnote

                page = obj if isinstance(obj, Page) else obj.content_object
                fn_index = self.FN_REGISTER.get(page.id, 1)

                for idx, fn in enumerate(footnotes, start=fn_index):
                    # format: <a data-footnote="c847f9da-3780-4085-9426-73e7a0228b3d" linktype="footnote">✱</a>
                    fn_content = self.markdown_to_html(fn['data-footnote'])

                    if is_rev:
                        # we don't create footnote records for page revisions as they would be repeats
                        # of notes that already exist in the live pages
                        fn_record = Footnote.objects.filter(text=fn_content, page=page)
                        if fn_record.exists() and fn_record.count() == 1:
                            fn['data-footnote'] = fn_record.first().id
                        else:
                            fn['data-footnote'] = True
                    else:
                        new_footnote = Footnote.objects.create(
                            id=uuid.uuid4(),
                            page=page,
                            text=fn_content,
                            sort_order=idx,
                        )
                        fn['data-footnote'] = new_footnote.id

                    self.FN_REGISTER[page.id] = idx  # update footnote index for page with last used one
                    fn.name = 'a'
                    fn['linktype'] = 'footnote'
                    del fn['data-note_id']

                self.FN_REGISTER[page.id] += 1  # increment last index by one for next run

        # saved searches
        # source format: <a id="01d5187e-2752-466e-9e7d-64e51051facd" linktype="saved_search">storage</a>
        # target format: <a id="01d5187e-2752-466e-9e7d-64e51051facd" data-saved-search="pansier" linktype="saved_search">dissemination</a>
        saved_searches = soup.find_all('a', attrs={'linktype': 'saved_search'})
        if saved_searches:
            for ss in saved_searches:
                try:
                    search_obj = SavedSearch.objects.get(pk=ss['id'])
                    ss['data-saved-search'] = search_obj.name
                except:  # noqa: E722
                    self.logger.info('Failed to migrate saved search entity in page %s', obj.id)

        return ''.join(str(b) for b in soup.body.findChildren(recursive=False))

    def parse_streamfield(self, content, obj, is_rev=False):  # noqa: C901, PLR0912, PLR0915
        """We parse streamfields to convert the old subsection blocks into the new nested system."""
        new_content = []
        subsection = None
        nested_subsection = None
        for sblock in content:
            block = copy.deepcopy(sblock)
            if block.get('type') in ['subsection', 'subsection_end_marker']:
                if block.get('value', {}).get('minor_heading'):
                    block['type'] = 'nested_subsection'
                    if nested_subsection is None:
                        nested_subsection = block
                    else:
                        if subsection:
                            if not subsection['value'].get('body'):
                                subsection['value']['body'] = [nested_subsection]
                            else:
                                subsection['value']['body'].append(nested_subsection)
                        else:
                            new_content.append(nested_subsection)
                        nested_subsection = block
                else:
                    if nested_subsection:
                        if subsection:
                            if not subsection['value'].get('body'):
                                subsection['value']['body'] = [nested_subsection]
                            else:
                                subsection['value']['body'].append(nested_subsection)
                        else:
                            new_content.append(nested_subsection)

                        nested_subsection = None

                    if subsection:
                        new_content.append(subsection)

                    subsection = block if block.get('type') == 'subsection' else None
            else:
                if block.get('type') == 'text' and block.get('value'):
                    block['value'] = self.fix_entities(block['value'], obj, is_rev=is_rev)

                if nested_subsection:
                    if not nested_subsection['value'].get('body'):
                        nested_subsection['value']['body'] = [block]
                    else:
                        nested_subsection['value']['body'].append(block)

                elif subsection:
                    if not subsection['value'].get('body'):
                        subsection['value']['body'] = [block]
                    else:
                        subsection['value']['body'].append(block)

                else:
                    new_content.append(block)

        if nested_subsection:
            if subsection:
                if not subsection['value'].get('body'):
                    subsection['value']['body'] = [nested_subsection]
                else:
                    subsection['value']['body'].append(nested_subsection)
            else:
                new_content.append(nested_subsection)

        if subsection:
            new_content.append(subsection)

        return new_content

    def process_content_field(self, field_value, field_type, obj):
        if field_type == 'JSONField':
            is_rev = isinstance(field_value, dict)
            content = json.loads(field_value['body']) if is_rev else field_value.get_prep_value()
            new_content = self.parse_streamfield(content, obj, is_rev=is_rev)

            if is_rev:
                field_value['body'] = json.dumps(new_content)
            else:
                field_value = field_value.stream_block.to_python(new_content)

        else:
            field_value = self.fix_entities(field_value, obj)

        return field_value

    @cached_property
    def biblio_page_id(self):
        with schema_context('dalme'):
            from public.models import Bibliography

            return Bibliography.objects.first().page_ptr_id

    @transaction.atomic
    def content_conversions(self):
        """Convert content between old and new formats (footnotes, references, people/team members)."""
        targets = {
            'public': [
                'collection',
                'collections',
                'essay',
                'featuredinventory',
                'featuredobject',
                'features',
                'flat',
            ],
            'wagtailcore': ['revision'],
        }

        for app_label, models in targets.items():
            for model_name in models:
                qualified_name = f'{app_label}_{model_name}'
                self.logger.info('Processing "%s"', qualified_name)
                with schema_context('dalme'):
                    model = apps.get_model(app_label=app_label, model_name=model_name)
                    target_fields = self.get_fields_by_type(model, ['JSONField', 'RichTextField'], as_map=True)
                    self.logger.info(
                        'Targetting: %s JSONField | %s Other',
                        len([f for f in target_fields if f[1] == 'JSONField']),
                        len([f for f in target_fields if f[1] != 'JSONField']),
                    )
                    for instance in model.objects.all():
                        updated_fields = []
                        for field_name, field_type in target_fields:
                            field_value = getattr(instance, field_name, None)
                            if field_value:
                                updated_fields.append(field_name)
                                setattr(
                                    instance, field_name, self.process_content_field(field_value, field_type, instance)
                                )

                        instance.save(update_fields=updated_fields)

    @transaction.atomic
    def update_footnote_state(self):
        """Update footnote state fields for pages."""
        targets = [
            'collection',
            'collections',
            'essay',
            'featuredinventory',
            'featuredobject',
            'features',
            'flat',
        ]

        for model_name in targets:
            qualified_name = f'public_{model_name}'
            self.logger.info('Processing "%s"', qualified_name)
            with schema_context('dalme'):
                model = apps.get_model(app_label='public', model_name=model_name)
                for instance in model.objects.all():
                    raw_content = str(instance.body.raw_data)
                    instance.has_footnotes = 'data-footnote=' in raw_content
                    instance.has_placemarker = 'footnotes_placemarker' in raw_content
                    instance.save(update_fields=['has_footnotes', 'has_placemarker'])

    @transaction.atomic
    def fix_biblio_page(self):
        """Fix collection block references in bibliography page."""
        with schema_context('dalme'):
            from public.models import Bibliography

            biblio_page = Bibliography.objects.first()
            body = biblio_page.body.get_prep_value()
            for block in body:
                if block.get('type') == 'bibliography':
                    block['value'] = block['value']['collection']

            biblio_page.body = body
            biblio_page.save(update_fields=['body'])

    @transaction.atomic
    def migrate_people(self):
        """Convert people blocks to TeamMember entities."""
        with schema_context('dalme'):
            from wagtail.models import Page

            from public.extensions.team.models import TeamMember, TeamRole

            roles = {
                'PI': TeamRole.objects.create(
                    role='PI',
                    description='DALME Principal Investigator.',
                ),
                'Project Team': TeamRole.objects.create(
                    role='Core',
                    description='Member of the core project team.',
                ),
                'Contributors': TeamRole.objects.create(
                    role='Contributor',
                    description='Occasional contributor to the project.',
                ),
                'Advisory Board': TeamRole.objects.create(
                    role='Board',
                    description='Member of the DALME Advisory Board.',
                ),
            }

            people_page = Page.objects.get(title='People').specific

            for block in people_page.body:
                current_role = None
                if block.block_type == 'subsection':
                    block_value = block.block.get_prep_value(block.value)
                    current_role = roles.get(block_value.get('subsection'))

                    for sub_block in block_value['body']:
                        if sub_block.get('type') == 'person':
                            sub_block_value = sub_block.get('value')
                            tm = TeamMember.objects.create(
                                name=sub_block_value.get('name'),
                                title=sub_block_value.get('job'),
                                affiliation=sub_block_value.get('institution'),
                                url=sub_block_value.get('url'),
                                photo_id=sub_block_value.get('photo'),
                            )
                            tm.roles.add(current_role)
                            log(instance=tm, action='wagtail.create')

    @transaction.atomic
    def process_images(self):
        """Apply feature recognition to images and get rendition for people."""
        with schema_context('dalme'):
            from wagtail.images import get_image_model

            Image = get_image_model()  # noqa: N806

            for image in Image.objects.all():
                try:
                    if not image.has_focal_point():
                        image.set_focal_point(image.get_suggested_focal_point())
                        image.save()
                        image.get_rendition('fill-100x100')
                except:  # noqa: E722
                    pass
