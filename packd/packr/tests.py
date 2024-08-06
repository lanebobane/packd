from django.test import TestCase
from .models import Item, Pack
from django.contrib.auth.models import User

# Create your tests here.

# Test Ideas
# 1. validate that a user shouldn't see another users items (on their dashboard or when creating a Pack).


class BagTest(TestCase):

	def create_bag(
		self, 
		name="Default Test Bag Name", 
		weight=10, 
		dimension_x=1, 
		dimension_y=2, 
		dimension_z=3, 
		is_bag=True
	):
		return Item.objects.create(
			name=name,
			weight=weight,
			dimension_x=dimension_x,
			dimension_y=dimension_y,
			dimension_z=dimension_z,
			is_bag=is_bag
		)

	def test_bag_creation(self):
		bag = self.create_bag()
		self.assertTrue(isinstance(bag, Item))
		self.assertEqual(bag.__str__(), bag.name)

	def test_bag_volume(self):
		bag = self.create_bag()
		self.assertTrue(bag.volume() == 6)

class ItemTest(TestCase):

	def create_item(
		self, 
		name="Default Test Item Name", 
		weight=10, 
		dimension_x=4, 
		dimension_y=5, 
		dimension_z=6, 
		is_bag=False
	):
		return Item.objects.create(
			name=name,
			weight=weight,
			dimension_x=dimension_x,
			dimension_y=dimension_y,
			dimension_z=dimension_z,
			is_bag=is_bag
		)

	def test_item_creation(self):
		item = self.create_item()
		self.assertTrue(isinstance(item, Item))
		self.assertEqual(item.__str__(), item.name)

	def test_item_volume(self):
		item = self.create_item()
		self.assertTrue(item.volume() == 120)
