from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(max_length=300)
    date = models.DateTimeField()
    link = models.CharField(max_length=300, blank=True, null=True)


class Regimen(models.Model):
    Choice = (
        (1, 'Zeus'),
        (2, 'Apollo'),
        (3, 'Prometheus')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.IntegerField(choices=Choice)
    time = models.IntegerField(default=35)
    progress = models.DecimalField(default=0.0, max_digits=3, decimal_places=2)

    def add_progress(self):
        self.progress += 0.2


class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthday = models.DateField()
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)
    bmi = models.DecimalField(decimal_places=1, max_digits=3)


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password):

        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_trainer = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    username = models.CharField(max_length=128, blank=False, unique=True)
    email = models.CharField(max_length=128, unique=True, blank=False)
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    objects = MyUserManager()
    is_trainer = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.username

