# Generated by Django 3.2.3 on 2021-06-05 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0040_item_uploaded_at'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
    ]