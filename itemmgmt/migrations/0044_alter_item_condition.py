# Generated by Django 3.2.3 on 2021-06-07 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0043_auto_20210605_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='condition',
            field=models.CharField(choices=[('Like New', 'Like New'), ('Excelllent', 'Excelllent'), ('Good', 'Good'), ('Used', 'Used'), ('Poor', 'Poor'), ('Spares or Repair', 'Spares or Repair')], max_length=50),
        ),
    ]
