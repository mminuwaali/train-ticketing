# Generated by Django 5.0.3 on 2024-04-18 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='image',
            field=models.ImageField(blank=True, upload_to='trains/'),
        ),
    ]
