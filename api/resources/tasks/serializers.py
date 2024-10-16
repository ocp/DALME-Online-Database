"""Serializers for task data."""

from rest_framework import serializers

from api.resources.attachments import AttachmentSerializer
from api.resources.collections import CollectionSerializer
from api.resources.groups import GroupSerializer
from api.resources.tenants import TenantSerializer
from api.resources.users import UserSerializer
from ida.models import Task, TaskList


class TaskListSerializer(serializers.ModelSerializer):
    """Serializer for task lists."""

    creation_user = UserSerializer(field_set='attribute', required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)
    owner = UserSerializer(field_set='attribute')
    team_link = GroupSerializer(field_set='attribute', required=False)
    tenant = TenantSerializer(required=True)

    class Meta:
        model = TaskList
        fields = [
            'id',
            'tenant',
            'name',
            'description',
            'slug',
            'team_link',
            'owner',
            'task_count',
            'creation_user',
            'creation_timestamp',
            'modification_user',
            'modification_timestamp',
        ]


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""

    task_list = TaskListSerializer(required=True)
    completed_by = UserSerializer(field_set='attribute', required=False)
    files = AttachmentSerializer(many=True, required=False)
    assignees = UserSerializer(many=True, field_set='attribute', required=False)
    resources = CollectionSerializer(many=True, field_set='attribute', required=False)
    creation_user = UserSerializer(field_set='attribute', required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)
    tenant = TenantSerializer(required=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'tenant',
            'title',
            'task_list',
            'description',
            'due_date',
            'completed',
            'completed_date',
            'completed_by',
            'overdue',
            'files',
            'resources',
            'assignees',
            'url',
            'comment_count',
            'creation_timestamp',
            'creation_user',
            'modification_user',
            'modification_timestamp',
        ]
        extra_kwargs = {
            'overdue': {
                'required': False,
            },
            'comment_count': {
                'required': False,
            },
        }
