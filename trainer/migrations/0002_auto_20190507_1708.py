# Generated by Django 2.2.1 on 2019-05-07 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='bmi',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
    ]
