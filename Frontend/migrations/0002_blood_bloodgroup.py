# Generated by Django 3.2.5 on 2022-01-05 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Blood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('blood', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_blood_group', to='Frontend.bloodgroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_blood', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
