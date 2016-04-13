"""
Location URLs; included by inventory_urls
"""

from django.conf.urls import url

from views import views_location as vl

app_name = 'location'
urlpatterns = [
	#/inventory/location/
	url(r'^$', vl.IndexView.as_view(), name='index'),
]
