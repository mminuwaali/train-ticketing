# Generated by Django 5.0.3 on 2024-04-18 18:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_schedule_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='landing.train'),
        ),
    ]
