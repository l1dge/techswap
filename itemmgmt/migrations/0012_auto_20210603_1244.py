# Generated by Django 3.2.3 on 2021-06-03 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0005_rename_zip_address_zipcode'),
        ('itemmgmt', '0011_photos_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='file_loc',
        ),
        migrations.RemoveField(
            model_name='photos',
            name='upload',
        ),
        migrations.AlterField(
            model_name='items',
            name='feedback',
            field=models.ManyToManyField(default=None, related_name='ItemFeedback', to='usermgmt.Feedback'),
        ),
    ]