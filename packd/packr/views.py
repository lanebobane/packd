from django.shortcuts import render, redirect
from .models import Item, Pack
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required
def dashboard(request):
    packing_items = Item.objects.filter(is_bag=False, traveler=request.user)
    bags = Item.objects.filter(is_bag=True, traveler=request.user)
    packs = Pack.objects.filter(traveler=request.user)
    context = {
    	'packing_items': packing_items,
    	'bags': bags,
    	'packs': packs
    }
    
    return render(request, 'packr/dashboard.html', context)


@login_required
def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        weight = request.POST.get('weight')
        dimension_x = request.POST.get('dimension_x')
        dimension_y = request.POST.get('dimension_y')
        dimension_z = request.POST.get('dimension_z')
        is_packable = True if request.POST.get('packable_yes') == 'on' else False
        
        item = Item(name=name, weight=weight, dimension_x=dimension_x, dimension_y=dimension_y, dimension_z=dimension_z, is_bag=is_packable, traveler=request.user)
        item.save()

    
    return render(request, 'packr/additem.html')

def home(request):
    return render(request, 'packr/home.html')

def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/dashboard')