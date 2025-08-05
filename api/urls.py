from django.urls import path
from . import views

urlpatterns = [
    path('config/', views.APIConfigurationView.as_view(), name='api-config'),
    path('tokens/', views.APIAccessTokenListCreateView.as_view(), name='api-tokens'),
    path('logs/', views.APIRequestLogListView.as_view(), name='api-logs'),
    path('versions/', views.APIVersionListView.as_view(), name='api-versions'),
]