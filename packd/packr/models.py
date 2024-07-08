from django.db import models
from django.contrib.auth.models import User

# TODOS: 
# on_delete functionality

# Create your models here.
class Trip(models.Model):

    trip_name = models.CharField(max_length=100)
    traveler = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.trip_name

class Bag(models.Model):

    bag_name = models.CharField(max_length=100)
    dimension_x = models.FloatField()
    dimension_y = models.FloatField()
    dimension_z = models.FloatField()

    traveler = models.ForeignKey(User, on_delete=models.CASCADE)
    trips = models.ManyToManyField(Trip)
    
    def __str__(self):
        return self.bag_name


class Compartment(models.Model):

    compartment_name = models.CharField(max_length=100)
    dimension_x = models.FloatField()
    dimension_y = models.FloatField()
    dimension_z = models.FloatField()

    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.bag.bag_name}: {self.compartment_name}"

class Item(models.Model):

    compartments = models.ManyToManyField(Compartment)
    item_name = models.CharField(max_length=100)
    weight = models.FloatField()
    dimension_x = models.FloatField()
    dimension_y = models.FloatField()
    dimension_z = models.FloatField()

    def __str__(self):
        return self.item_name

