# Generated by Django 3.2.4 on 2021-07-09 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swapshop', '0018_auto_20210709_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(default=81, on_delete=django.db.models.deletion.DO_NOTHING, to='swapshop.category'),
            preserve_default=False,
        ),
    ]
