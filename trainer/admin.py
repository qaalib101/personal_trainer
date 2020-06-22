from django.contrib import admin
from django.apps import apps
from trainer.models import *
from django.contrib.auth.admin import UserAdmin
# all other submodels
models = apps.get_models()

admin.site.register(CustomUser, UserAdmin)

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
