"""Define URLs for dalme_api."""
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from ida import urls as ida_urls

from . import resources
from .csrf import csrf

router = routers.DefaultRouter()

router.register(r'agents', resources.Agents, basename='agents')
router.register(r'attachments', resources.Attachments, basename='attachments')
router.register(r'attribute_types', resources.AttributeTypes, basename='attribute_types')
router.register(r'attributes', resources.Attributes, basename='attributes')
router.register(r'collections', resources.Collections, basename='collections')
router.register(r'comments', resources.Comments, basename='comments')
router.register(r'content-types', resources.ContentTypes, basename='content_types')
router.register(r'countries', resources.Countries, basename='countries')
router.register(r'datasets', resources.Datasets, basename='datasets')
router.register(r'groups', resources.Groups, basename='groups')
router.register(r'images', resources.Images, basename='images')
router.register(r'languages', resources.Languages, basename='languages')
router.register(r'library', resources.Library, basename='library')
router.register(r'locales', resources.Locales, basename='locales')
router.register(r'locations', resources.Locations, basename='locations')
router.register(r'pages', resources.Pages, basename='pages')
router.register(r'ping', resources.Ping, basename='ping')
router.register(r'places', resources.Places, basename='places')
router.register(r'records', resources.Records, basename='records')
router.register(r'rights', resources.Rights, basename='rights')
router.register(r'session', resources.Session, basename='session')
router.register(r'tasklists', resources.TaskLists, basename='tasklists')
router.register(r'tasks', resources.Tasks, basename='tasks')
router.register(r'tickets', resources.Tickets, basename='tickets')
router.register(r'transcriptions', resources.Transcriptions, basename='transcriptions')
router.register(r'users', resources.Users, basename='users')
router.register(r'workflow', resources.Workflows, basename='workflow')

urlpatterns = [
    path('', include(ida_urls)),
    path('', include((router.urls, 'dalme_api'), namespace='api_endpoint')),
    path('csrf/', csrf),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
