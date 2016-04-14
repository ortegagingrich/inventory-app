"""
Location URLs; included by inventory_urls
"""

from django.conf.urls import url

from views import views_location as vl

app_name = 'location'
urlpatterns = [
	#/inventory/location/
	url(r'^$', vl.IndexView.as_view(), name='index'),
	#/inventory/location/new/
	url(r'^new/$', vl.create_page, name='create_page'),
	#/inventory/location/new/submit/
	url(r'^new/submit/', vl.create_submit, name='create_submit'),
	#/inventory/location/1901/
	url(r'^(?P<location_key>[0-9]+)/$', vl.detail_page, name='detail'),
	#/inventory/location/1901/rename/
	url(r'^(?P<location_key>[0-9]+)/rename/$', vl.rename_submit, name='rename'),
]
