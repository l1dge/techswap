# Generated by Django 3.2.4 on 2021-07-08 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swapshop', '0014_auto_20210708_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='swap',
            name='swap_list',
        ),
        migrations.AddField(
            model_name='swap',
            name='swap_list',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='swapshop.swaplist'),
            preserve_default=False,
        ),
    ]
