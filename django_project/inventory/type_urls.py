"""
ItemType URLs; included by inventory_urls
"""

from django.conf.urls import url

from views import views_type as vt

app_name = 'type'
urlpatterns=[
	url(r'^$', vt.IndexView.as_view(), name='index'),
]
