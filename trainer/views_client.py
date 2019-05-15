from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .forms import UserRegistrationForm, NewClientForm, NewProgressForm
from .models import Progress, Client, CustomUser as User, Notification
from datetime import datetime, timezone, date
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponse
from json import dumps, loads




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
            tz = datetime.now(timezone.utc).astimezone().tzinfo
            date = datetime.now(tz=tz)
            message = 'New client signed up'
            link = f'/user/profile/{user.pk}/'
            save_notification(user, date, message, link)
            return redirect('trainer:user_profile', user_pk=user.pk)
        else:
            message = 'Form is not valid'
            return render(request, 'users/setup_client.html', {'form': clientForm, 'message': message})
    else:
        return render(request, 'users/setup_client.html', {'form': clientForm})


@login_required
def submit_progress(request):
    form = NewProgressForm(request.POST)
    if request.method == 'POST':

        tz = datetime.now(timezone.utc).astimezone().tzinfo
        date = datetime.now(tz=tz)
        progress = form.save(commit=False)
        progress.user = request.user
        progress.date = date
        progress.save()
        client = Client.objects.get(user=request.user)
        client.change_weight(weight=progress.weight)
        message = f'{request.user.username} has submitted their progress.'
        save_notification(request.user, date, message)

        return redirect('trainer:user_profile', user_pk=request.user.pk)


def save_notification(user, date, message, link=None):
    if link == None:
        notification = Notification(user=user, date=date, message=message)
    else:
        notification = Notification(user=user, date=date, message=message, link=link)
    notification.save()
    return notification


@login_required
def get_progress(request, pk):
    user = User.objects.get(id=pk)
    progress = Progress.objects.filter(user_id=pk).values_list('date', 'weight').order_by('date').reverse()
    if user.is_trainer:
        progress = Progress.objects.all().order_by('date').reverse()
    progress = list(progress.values())
    epoch = date(1970, 1, 1)
    for p in progress:
        d = p['date']
        t = (d - epoch).total_seconds()
        p['date'] = t
        p['weight'] = str(p['weight'])
    raw = dumps(progress)
    return HttpResponse(raw)


