# Generated by Django 3.2.5 on 2022-01-07 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0013_auto_20220108_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='image',
        ),
    ]
