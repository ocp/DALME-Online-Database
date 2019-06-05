from django.urls import path, re_path
from . import views

urlpatterns = [
    path('search/', views.DefaultSearch.as_view(), name='search'),
    path('su/', views.SessionUpdate, name='session_update'),
    path('uiref/', views.UIRefMain.as_view(), name='uiref'),
    path('scripts/', views.Scripts.as_view(), name='scripts'),
    path('worksets/<slug:pk>/', views.WorksetsRedirect.as_view(), name='worksets_redirect'),
    path('models/<model>/', views.ModelLists.as_view(), name='model_lists'),
    path('languages/', views.LanguageList.as_view(), name='language_list'),
    path('async_tasks/', views.AsyncTaskList.as_view(), name='async_task_list'),
    path('countries/', views.CountryList.as_view(), name='country_list'),
    path('cities/', views.CityList.as_view(), name='city_list'),
    path('download/<path:path>/', views.DownloadAttachment, name='download_attachment'),
    re_path(r'^sources/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.SourceManifest, name='source_manifest'),
    re_path(r'^pages/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.PageManifest, name='page_manifest'),
    path('sources/', views.SourceList.as_view(), name='source_list'),
    path('sources/<slug:pk>/', views.SourceDetail.as_view(), name='source_detail'),
    path('images/', views.ImageList.as_view(), name='image_list'),
    path('images/<slug:pk>/', views.ImageDetail.as_view(), name='image_detail'),
    path('pages/', views.PageList.as_view(), name='page_list'),
    path('pages/<slug:pk>/', views.PageDetail.as_view(), name='page_detail'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<username>/', views.UserDetail.as_view(), name='user_detail'),
    path('tasks/', views.TasksList.as_view(), name='tasks_list'),
    path('tasks/<slug:pk>/', views.TasksDetail.as_view(), name='tasks_detail'),
    path('', views.Index.as_view(), name='dashboard'),
]
