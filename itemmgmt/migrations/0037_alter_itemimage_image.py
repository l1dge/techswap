# Generated by Django 3.2.3 on 2021-06-05 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0036_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemimage',
            name='image',
            field=models.FileField(upload_to='', verbose_name='uploads/'),
        ),
    ]