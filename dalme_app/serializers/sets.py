from django.contrib.auth.models import Group
from dalme_app.models import Set
from rest_framework import serializers
from ._common import DynamicSerializer
import dalme_app.serializers.users as _users
import dalme_app.serializers.others as _others
from dalme_app.models._templates import get_current_user


class SetSerializer(DynamicSerializer):
    owner = _users.UserSerializer(fields=['id', 'full_name', 'username'], required=False, read_only=True)
    set_type_name = serializers.CharField(source='get_set_type_display', required=False)
    permissions_name = serializers.CharField(source='get_permissions_display', required=False)
    dataset_usergroup = _others.GroupSerializer(required=False, read_only=True)

    class Meta:
        model = Set
        fields = ('id', 'name', 'set_type', 'set_type_name', 'description', 'owner', 'permissions', 'permissions_name', 'workset_progress', 'member_count',
                  'endpoint', 'creation_timestamp', 'is_public', 'has_landing', 'stat_title', 'stat_text', 'dataset_usergroup', 'detail_string')
        extra_kwargs = {
                        'endpoint': {'required': False},
                        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('workset_progress') is not None and ret.get('set_type') is not None and ret['set_type'] == 4:
            ret['workset'] = '<a class="workset-title" href="/sets/go/{}">{}</a><div class="workset-description">{}</div><div class="workset-endpoint">Endpoint: {}</div>'.format(ret['id'], ret['name'], ret['description'], ret['endpoint'])
            progress = ret['workset_progress']
            angle = round((progress * 360 / 100))
            if angle <= 180:
                right_style = 'style="display:none;"'
                pie_style = ''
            else:
                right_style = 'style="transform:rotate(180deg);"'
                pie_style = 'style="clip:rect(auto, auto, auto, auto);"'
            left_style = 'style="transform:rotate(' + str(angle) + 'deg);"'
            progress_circle = '<div class="pie-wrapper"><span class="label">{}<span class="smaller">%</span></span><div class="pie" {}>'.format(round(progress), pie_style)
            progress_circle += '<div class="left-side half-circle" {}></div><div class="right-side half-circle" {}></div></div></div>'.format(left_style, right_style)
            ret['progress_circle'] = progress_circle
        if ret.get('set_type') is not None:
            ret['set_type'] = {
                'name': ret.pop('set_type_name'),
                'id': ret.pop('set_type')
            }
        if ret.get('permissions') is not None:
            ret['permissions'] = {
                'name': ret.pop('permissions_name'),
                'id': ret.pop('permissions')
            }
        return ret

    def to_internal_value(self, data):
        if data.get('owner') is None:
            data['owner'] = get_current_user().id
        if data.get('endpoint') is None:
            data['endpoint'] = 'sources'
        return super().to_internal_value(data)

    def run_validation(self, data):
        if type(data) is dict:
            if data.get('set_type') is not None:
                required = {
                    1: ['name', 'set_type', 'permissions', 'description'],
                    2: ['name', 'set_type', 'permissions', 'description'],
                    3: ['name', 'set_type', 'dataset_usergroup', 'description'],
                    4: ['name', 'set_type', 'endpoint', 'permissions']
                }
                missing = {}
                for field in required[data['set_type']]:
                    if data.get(field) in [None, '', 0]:
                        missing[field] = ['This field is required.']
                if len(missing):
                    raise serializers.ValidationError(missing)
            _id = data['id'] if data.get('id') is not None else False
            _ds_usergroup = data.pop('dataset_usergroup') if data.get('dataset_usergroup') is not None else False
            data = {k: v for k, v in data.items() if v is not None}
            validated_data = super().run_validation(data)
            if _id:
                validated_data['id'] = _id
            if _ds_usergroup:
                validated_data['dataset_usergroup'] = Group.objects.get(pk=_ds_usergroup)
            return validated_data
        elif type(data) is str and data != '':
            return Set.objects.get(pk=data)
        else:
            return super().run_validation(data)

    # def create(self, validated_data):
    #     bob=uncle
    #     return 's'
