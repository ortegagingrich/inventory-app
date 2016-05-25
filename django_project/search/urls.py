"""
URLs directly related to the search app
"""
from django.conf.urls import url

from django_project.settings import DEBUG
from search import views


app_name = 'search'
urlpatterns = []

debug_urlpatterns = [
	url('^test/$', views.test_view, name='test_view'),
]

if DEBUG:
	urlpatterns += debug_urlpatterns


