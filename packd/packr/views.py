from django.shortcuts import render
from .models import Item, Pack

# Create your views here.

def dashboard(request):
    packing_items = Item.objects.filter(is_bag=False)
    bags = Item.objects.filter(is_bag=True)
    context = {
    	'packing_items': packing_items,
    	'bags': bags
    }
    
    return render(request, 'dashboard.html', context)