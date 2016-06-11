"""
URLs related to the inventory system
"""

from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from inventory.views import actions_admin, views_user, views_item, views_misc, views_notification

app_name = 'inventory'
user_urlpatterns = [
	#/inventory/
	url(r'^$', views_misc.inventory_greeter, name='inventory_greeter'),
	#/inventory/location/*
	url(r'^location/', include('inventory.urls.location_urls'), name='location'),
	#/inventory/type/
	url(r'^type/', include('inventory.urls.type_urls'), name='type'),
	#/inventory/login/
	url(r'^login/$', views_user.login_submit, name='login'),
	#/inventory/logout/
	url(r'^logout/$', views_user.logout_submit, name='logout'),
	#/inventory/profile/
	url(r'^profile/$', views_user.profile_page, name='profile'),
	#/inventory/profile/modify/
	url(r'^profile/modify/$', views_user.profile_modify, name='profile_modify'),
	#/inventory/profile/modify/submit/
	url(r'^profile/modify/submit/$', views_user.profile_submit, name='profile_submit'),
	#/inventory/profile/password/
	url(r'^profile/password/$', views_user.password_modify, name='password_modify'),
	#/inventory/profile/password/submit/
	url(r'^profile/password/submit/$', views_user.password_submit, name='password_submit'),
	#/inventory/signup/
	url(r'^signup/$', views_user.signup_page, name='signup'),
	#/inventory/signup/submit/
	url(r'^signup/submit/$', views_user.signup_submit, name='signup_submit'),
	#/inventory/reset/
	url(r'^reset/$', views_user.password_reset, name='password_reset'),
	#/inventory/reset/submit/
	url(r'^reset/submit/', views_user.password_reset_submit, name='password_reset_submit'),
	#/inventory/notifications/
	url(r'^notifications/$', views_notification.notification_page, name='notification_page'),
	#/inventory/index/
	url(r'^index/$', views_item.IndexView.as_view(), name='inventory_index'),
	#/inventory/index/expired/
	url(r'^index/expired/$', views_item.item_index_expired, name='inventory_index_expired'),
	#/inventory/index/old/
	url(r'^index/old/', views_item.item_index_old, name='inventory_index_old'),
	#/inventory/5/
	#url(r'^(?P<item_id>[0-9]+)/$', views.item_detail, name='item_detail'),
	url(r'^(?P<pk>[0-9]+)/$', views_item.ItemDetailView.as_view(), name='item_detail'),
	#/inventory/5/open/
	url(r'^(?P<item_id>[0-9]+)/open/$', views_item.item_open_page, name='item_open_page'),
	#/inventory/5/open/submit/
	url(r'^(?P<item_id>[0-9]+)/open/submit/$', 
	    views_item.item_open_submit, name='item_open_submit'),
	#/inventory/5/move/
	url(r'^(?P<item_id>[0-9]+)/move/$', views_item.item_move_page, name='item_move_page'),
	#/inventory/5/move/submit/
	url(r'^(?P<item_id>[0-9]+)/move/submit/$', views_item.item_move_submit,
	    name='item_move_submit'),
	#/inventory/5/delete/
	url(r'^(?P<item_id>[0-9]+)/delete/$', views_item.item_delete_submit, name='item_delete_submit'),
]

admin_urlpatterns = [
	url(r'crash/$', actions_admin.crash, name='cause_server_error'),
	url(r'^purge/$', actions_admin.purge_database, name='purge_database'),
]

urlpatterns = user_urlpatterns + admin_urlpatterns

