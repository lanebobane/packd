from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):

    name = models.CharField(max_length=100)
    weight = models.FloatField()
    dimension_x = models.FloatField()
    dimension_y = models.FloatField()
    dimension_z = models.FloatField()
    is_bag = models.BooleanField(default=False)

    traveler = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

class Pack(models.Model):
    name = models.CharField(max_length=100, default=None)
    bag = models.ForeignKey(Item, related_name="bag", on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name="items")

    traveler = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.name