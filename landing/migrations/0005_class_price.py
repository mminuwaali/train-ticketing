# Generated by Django 5.0.3 on 2024-04-20 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_alter_schedule_train'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
