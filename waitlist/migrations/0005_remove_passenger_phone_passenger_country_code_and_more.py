# Generated by Django 5.2.4 on 2025-07-14 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waitlist', '0004_remove_passenger_country_code_alter_passenger_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passenger',
            name='phone',
        ),
        migrations.AddField(
            model_name='passenger',
            name='country_code',
            field=models.CharField(default='+353', max_length=6),
        ),
        migrations.AddField(
            model_name='passenger',
            name='local_phone',
            field=models.CharField(default='353', max_length=20),
            preserve_default=False,
        ),
    ]
