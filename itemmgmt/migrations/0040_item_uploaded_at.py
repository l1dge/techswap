# Generated by Django 3.2.3 on 2021-06-05 08:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0039_auto_20210605_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
