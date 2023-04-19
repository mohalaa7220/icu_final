# Generated by Django 4.2 on 2023-04-18 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0003_notificationapp_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationapp',
            name='user_receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_receiver', to=settings.AUTH_USER_MODEL),
        ),
    ]