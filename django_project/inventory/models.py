from __future__ import unicode_literals

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from notifications.models import add_notification_link, NotificationModel

import inventory.exceptions

"""
Important note about the behavior of defaults.

For Locations, it is expected that users will not very much appreciate having
locations changed on the fly.  It is also expected that if a user modifies a
default location, they will want it to remain as it is, ignoring updates.  As
such, Location Defaults are turned into user-specific Locations upon the creation
of accounts.  These locations are not to be modified afterwards and do not even
keep reference to their corresponding defaults.  Really defaults are just
templates that are used to make individual locations for each user.

ItemTypes, on the other hand, are handled very differently.  Each 'Default' item
type is just a single item type without an associated user (i.e. null).  This
type is not modifiable by any user, though any user may add an item of this type
to the database.  These types are subject to change, but will not be deleted.
"""


""" Locations """

class LocationDefault(models.Model):
	"""
	Class of default locations which serve as 'blueprints' for user-specific
	locations.
	"""
	
	name = models.CharField(max_length=100)
	refrigerated = models.BooleanField(default=False)
	frozen = models.BooleanField(default=False)
	
	def __str__(self):
		return self.name


class Location(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	
	name = models.CharField(max_length=100)
	refrigerated = models.BooleanField(default=False)
	frozen = models.BooleanField(default=False)
	
	@staticmethod
	def retrieve_with_write_permision(user, location_id):
		"""
		Attempts to retrieve an item with the given id belonging to the given user.
		If no such item exists, the appropriate error is raised
		"""
		try:
			item = Item.objects.get(pk=item_id)
			if item.user != user:
				raise Exception
		except:
			raise inventory.exceptions.InvalidItemError(item_id)
		return item
	
	
	@property
	def temperature(self):
		if self.frozen:
			return "Frozen"
		elif self.refrigerated:
			return "Refrigerated"
		else:
			return "Room Temperature"
	
	@property
	def item_count(self):
		return len(Item.objects.filter(location=self))
	
	def __str__(self):
		return self.name


""" Item Types """

class OpenGroceryDatabaseEntry(models.Model):
	grp_id = models.IntegerField()
	product_brand = models.CharField(max_length = 50)
	product_name = models.CharField(max_length = 100)
	product_upc = models.BigIntegerField()


class ItemType(models.Model):
	open_grocery_entry = models.ForeignKey(OpenGroceryDatabaseEntry, default=None,
	                           on_delete=models.CASCADE, null=True, blank=True)
	#user is null for default items
	user = models.ForeignKey(User, on_delete = models.CASCADE, null=True,
	                         blank=True)
	
	name = models.CharField(max_length = 150)
	
	"""
	needed_temperature values:
		0: Does not need to be refrigerated
		1: Only needs refrigeration when opened
		2: Always needs refrigeration
		3: Always needs to be frozen
	"""
	needed_temperature = models.SmallIntegerField(default=2)
	
	openable = models.BooleanField(default=False)
	open_expiration_term = models.DurationField(null=True, blank=True)
	freezer_expiration_term = models.DurationField(null=True, blank=True)
	
	initialized = models.BooleanField(default=True)
	
	@staticmethod
	def retrieve_with_write_permission(user, type_id):
		"""
		Attempts to retrieve an ItemType with the given id belonging to the given user.
		If no such type exists, the appropriate error is raised
		"""
		try:
			item_type = ItemType.objects.get(pk=type_id)
			if not item_type.user in [user, None]:
				raise Exception
		except:
			raise inventory.exceptions.InvalidItemTypeError(type_id)
		return item_type
	
	
	@property
	def is_generic(self):
		return self.open_grocery_entry == None
	
	@property
	def is_custom(self):
		return self.user != None and self.is_generic
	
	@property
	def item_count(self):
		if self.user == None:
			return None
		else:
			return len(Item.objects.filter(item_type=self))
	
	def item_count_generic(self, user):
		return len(Item.objects.filter(item_type=self, user=user))
	
	def __str__(self):
		return self.name


""" Items """

class Item(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	
	location = models.ForeignKey(Location, on_delete = models.CASCADE)
	item_type = models.ForeignKey(ItemType, on_delete = models.CASCADE)
	
	
	printed_expiration_date = models.DateField(blank=True, null=True)
	opened_date = models.DateField(null=True, blank=True)
	
	#Do not change these; they are handled automatically:
	#indicates that at some point, the item was improperly stored.
	_improperly_stored = models.BooleanField(default=False)
	#the date when the item was placed in its last location; if null
	_location_date = models.DateField(null=True)
	
	#indicates whether or not an expiration notification has been issued
	#This is to prevent double-reporting of expiration.
	_expiration_notified = models.BooleanField(default=False)
	
	
	@staticmethod
	def retrieve_with_write_permission(user, item_id):
		"""
		Attempts to retrieve an item with the given id belonging to the given user.
		If no such item exists, the appropriate error is raised
		"""
		try:
			item = Item.objects.get(pk=item_id)
			if item.user != user:
				raise Exception
		except:
			raise inventory.exceptions.InvalidItemError(item_id)
		return item
	
	
	@staticmethod
	def get_expired_items(user):
		"""
		Returns a (possibly empty) list of expired items owned by the
		provided user
		"""
		all_items = Item.objects.filter(user=user)
		expired_items = []
		for item in all_items:
			if item.expired:
				expired_items.append(item)
		return expired_items
	
	
	#TODO: figure out when the appropriate time is to call this
	# Called in the following circumstances:
	#    1) when the user logs in
	#    2) TODO: setup celery task to check this at regular intervals
	@staticmethod
	def update_notifications(user):
		"""
		Updates the notifications related to inventory items for the provided
		user.  For example, it creates notifications for all expired items
		"""
		items = Item.get_expired_items(user)
		for item in items:
			if not item._expiration_notified:
				message = 'An item "{}" is expired.  Click here to go to its page.'
				
				add_notification_link(
					user=user,
					name='Expired Item: {}'.format(item.item_type.name),
					message=message.format(item.item_type.name),
					url=item.url,
					id_string='item_{}'.format(item.id)
				)
				
				item._expiration_notified = True
				item.save()
	
		
	
	
	def __setattr__(self, k, v):
		super(Item, self).__setattr__(k, v)
		if k in ['location_id', 'opened_date']:
			self.on_state_change()
	
	@property
	def properly_stored(self):
		return not self._improperly_stored
	
	@property
	def improperly_stored(self):
		return self._improperly_stored
	
	@property
	def expired(self):
		if self.expiration_date != None:
			return date.today() > self.expiration_date
		else:
			return self._improperly_stored
	
	@property
	def opened(self):
		return self.opened_date != None
	
	@property
	def expiration_date(self):
		"""
		Computes the actual expiration date, assuming the item is stored in its
		current conditions indefinitely.
		"""
		if self.printed_expiration_date == None:
			return None
		
		#first, check for immediate disqualifications (improper storage)
		if self._improperly_stored:
			return min(self._location_date, date.today()) - timedelta(days=1)
		
		
		modified_date = self.printed_expiration_date
		
		if self.item_type.openable and self.opened:
			base_date = self.opened_date
			term = self.item_type.open_expiration_term
			if term != None:
				modified_date = min(base_date + term, modified_date)
		
		exp_date = min(self.printed_expiration_date, modified_date)
		
		#alternate criterion for items frozen before they went bad.
		if self.location.frozen and self._location_date < exp_date:
			exp_term = self.item_type.freezer_expiration_term
			if exp_term != None:
				exp_date = self._location_date + self.item_type.freezer_expiration_term
		
		return exp_date
	
	@property
	def url(self):
		"""
		Returns the url of this item's detail page
		"""
		return reverse('inventory:item_detail', args=(self.id,))
	
	
	def on_state_change(self):
		"""
		Executed whenever an item is opened or moved to a new location.
		"""
		#Note: the part below might fail for new objects just being created.
		try:
			self._location_date = date.today()
			self.check_improper_storage()
		except:
			pass
	
	
	def check_improper_storage(self):
		"""
		Checks to see if the item is currently improperly stored.  This should
		be called whenever the item's location is changed.
		"""
		if self._location_date == None:
			self._location_date = date.today()
		
		if not self._improperly_stored:
			if self.item_type.needed_temperature in [1, 2]: #needs refrigeration
				if not (self.location.refrigerated or self.location.frozen):
					if self.item_type.needed_temperature == 2:
						self._improperly_stored = True
					elif self.opened:
						self._improperly_stored = True
			elif self.item_type.needed_temperature == 3: #needs freezer
				if not self.location.frozen:
					self._improperly_stored = True
		
		self.save()
	
	def __str__(self):
		return self.item_type.name


"""Administrative Models"""

class UserProfile(models.Model):
	
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	_needs_password_reset = models.BooleanField(default=True)
	
	
	@staticmethod
	def needs_reset(user):
		"""Checks to see if the provided user needs a password reset"""
		try:
			profile = UserProfile.objects.get(user=user)
			return profile._needs_password_reset
		except ObjectDoesNotExist:
			return False
	
	@staticmethod
	def on_reset(user):
		"""
		User no longer needs to reset password
		"""
		try:
			profile = UserProfile.objects.get(user=user)
			profile._needs_password_reset = False
			profile.save()
			
			#get rid of any unread password reset notifications
			notifications = NotificationModel.objects.filter(
				user=user,
				id_string=reset_password
			)
			for notification in notifications:
				if notification.unread:
					notification.delete()
			
		except ObjectDoesNotExist:
			pass
	
	@staticmethod
	def on_require_reset(user):
		"""
		User does something that requires a password reset (e.g. new account)
		"""
		profile, new = UserProfile.objects.get_or_create(user=user)
		
		if not profile._needs_password_reset:
			profile._needs_password_reset = True
			profile.save()
			
			#create a notification for the reset
			add_notification_link(
				user=user,
				name='Reset Password',
				message='Please reset your password as soon as possible.',
				id_string='reset_password'
			)
	
	
#hack to make sure signals are properly initiated
from inventory import user, item

