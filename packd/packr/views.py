from django.shortcuts import render, redirect, reverse
from .forms import ItemForm, PackForm
from .models import Item, Pack
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden



# Create your views here.

@login_required
def dashboard(request):
    items = Item.objects.filter(is_bag=False, traveler=request.user)
    bags = Item.objects.filter(is_bag=True, traveler=request.user)
    packs = Pack.objects.filter(traveler=request.user)
    context = {
    	'items': items,
    	'bags': bags,
    	'packs': packs
    }

    return render(request, 'packr/dashboard.html', context)


@login_required
def add_item(request, **kwargs):
    pk = kwargs.get('pk')
    if pk:
        item = get_object_or_404(Item, pk=pk)
        if item.traveler != request.user:
            return HttpResponseForbidden()
    else:
        item = Item(traveler=request.user)

    form = ItemForm(request.POST or None, instance=item)

    if request.method == 'POST' and form.is_valid():
        item = form.save()
        return redirect('/items/add')

    context = { 'form': form }
    
    return render(request, 'packr/additem.html', context)

@login_required
def add_pack(request, **kwargs):
    pk = kwargs.get('pk')
    if pk:
        pack = get_object_or_404(Pack, pk=pk)
        if pack.traveler != request.user:
            return HttpResponseForbidden()
    else:
        pack = Pack(traveler=request.user)

    form = PackForm(request.POST or None, instance=pack)
    form.fields['bag'].queryset = Item.objects.filter(is_bag=True, traveler=request.user)
    form.fields['items'].queryset = Item.objects.filter(traveler=request.user)

    if request.method == 'POST' and form.is_valid():
        pack = form.save()
        return redirect('/dashboard')

    context = { 'form': form }
    
    return render(request, 'packr/addpack.html', context)


def home(request):
    anonymous_packs = Pack.objects.filter(traveler=None)
    context = {'packs': anonymous_packs}
    return render(request, 'packr/home.html', context)

def share_pack(request, pk):
    if request.method == 'POST':
        obj = Pack.objects.filter(pk=pk)
        copied_items = obj[0].items.all()
        data = dict(obj.values()[0])
        data.pop('id')
        data.pop('traveler_id')
        #TODO: Do we want to add an option to share bag? Same with adopt. 
        data.pop('bag_id')
        pack = Pack.objects.create(**data)
        pack.items.set(copied_items)

        return redirect('/dashboard')

# TODO: When adopting a pack, should the user also gain copies of the included items? 
def adopt_pack(request, pk):
    if request.method == 'POST':
        obj = Pack.objects.filter(pk=pk)
        copied_items = obj[0].items.all()
        data = dict(obj.values()[0])
        data.pop('id')
        data['traveler_id'] = request.user.id
        pack = Pack.objects.create(**data)
        pack.items.set(copied_items)

        return redirect('/dashboard')

def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()

        return redirect('/dashboard')

def delete_pack(request, pk):
    pack = get_object_or_404(Pack, pk=pk)
    if request.method == 'POST':
        pack.delete()

        return redirect('/dashboard')