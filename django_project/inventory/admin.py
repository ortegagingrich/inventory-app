from django.contrib import admin

from.models import *


class ItemAdmin(admin.ModelAdmin):
	list_display = (
		'__str__', 'location', 'printed_expiration_date', 'opened_date',
		'expiration_date',
	)
	
	"""fieldsets = [
		(None, {'fields': ['item_type', 'location',]}),
		('Date Information', {'fields': ['printed_expiration_date', 'opened_date',]}),
	]
	"""

admin.site.register(Location)
admin.site.register(LocationDefault)

admin.site.register(ItemType)
admin.site.register(Item, ItemAdmin)
