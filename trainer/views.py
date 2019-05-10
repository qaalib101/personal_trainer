from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .forms import UserRegistrationForm, NewClientForm, NewRegimenForm
from .models import Regimen, Client, CustomUser as User, Notification
from datetime import datetime
from django.http import Http404

# Create your views here.


def homepage(request):
    return render(request, 'trainer/home.html')


def logout_user(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('trainer:edit_profile')
        else:
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html',
                          {'form': form, 'message': message})
    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})


@login_required
def user_profile(request, user_pk):
    try:
        user = User.objects.get(pk=user_pk)
        if user.is_trainer:
            notifications = Notification.objects.all().order_by('date').reverse()
            clients = Client.objects.all().order_by('user.date_joined').reverse()
            return render(request, 'users/trainer.html', {'clients': clients, 'notifications': notifications})
        else:
            try:
                client = Client.objects.get(user=user)
                regimen = Regimen.objects.get(user=user)
                return render(request, 'users/profile.html', {'client': client, 'regimen': regimen})
            except Client.DoesNotExist:
                return redirect('trainer:edit_profile')
            except Regimen.DoesNotExist:
                client = Client.objects.get(user=user)
                return render(request, 'users/profile.html', {'client': client})
    except User.DoesNotExist:
        return render(request, 'registration/')


@login_required
def setup_client(request):
    user = request.user
    clientForm = NewClientForm()
    try:
        instance = Client.objects.get(user=user)
        clientForm = NewClientForm(request.POST, instance=instance)
    except Client.DoesNotExist:
        clientForm = NewClientForm(request.POST)
    if request.method == 'POST':
        if clientForm.is_valid():
            form = clientForm.save(commit=False)
            form.user = user
            form.save()
            date = datetime.now()
            message = 'New client signed up'
            link = f'/user/profile/{user.pk}/'
            notification = Notification(user=user, message=message, link=link, date=date)
            notification.save()
            return redirect('trainer:user_profile', user_pk=user.pk)
        else:
            message = 'Form is not valid'
            return render(request, 'users/setup_client.html', {'form': clientForm, 'message': message})
    else:
        return render(request, 'users/setup_client.html', {'form': clientForm})


@login_required
def add_regimen(request):
    user = request.user
    form = NewRegimenForm(request.POST)
    try:
        instance = Regimen.objects.get(user=user)
        form = NewRegimenForm(request.POST, instance=instance)
    except Regimen.DoesNotExist:
        form = NewRegimenForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            regimen = form.save(commit=False)
            regimen.user = user
            regimen.save()
            return redirect('trainer:edit_regimen', user_pk=user.pk)
        else:
            message = 'Invalid form'
            return render(request, 'trainer/regimen/setup_regimen.html', {'message': message, 'form': form})
    else:
        return render(request, 'trainer/regimen/setup_regimen.html', {'form': form})
