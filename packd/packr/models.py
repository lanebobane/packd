from django.db import models

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
    dimension_x = models.DecimalField(max_digits=2)
    dimension_y = models.DecimalField(max_digits=2)
    dimension_z = models.DecimalField(max_digits=2)

    traveler = models.ForeignKey(User)
    trips = models.ManyToManyField(Trip)
    
    def __str__(self):
        return self.bag_name


class Compartment(models.Model):

    compartment_name = models.CharField(max_length=100)
    dimension_x = models.DecimalField(max_digits=2)
    dimension_y = models.DecimalField(max_digits=2)
    dimension_z = models.DecimalField(max_digits=2)

    bag = models.ForeignKey(Bag)
    
    def __str__(self):
        return self.bag_name

class Item(models.Model):

    item_name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=2)
    dimension_x = models.DecimalField(max_digits=2)
    dimension_y = models.DecimalField(max_digits=2)
    dimension_z = models.DecimalField(max_digits=2)

class Activity(models.Model):
    SKIING = 'skiing'
    MTB = 'mountain_biking'
    GOLF = 'golf'
    FISHING = 'fishing'
    ACTIVITIES = [SKIING,MTB,GOLF,FISHING]
    activity_name = models.CharField(choices=ACTIVITIES)

