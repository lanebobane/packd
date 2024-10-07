from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):

    name = models.CharField(max_length=100)
    weight = models.FloatField()
    dimension_x = models.FloatField()
    dimension_y = models.FloatField()
    dimension_z = models.FloatField()
    is_bag = models.BooleanField(default=False)
    reference_pk = models.PositiveIntegerField(default=None, null=True, blank=True)

    traveler = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def volume(self):
        return self.dimension_x * self.dimension_y * self.dimension_z


class Pack(models.Model):
    name = models.CharField(max_length=100, default=None)
    bag = models.ForeignKey(
        Item, related_name="bag", null=True, on_delete=models.CASCADE
    )
    items = models.ManyToManyField(Item, related_name="items")

    traveler = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def volume_remaining(self):
        vol_remaining = self.bag.volume() if self.bag else 0
        for i in self.items.all():
            if self.bag is not None and self.bag.id == i.id:
                continue
            vol_remaining -= i.volume()
        return vol_remaining

    def pack_weight(self):
        return sum([item.weight for item in self.items.all()], self.bag.weight if self.bag else 0)

    def share_pack(self):
        copied_items = []

        for item in self.items.all():
            temp_item_data = {
                    'name': item.name,
                    'dimension_x': item.dimension_x,
                    'dimension_y': item.dimension_y,
                    'dimension_z': item.dimension_z,
                    'weight': item.weight,
                    'is_bag': item.is_bag,
                    'reference_pk': item.pk
                }
            new_item = Item.objects.create(**temp_item_data)
            copied_items.append(new_item)

        pack = Pack.objects.create(name=self.name)
        pack.items.set(copied_items)
        return pack

    def adopt_pack(self, traveler_id):
        user_items = Item.objects.filter(traveler_id=traveler_id)
        user_items_dict = {}

        for item in user_items:
            user_items_dict[item.reference_pk] = item
        
        copied_items = []
        
        for item in self.items.all():
            if item.reference_pk in user_items_dict:
                copied_items.append(user_items_dict[item.reference_pk])
            else:
                temp_item_data = {
                    'name': item.name,
                    'dimension_x': item.dimension_x,
                    'dimension_y': item.dimension_y,
                    'dimension_z': item.dimension_z,
                    'weight': item.weight,
                    'is_bag': item.is_bag,
                    'traveler_id': traveler_id,
                    'reference_pk': item.reference_pk
                }
                item = Item.objects.create(**temp_item_data)
                copied_items.append(item)

        traveler = User.objects.get(pk=traveler_id)
        new_pack = Pack.objects.create(name=self.name, traveler=traveler)
        new_pack.items.set(copied_items)
        return new_pack