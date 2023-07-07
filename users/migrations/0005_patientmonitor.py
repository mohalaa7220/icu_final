# Generated by Django 4.2 on 2023-07-07 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_is_headnursing'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientMonitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ecg', models.CharField(max_length=220)),
                ('resp', models.CharField(max_length=220)),
                ('spo2', models.CharField(max_length=220)),
                ('co2', models.CharField(max_length=220)),
                ('ibp', models.CharField(max_length=220)),
                ('nibp', models.CharField(max_length=220)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
