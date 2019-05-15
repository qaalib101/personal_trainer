from django import forms
from .models import Progress, Client, CustomUser as User

from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def clean_username(self):

        username = self.cleaned_data['username']
        username = ''.join([c.lower() for c in username])
        if not username:
            raise ValidationError('Please enter a username')

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('A user with that username already exists')

        return username


    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError('Please enter your first name')

        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError('Please enter your last name')

        return last_name


    def clean_email(self):
        email = self.cleaned_data['email']
        email = ''.join([c.lower()for c in email])
        if not email:
            raise ValidationError('Please enter an email address')

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with that email address already exists')

        return email


    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class NewClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('birthday', 'photo', 'weight')

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        if not birthday:
            raise ValidationError('Please enter a birthday')
        return birthday

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if not weight:
            raise ValidationError('Please enter a bmi')
        return weight


    def save(self, commit=True):
        client = super(NewClientForm, self).save(commit=False)
        client.birthday = self.cleaned_data['birthday']
        client.photo = self.cleaned_data['photo']
        client.weight = self.cleaned_data['weight']

        if commit:
            client.save()

        return client


class NewProgressForm(forms.ModelForm):

    class Meta:
        model = Progress
        fields = ('weight',)
