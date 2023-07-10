from dalme_app.models import Folio, Record

from .attributes import AttributeSerializer
from .base_classes import DynamicSerializer
from .page import PageSerializer
from .transcriptions import TranscriptionSerializer
from .users import UserSerializer
from .workflows import WorkflowSerializer


class RecordFolioSerializer(DynamicSerializer):
    """Serializer for Folios."""

    page = PageSerializer()
    transcription = TranscriptionSerializer()

    class Meta:  # noqa: D106
        model = Folio
        fields = ('id', 'page', 'transcription', 'page_data')


class RecordSerializer(DynamicSerializer):
    """Serializer for records."""

    attributes = AttributeSerializer(many=True, required=False)
    workflow = WorkflowSerializer(required=False)
    pages = PageSerializer(many=True, required=False)
    owner = UserSerializer(field_set='attribute', required=False)
    creation_user = UserSerializer(field_set='attribute', required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)
    folios = RecordFolioSerializer(many=True, fields=['page_data'], required=False)

    class Meta:  # noqa: D106
        model = Record
        fields = [
            'id',
            'name',
            'short_name',
            # 'parent',
            'owner',
            'attributes',
            'no_folios',
            'no_images',
            'workflow',
            'pages',
            'is_private',
            'comment_count',
            'folios',
            'creation_timestamp',
            'creation_user',
            'modification_timestamp',
            'modification_user',
        ]
        field_sets = {
            'collection_member': [
                'id',
                'name',
            ],
            'option': [
                'id',
                'name',
            ],
            'attribute': [
                'id',
                'name',
                'short_name',
            ],
        }


# class BackupRecordSerializer(DynamicSerializer):
#     """Serializer for sources."""

#     attributes = AttributeSerializer(many=True, required=False)
#     inherited = AttributeSerializer(many=True, required=False)
#     workflow = WorkflowSerializer(required=False)
#     pages = PageSerializer(many=True, required=False)
#     owner = UserSerializer(fields=['full_name', 'username', 'id'])
#     # credits = RecordCreditSerializer(many=True, required=False)
#     comment_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Record
#         fields = (
#             'id',
#             'type',
#             'name',
#             'short_name',
#             'parent',
#             'has_inventory',
#             'attributes',
#             'inherited',
#             # 'credits',
#             'no_folios',
#             'no_images',
#             'workflow',
#             'owner',
#             'pages',
#             'no_records',
#             'is_private',
#             'comment_count',
#         )
#         extra_kwargs = {
#             'parent': {'required': False},
#             'no_folios': {'required': False},
#             'no_images': {'required': False},
#             'comment_count': {'required': False},
#         }

#     def get_comment_count(self, obj):
#         return obj.comments.count()

#     def to_representation(self, instance):
#         ret = super().to_representation(instance)

#         if ret.get('attributes') is not None:
#             ret['attributes'] = self.process_attributes(instance.type, ret.pop('attributes'))

#         if ret.get('inherited') is not None and ret['inherited'] is not None:
#             ret['inherited'] = self.process_attributes(instance.type, ret.pop('inherited'))

#         if ret.get('parent') is not None:
#             ret['parent'] = {'id': instance.parent.id, 'name': instance.parent.name}

#         if instance.agents():
#             agents = []
#             for agent in instance.agents():
#                 lp = agent.attributes.filter(attribute_type=150)
#                 agents.append(
#                     {
#                         'id': agent.id,
#                         'name': agent.content_object.standard_name,
#                         'type': agent.content_object.get_type_display(),
#                         'legal_persona': lp.first().value_STR if lp.exists() else 'Unknown',
#                     },
#                 )
#             ret['agents'] = agents

#         if instance.children.exists():
#             children = []
#             for child in instance.children.all():
#                 children.append(
#                     {
#                         'id': child.id,
#                         'name': child.name,
#                         'short_name': child.short_name,
#                         'type': child.type.name,
#                         'has_inventory': child.has_inventory,
#                     },
#                 )
#             ret['children'] = children

#         if instance.pages.exists():
#             ret['pages'] = self.get_folios(instance)

#         if instance.places():
#             places = []
#             for place in instance.places():
#                 locale = f'{place.locale.name}, {place.locale.administrative_region}'
#                 if place.locale.latitude and place.locale.longitude:
#                     locale += f' ({place.locale.latitude}, {place.locale.longitude})'
#                 places.append(
#                     {
#                         'id': place.id,
#                         'placename': place.standard_name,
#                         'locale': locale,
#                     },
#                 )
#             ret['places'] = places

#         ret['created'] = {
#             'timestamp': timezone.localtime(
#                 instance.creation_timestamp,
#             ).strftime('%d-%b-%Y@%H:%M'),
#             'username': instance.creation_user.username,
#             'user': instance.creation_user.profile.full_name,
#         }
#         ret['modified'] = {
#             'timestamp': timezone.localtime(
#                 instance.modification_timestamp,
#             ).strftime('%d-%b-%Y@%H:%M'),
#             'username': instance.modification_user.username,
#             'user': instance.modification_user.profile.full_name,
#         }

#         ret['type'] = {
#             'name': instance.type.name,
#             'id': instance.type.id,
#         }

#         return {key: value for key, value in ret.items() if value is not None}

#     def to_internal_value(self, data):
#         for name in ['type', 'parent']:
#             if data.get(name) is not None:
#                 data[name] = data[name]['id']

#         if data.get('attributes'):
#             _type = data.get('type', False) or self.instance.type
#             data['attributes'] = self.process_attributes(_type, data['attributes'])

#         workflow = data.get('workflow', {})
#         if workflow.get('status') is not None:
#             if workflow['status']['text'] is not None:
#                 for key, value in translate_workflow_string(workflow['status']['text']).items():
#                     data['workflow'][key] = value
#             else:
#                 workflow.pop('status')

#         if data.get('credits') is not None and not data.get('credits'):
#             data.pop('credits')

#         data['owner'] = {'id': data.get('owner', {}).get('id', get_current_user().id)}
#         data['owner']['username'] = User.objects.get(pk=data['owner']['id']).username

#         return super().to_internal_value(data)

#     def run_validation(self, data):
#         if data.get('type') is not None:
#             required_dict = {
#                 12: [
#                     'name',
#                     'short_name',
#                     'parent',
#                     'primary_dataset',
#                     'attributes.authority',
#                     'attributes.format',
#                     'attributes.support',
#                 ],
#                 13: ['name', 'short_name', 'parent', 'has_inventory', 'attributes.record_type', 'attributes.language'],
#                 19: ['name', 'short_name', 'attributes.locale'],
#             }
#             required = required_dict.get(data['type']['id'], ['name', 'short_name'])
#             missing = {}
#             for field in required:
#                 group, field = field.split('.') if '.' in field else (None, field)
#                 if data.get(group, data).get(field) in [None, '', 0]:
#                     missing[field] = ['This field is required.']

#             if len(missing):
#                 raise serializers.ValidationError(missing)
#             else:
#                 validated_data = super().run_validation(data)

#                 if validated_data.get('owner') is not None:
#                     validated_data['owner'] = User.objects.get(
#                         username=validated_data['owner']['username'],
#                     )
#         else:
#             raise serializers.ValidationError({'non_field_errors': ['Type information missing.']})

#         return validated_data

#     def create(self, validated_data):
#         attributes = validated_data.pop('attributes', None)
#         workflow = validated_data.pop('workflow', None)
#         pages = validated_data.pop('pages', None)
#         validated_data.pop('credits', None)

#         source = Record.objects.create(**validated_data)

#         self.update_or_create_attributes(source, attributes)
#         self.update_or_create_workflow(source, workflow)
#         self.update_or_create_pages(source, pages)
#         # self.update_or_create_credits(source, credits)

#         return source

#     def update(self, instance, validated_data):
#         self.update_or_create_attributes(instance, validated_data.pop('attributes', None))
#         self.update_or_create_workflow(instance, validated_data.pop('workflow', None))
#         self.update_or_create_pages(instance, validated_data.pop('pages', None))
#         # self.update_or_create_credits(instance, validated_data.pop('credits', None))

#         return super().update(instance, validated_data)

#     def update_or_create_attributes(self, instance, validated_data):
#         if validated_data is not None:
#             if instance.attributes.all().exists():
#                 current_attributes = instance.attributes.all()
#                 current_attributes_dict = {i.id: [i.attribute_type.short_name, i] for i in current_attributes}
#                 active_types = self.get_active_attributes(instance)
#                 new_attributes = []
#                 for _i, attribute in enumerate(validated_data):
#                     if current_attributes.filter(**attribute).count() == 1:
#                         current_attributes_dict.pop(current_attributes.get(**attribute).id)
#                     else:
#                         new_attributes.append(attribute)

#                 if len(current_attributes_dict) > 0:
#                     for _id, lst in current_attributes_dict.items():
#                         if lst[0] in active_types:
#                             lst[1].delete()
#             else:
#                 new_attributes = validated_data

#             if new_attributes:
#                 for attribute in new_attributes:
#                     instance.attributes.create(**attribute)

#     # def update_or_create_credits(self, instance, validated_data):
#     #     if validated_data is not None:
#     #         if instance.credits.all().exists():
#     #             current_credits = instance.credits.all()
#     #             current_credits_dict = {i.id: i for i in current_credits}
#     #             new_credits = []
#     #             for _i, credit in enumerate(validated_data):
#     #                 if current_credits.filter(source=instance.id, agent=credit['agent']['id']).exists():
#     #                     current_credits_dict.pop(
#     #                         current_credits.get(source=instance.id, agent=credit['agent']['id']).id
#     #                     )
#     #                 else:
#     #                     new_credits.append(credit)

#     #             if len(current_credits_dict) > 0:
#     #                 for credit in current_credits_dict.values():
#     #                     credit.delete()
#     #         else:
#     #             new_credits = validated_data

#     #         if new_credits:
#     #             for credit in new_credits:
#     #                 agent = Agent.objects.get(pk=credit['agent']['id'])
#     #                 Record_credit.objects.create(
#     #                     source=instance,
#     #                     agent=agent,
#     #                     note=credit.get('note'),
#     #                     type=credit.get('type'),
#     #                 )

#     def update_or_create_workflow(self, instance, validated_data):
#         if validated_data is not None:
#             try:
#                 workflow = instance.workflow
#             except Workflow.DoesNotExist:
#                 workflow = Workflow.objects.create(source=instance, last_modified=instance.modification_timestamp)
#                 WorkLog.objects.create(source=workflow, event='Record created', timestamp=workflow.last_modified)
#             for key, value in validated_data.items():
#                 setattr(workflow, key, value)
#             workflow.save()

#     def update_or_create_pages(self, instance, validated_data):
#         if validated_data is not None:
#             if instance.pages.all().exists():
#                 new_pages = []
#                 current_pages = {i.id: i for i in instance.pages.all()}
#                 for page in validated_data:
#                     if 'id' in page:
#                         current_page = current_pages.pop(UUID(page['id']))
#                         page.pop('id')
#                         page['dam_id'] = page.get('dam_id')
#                         for key, value in page.items():
#                             setattr(current_page, key, value)
#                         current_page.save()
#                     else:
#                         new_pages.append(page)
#                 if len(current_pages) > 0:
#                     for page in current_pages.values():
#                         page.delete()
#             else:
#                 new_pages = validated_data

#             if new_pages:
#                 for page in new_pages:
#                     instance.pages.create(**page)

#     def process_attributes(self, source_type, data):
#         multi_attributes = [
#             i.attribute_type.short_name
#             for i in ContentAttributeTypes.objects.filter(content_type=source_type)
#             if not i.unique
#         ]

#         if type(data) is dict:
#             attributes = []
#             for key, value in data.items():
#                 if key in multi_attributes and value == 0:
#                     continue
#                 value_list = value if key in multi_attributes else [value]
#                 for item in value_list:
#                     if item is not None:
#                         attributes.append({key: item})

#         else:
#             attributes = {}
#             for attribute in data:
#                 if attribute is not None:
#                     ((key, value),) = attribute.items()
#                     if key in multi_attributes:
#                         if attributes.get(key) is not None:
#                             attributes[key].append(value)
#                         else:
#                             attributes[key] = [value]
#                     else:
#                         attributes[key] = value

#         return attributes

#     def get_active_attributes(self, instance):
#         if instance.type.id == 13:
#             source_type = 'records'
#         elif instance.type.id == 19:
#             source_type = 'archives'
#         elif instance.type.id == 12:
#             source_type = 'archival-files'
#         else:
#             source_type = 'bibliography'

#         with open(os.path.join('dalme_app', 'config', 'datatables', f'_sources_{source_type}.json')) as fp:
#             config_file = json.load(fp)

#         return [k for k, v in config_file['config']['globals']['attribute_concordance'].items()]

#     @staticmethod
#     def get_folios(instance):
#         return [page.page_data for page in instance.folios.all()]
