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
    context = {"items": items, "bags": bags, "packs": packs}

    return render(request, "packr/dashboard.html", context)


@login_required
def add_item(request, **kwargs):
    pk = kwargs.get("pk")
    if pk:
        item = get_object_or_404(Item, pk=pk)
        if item.traveler != request.user:
            return HttpResponseForbidden()
    else:
        item = Item(traveler=request.user)

    form = ItemForm(request.POST or None, instance=item)

    if request.method == "POST" and form.is_valid():
        item = form.save()
        item.reference_pk = item.id
        item.save()
        return redirect("/items/add")

    context = {"form": form}

    return render(request, "packr/additem.html", context)


@login_required
def add_pack(request, **kwargs):
    pk = kwargs.get("pk")
    if pk:
        pack = get_object_or_404(Pack, pk=pk)
        if pack.traveler != request.user:
            return HttpResponseForbidden()
    else:
        pack = Pack(traveler=request.user)

    form = PackForm(request.POST or None, instance=pack)
    form.fields["bag"].queryset = Item.objects.filter(
        is_bag=True, traveler=request.user
    )
    form.fields["items"].queryset = Item.objects.filter(traveler=request.user)

    if request.method == "POST" and form.is_valid():
        pack = form.save()
        return redirect("/dashboard")

    context = {"form": form}

    return render(request, "packr/addpack.html", context)


def shared_packs(request):
    anonymous_packs = Pack.objects.filter(traveler=None)
    context = {"packs": anonymous_packs}
    return render(request, "packr/sharedpacks.html", context)


def share_pack(request, pk):
    if request.method == "POST":
        pack = Pack.objects.get(pk=pk)
        shared_pack = pack.share_pack()
        return redirect("/dashboard")


def adopt_pack(request, pk):
    if request.method == "POST":
        pack = Pack.objects.get(pk=pk)
        adopted_pack = pack.adopt_pack(request.user.id)
        return redirect("/dashboard")

        
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()

        return redirect("/dashboard")


def delete_pack(request, pk):
    pack = get_object_or_404(Pack, pk=pk)
    if request.method == "POST":
        pack.delete()

        return redirect("/dashboard")
