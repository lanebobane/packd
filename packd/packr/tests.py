from django.test import TestCase
from .models import Trip, Bag, Compartment, Item
from django.contrib.auth.models import User

# Create your tests here.

class TripModelTests(TestCase):

	def test_valid_trip(self):
		# TODO: how can I do this better? A mock perhaps? 
		user = User()
		name = 'Test Trip'
		trip = Trip(traveler=user, trip_name=name)

		assert trip.trip_name == name
		assert trip.traveler.id == user.id



# Test Ideas
# 1. validate that a bag's compartments do not exceed its own size
# 2. A compartment can only belong to one bag.
# 3. 