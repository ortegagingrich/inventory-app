"""
ItemType URLs; included by inventory_urls
"""

from django.conf.urls import url

from views import views_type as vt

app_name = 'type'
urlpatterns=[
	url(r'^$', vt.index_page, name='index'),
	#/inventory/type/new/
	#url(r'^new/$', vt.create_page, name='create_page'),
	#/inventory/type/new/submit/
	#url(r'^new/submit/', vt.create_submit, name='create_submit'),
	#/inventory/type/1901/
	url(r'^(?P<type_key>[0-9]+)/$', vt.detail_page, name='detail'),
	#/inventory/type/1901/rename/
	url(r'^(?P<type_key>[0-9]+)/rename/$', vt.rename_submit, name='rename'),
	#/inventory/type/1901/delete/
	url(r'^(?P<type_key>[0-9]+)/delete/$', vt.delete_submit, name='delete'),
]
