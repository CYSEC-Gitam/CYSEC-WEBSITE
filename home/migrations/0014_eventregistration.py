# Generated by Django 4.2 on 2023-08-26 12:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_delete_eventregistration_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField()),
                ('email', models.EmailField(max_length=1024)),
                ('registered_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('fullname', models.CharField(max_length=200)),
                ('registration_no', models.CharField(max_length=20)),
                ('study_year', models.CharField(max_length=1)),
                ('campus', models.CharField(max_length=100)),
            ],
        ),
    ]
