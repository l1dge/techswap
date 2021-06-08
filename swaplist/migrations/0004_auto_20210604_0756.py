# Generated by Django 3.2.3 on 2021-06-04 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0029_auto_20210604_0756'),
        ('swaplist', '0003_alter_wanted_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forswap',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ItemID', to='itemmgmt.item'),
        ),
        migrations.AlterField(
            model_name='wanted',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itemmgmt.item'),
        ),
    ]