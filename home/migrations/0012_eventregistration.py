# Generated by Django 4.2 on 2023-08-18 00:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_rename_link_events_whatsapp_group_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField(max_length=1024)),
                ('email', models.EmailField(max_length=1024)),
                ('registered_datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]