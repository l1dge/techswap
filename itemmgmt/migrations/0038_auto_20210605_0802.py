# Generated by Django 3.2.3 on 2021-06-05 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0037_alter_itemimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.FileField(upload_to='uploads'),
        ),
        migrations.AlterField(
            model_name='itemimage',
            name='image',
            field=models.FileField(upload_to='uploads'),
        ),
    ]