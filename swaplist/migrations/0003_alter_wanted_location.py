# Generated by Django 3.2.3 on 2021-05-28 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0002_auto_20210527_0925'),
        ('swaplist', '0002_auto_20210527_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wanted',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itemmgmt.location'),
        ),
    ]