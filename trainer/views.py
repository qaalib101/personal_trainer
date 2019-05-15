from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .forms import UserRegistrationForm, NewProgressForm
from .models import Progress, Client, CustomUser as User, Notification
from datetime import datetime, timezone
from .views_client import save_notification

# Create your views here.


def homepage(request):
    return redirect('trainer:my_user_profile')

@login_required
def my_user_profile(request):
    user_pk = request.user.pk
    return redirect('trainer:user_profile', user_pk=user_pk)

def logout_user(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            tz = datetime.now(timezone.utc).astimezone().tzinfo
            date = datetime.now(tz=tz)
            user.date_joined = date
            user.save()
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
        form = NewProgressForm()
        if user.is_trainer:
            if request.user.is_trainer:
                notifications = Notification.objects.all().order_by('date').reverse()
                clients = Client.objects.raw('select * from trainer_client'
                                         ' inner join trainer_customuser on trainer_client.user_id = trainer_customuser.id'
                                             ' order by trainer_customuser.date_joined desc')
                history = Progress.objects.all().order_by('date').reverse()
                return render(request, 'users/trainer.html', {'clients': clients, 'notifications': notifications, 'history' :history})
            else:
                return redirect('trainer:my_user_profile')
        else:
            try:
                client = Client.objects.get(user=user)
                return render(request, 'users/profile.html', {'client': client, 'form': form})
            except Client.DoesNotExist:
                return redirect('trainer:edit_profile')
    except User.DoesNotExist:
        return render(request, 'registration/login.html')
