from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            print('valid form!')
            user = form.save()
            return redirect('/dashboard')
        else:
            print('invalid fomrm!')
        # print(form)

    form = NewUserForm()
    context = {
        'form': form
    }

    return render(request, 'register.html', context)

@login_required
def profile(request):
    # context = {
    #     ''
    # }
    return render(request, 'profile.html')


def create_profile(request):
    if request.method == "POST":
        user = request.user
        profile = Profile(
            user=user,
        )
        profile.save()

    return render(request, 'createprofile.html')

def seller_profile(request, id):
    seller = User.objects.get(id=id)
    context = {
        'seller': seller
    }
    return render(request, 'sellerprofile.html', context)