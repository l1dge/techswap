# Generated by Django 3.2.3 on 2021-06-05 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0042_auto_20210605_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ManyToManyField(to='itemmgmt.Category'),
        ),
    ]
