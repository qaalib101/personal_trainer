from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from PIL import Image
# Create your submodels here.


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(max_length=300)
    date = models.DateTimeField()
    link = models.CharField(max_length=300, blank=True, null=True)


class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=4, decimal_places=1)


class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthday = models.DateField()
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)
    weight = models.DecimalField(decimal_places=1, max_digits=4)

    def change_weight(self, weight):
        self.weight = weight
        self.save()


class Exercise(models.Model):
    TYPES = [
        ('FR', 'Free Range'),
        ('MC', 'Machine'),
        ('CL', 'Calisthenics'),
        ('MB', 'Medicine Balls/Sand bags'),
        ('SP', 'Suspension'),
        ('RB', 'Resistance Bands')
    ]
    name = models.CharField(max_length=128)
    type = models.CharField(
        max_length=20,
        choices=TYPES,
        default='1'
    )

    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name = models.CharField(max_length=128)
    commenName = models.CharField(max_length=128)
    location = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Activation(models.Model):
    muscle = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return ('Activation of ' + str(self.muscle) + ' by ' + str(self.exercise))