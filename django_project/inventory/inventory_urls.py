"""
URLs related to the inventory system
"""

from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from views import actions_admin, actions_user, actions_item, views, views_notification

app_name = 'inventory'
user_urlpatterns = [
	#/inventory/
	url(r'^$', views.inventory_greeter, name='inventory_greeter'),
	#/inventory/location/*
	url(r'^location/', include('inventory.location_urls'), name='location'),
	#/inventory/type/
	url(r'^type/', include('inventory.type_urls'), name='type'),
	#/inventory/login/
	url(r'^login/$', actions_user.login_action, name='login'),
	#/inventory/logout/
	url(r'^logout/$', actions_user.logout_action, name='logout'),
	#/inventory/profile/
	url(r'^profile/$', views.profile_page, name='profile'),
	#/inventory/profile/modify/
	url(r'^profile/modify/$', views.profile_modify, name='profile_modify'),
	#/inventory/profile/modify/submit/
	url(r'^profile/modify/submit/$', actions_user.profile_submit, name='profile_submit'),
	#/inventory/profile/password/
	url(r'^profile/password/$', views.password_modify, name='password_modify'),
	#/inventory/profile/password/submit/
	url(r'^profile/password/submit/$', actions_user.password_change, name='password_submit'),
	#/inventory/signup/
	url(r'^signup/$', views.signup_page, name='signup'),
	#/inventory/signup/submit/
	url(r'^signup/submit/$', actions_user.signup_submit, name='signup_submit'),
	#/inventory/notifications/
	url(r'^notifications/$', views_notification.notification_page, name='notification_page'),
	#/inventory/index/
	url(r'^index/$', views.IndexView.as_view(), name='inventory_index'),
	#/inventory/5/
	#url(r'^(?P<item_id>[0-9]+)/$', views.item_detail, name='item_detail'),
	url(r'^(?P<pk>[0-9]+)/$', views.ItemDetailView.as_view(), name='item_detail'),
	#/inventory/5/open/
	#url(r'^(?P<item_id>[0-9]+)/open/$', views.item_open, name='item_open'),
	url(r'^(?P<item_id>[0-9]+)/open/$', views.item_open_page, name='item_open'),
	#/inventory/5/open/submit/
	url(r'^(?P<item_id>[0-9]+)/open/submit/$', 
	    actions_item.item_open, name='item_open_submit'),
	#/inventory/5/move/
	url(r'^(?P<item_id>[0-9]+)/move/$', actions_item.item_move_page, name='item_move_page'),
	#/inventory/5/move/submit/
	url(r'^(?P<item_id>[0-9]+)/move/submit/$', actions_item.item_move_submit,
	    name='item_move_submit'),
	#/inventory/5/delete/
	url(r'^(?P<item_id>[0-9]+)/delete/$', actions_item.item_delete, name='item_delete'),
]

admin_urlpatterns = [
	url(r'^purge/$', actions_admin.purge_database, name='purge_database'),
]

urlpatterns = user_urlpatterns + admin_urlpatterns

def __test__():
	print "test"
	views.__test__()

if __name__ == '__main__':
	__test__()
