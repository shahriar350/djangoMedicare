# Generated by Django 3.2.5 on 2022-01-06 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0009_auto_20220106_1739'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminbasicinfo',
            old_name='websiteTile',
            new_name='websiteTitle',
        ),
    ]