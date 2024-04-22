# Generated by Django 5.0.3 on 2024-04-20 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_contact_ticket_booking'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='booking',
            name='type',
        ),
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('expired', 'expired'), ('success', 'success')], default='pending', max_length=20),
        ),
    ]
