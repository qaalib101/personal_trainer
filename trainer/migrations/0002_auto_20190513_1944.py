# Generated by Django 2.2.1 on 2019-05-14 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
