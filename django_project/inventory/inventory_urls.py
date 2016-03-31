"""
URLs related to the inventory system
"""

from django.conf.urls import url
from django.views.generic.base import RedirectView

from views import actions, views

app_name = 'inventory'
urlpatterns = [
	#/inventory/
	url(r'^$', views.inventory_greeter, name='inventory_greeter'),
	#/inventory/login/
	url(r'^login/$', actions.login_action, name='login'),
	#/inventory/logout/
	url(r'^logout/$', actions.logout_action, name='logout'),
	#/inventory/signup/
	url(r'^signup/$', views.signup, name='signup'),
	#/inventory/signup/submit/
	url(r'^signup/$', actions.signup_submit, name='signup_submit'),
	#/inventory/index/
	url(r'^index/$', views.IndexView.as_view(), name='inventory_index'),
	#/inventory/5/
	#url(r'^(?P<item_id>[0-9]+)/$', views.item_detail, name='item_detail'),
	url(r'^(?P<pk>[0-9]+)/$', views.ItemDetailView.as_view(), name='item_detail'),
	#/inventory/5/open/
	#url(r'^(?P<item_id>[0-9]+)/open/$', views.item_open, name='item_open'),
	url(r'^(?P<pk>[0-9]+)/open/$', views.ItemOpenView.as_view(), name='item_open'),
	#/inventory/5/open/2016-08-23
	url(r'^(?P<item_id>[0-9]+)/open/submit/$', 
	    actions.item_open, name='item_open_submit'),
]


def __test__():
	print "test"
	views.__test__()

if __name__ == '__main__':
	__test__()
