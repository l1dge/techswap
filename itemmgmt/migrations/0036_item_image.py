# Generated by Django 3.2.3 on 2021-06-05 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0035_alter_itemimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.FileField(default=None, upload_to='', verbose_name='uploads/'),
            preserve_default=False,
        ),
    ]
