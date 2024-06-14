# Generated by Django 5.0.6 on 2024-06-14 12:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('initial_sender_secret', models.TextField()),
                ('initial_recipient_secret', models.TextField()),
                ('recipient_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_channels', to=settings.AUTH_USER_MODEL)),
                ('sender_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_channels', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
