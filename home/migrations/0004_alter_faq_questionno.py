# Generated by Django 4.2 on 2023-07-30 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='questionno',
            field=models.IntegerField(unique=True),
        ),
    ]
