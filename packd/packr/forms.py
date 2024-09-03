from .models import Item, Pack

from django import forms


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = [
            "name",
            "weight",
            "dimension_x",
            "dimension_y",
            "dimension_z",
            "is_bag",
        ]

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.widget.input_type == 'checkbox':
                visible.field.widget.attrs['class'] = 'form-control-checkbox'
            else:    
                visible.field.widget.attrs['class'] = 'form-control'


class PackForm(forms.ModelForm):

    class Meta:
        model = Pack
        fields = ["name", "bag", "items"]

    def __init__(self, *args, **kwargs):
        super(PackForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.widget.input_type == 'checkbox':
                visible.field.widget.attrs['class'] = 'form-control-checkbox'
            else:    
                visible.field.widget.attrs['class'] = 'form-control'
