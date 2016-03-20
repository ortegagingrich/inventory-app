"""
URLs related to the inventory system
"""

from django.conf.urls import url

from views import views

urlpatterns = [
	url(r'^$', views.index, name = 'inventory_index'),
]


def __test__():
	print "test"
	views.__test__()

if __name__ == '__main__':
	__test__()
