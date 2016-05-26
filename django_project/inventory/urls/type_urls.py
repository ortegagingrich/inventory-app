"""
ItemType URLs; included by inventory_urls
"""

from django.conf.urls import url

from inventory.views import views_type as vt
from inventory.views import views_item as vi

app_name = 'type'
urlpatterns=[
	url(r'^$', vt.index_page, name='index'),
	#/inventory/type/upc/
	url(r'^upc/$', vt.upc_page, name='upc_page'),
	#/inventory/type/upc/001516153851/ TODO: switch to get methods w/ url
	url(r'^upc/lookup/$', vt.upc_lookup, name='upc_lookup'),
	#/inventory/type/search/
	url(r'^search/$', vt.search_page, name='search_page'),
	#/inventory/type/new/
	url(r'^new/$', vt.create_page, name='create_page'),
	#/inventory/type/new/submit/
	url(r'^new/submit/', vt.create_submit, name='create_submit'),
	#/inventory/type/1901/
	url(r'^(?P<type_key>[0-9]+)/$', vt.detail_page, name='detail'),
	#/inventory/type/1901/rename/
	url(r'^(?P<type_key>[0-9]+)/rename/$', vt.rename_submit, name='rename'),
	#/inventory/type/1901/modify/
	url(r'^(?P<type_key>[0-9]+)/modify/$', vt.modify_page, name='modify_page'),
	#/inventory/type/1901/modify/submit
	url(r'^(?P<type_key>[0-9]+)/modify/submit$', vt.modify_submit, name='modify_submit'),
	#/inventory/type/1901/delete/
	url(r'^(?P<type_key>[0-9]+)/delete/$', vt.delete_submit, name='delete'),
	#/inventory/type/1901/new/
	url(r'^(?P<type_key>[0-9]+)/new/$', vi.item_create_page, name='item_create_page'),
	#/inventory/type/1901/new/submit/
	url(r'^(?P<type_key>[0-9]+)/new/submit/$', vi.item_create_submit, 
	    name='item_create_submit'),
]
