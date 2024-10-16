"""Interface for the api.resources module."""

from .agents import Agents, AgentSerializer
from .attachments import Attachments, AttachmentSerializer
from .attributes import (
    Attributes,
    AttributeSerializer,
    AttributeTypes,
    AttributeTypeSerializer,
    ContentTypes,
    PublicAttributes,
    PublicAttributeTypes,
)
from .collections import Collections, CollectionSerializer
from .comments import Comments, CommentSerializer
from .countries import Countries, CountryReferenceSerializer
from .datasets import Datasets
from .groups import Groups, GroupSerializer
from .images import ImageOptionsSerializer, Images, ImageUrlSerializer, RSCollectionsSerializer, RSImageSerializer
from .languages import LanguageReferenceSerializer, Languages
from .library import Library
from .locales import LocaleReferenceSerializer, Locales
from .locations import Locations, LocationSerializer
from .pages import Pages, PageSerializer
from .ping import Ping
from .places import Places, PlaceSerializer
from .records import PublicRecords, Records, RecordSerializer, RecordTypeSerializer
from .rights import Rights, RightsPolicySerializer
from .session import Session
from .tasks import TaskLists, TaskListSerializer, Tasks, TaskSerializer
from .tenants import TenantSerializer
from .tickets import TicketDetailSerializer, Tickets, TicketSerializer
from .transcriptions import Transcriptions, TranscriptionSerializer
from .users import Users, UserSerializer
from .workflows import Workflows, WorkflowSerializer, WorklogSerializer

__all__ = [
    'AgentSerializer',
    'Agents',
    'AttachmentSerializer',
    'Attachments',
    'AttributeSerializer',
    'AttributeTypeSerializer',
    'AttributeTypes',
    'Attributes',
    'CollectionSerializer',
    'Collections',
    'CommentSerializer',
    'Comments',
    'ContentTypes',
    'Countries',
    'CountryReferenceSerializer',
    'Datasets',
    'GroupSerializer',
    'Groups',
    'ImageOptionsSerializer',
    'ImageUrlSerializer',
    'Images',
    'LanguageReferenceSerializer',
    'Languages',
    'Library',
    'LocaleReferenceSerializer',
    'Locales',
    'LocationSerializer',
    'Locations',
    'PageSerializer',
    'Pages',
    'Ping',
    'PlaceSerializer',
    'Places',
    'PublicRecords',
    'PublicAttributeTypes',
    'PublicAttributes',
    'RSCollectionsSerializer',
    'RSImageSerializer',
    'RecordSerializer',
    'RecordTypeSerializer',
    'Records',
    'Rights',
    'RightsPolicySerializer',
    'Session',
    'TaskListSerializer',
    'TaskLists',
    'TaskSerializer',
    'Tasks',
    'TenantSerializer',
    'TicketDetailSerializer',
    'TicketSerializer',
    'Tickets',
    'TranscriptionSerializer',
    'Transcriptions',
    'UserSerializer',
    'Users',
    'WorkflowSerializer',
    'Workflows',
    'WorklogSerializer',
]
