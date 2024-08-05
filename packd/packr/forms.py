from .models import Item

from django import forms


class ItemForm(forms.ModelForm):

	class Meta:
		model = Item
		fields = ["name", "weight", "dimension_x", "dimension_y", "dimension_z", "is_bag"]