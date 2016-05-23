"""
URLS directly related to the notification system
"""
from django.conf.urls import include, url

from notifications import views


app_name = 'notifications'
urlpatterns = [
	url(r'^(?P<key>[0-9]+)/delete/$', 
	    views.delete_notification, name='delete'),
]

