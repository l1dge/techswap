# Generated by Django 3.2.3 on 2021-06-08 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swapshop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='user',
            new_name='client',
        ),
    ]