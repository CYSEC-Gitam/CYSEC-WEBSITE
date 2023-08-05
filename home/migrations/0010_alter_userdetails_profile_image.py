# Generated by Django 4.2 on 2023-08-05 12:14

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_userdetails_discord_link_alter_userdetails_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='profile_image',
            field=models.ImageField(blank=True, default='https://img.freepik.com/premium-vector/anonymous-user-circle-icon-vector-illustration-flat-style-with-long-shadow_520826-1931.jpg?size=626&ext=jpg', null=True, upload_to=home.models.generate_profile_image_filename),
        ),
    ]
