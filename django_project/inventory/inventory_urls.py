"""
URLs related to the inventory system
"""

from django.conf.urls import url
from django.views.generic.base import RedirectView

from views import views

app_name = 'inventory'
urlpatterns = [
	#/inventory/
	url(r'^$', views.inventory_greeter, name='inventory_greeter'),
	#/inventory/index/
	url(r'^index/$', views.inventory_index, name='inventory_index'),
	#/inventory/5/
	url(r'^(?P<item_id>[0-9]+)/$', views.item_detail, name='item_detail'),
	#/inventory/5/open/
	url(r'^(?P<item_id>[0-9]+)/open/$', views.item_open, name='item_open'),
]


def __test__():
	print "test"
	views.__test__()

if __name__ == '__main__':
	__test__()
