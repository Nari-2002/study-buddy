# Generated by Django 5.1.2 on 2024-11-05 09:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_room_options_room_participents'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='participents',
            field=models.ManyToManyField(blank=True, related_name='participents', to=settings.AUTH_USER_MODEL),
        ),
    ]
