# Generated by Django 3.2.3 on 2021-06-04 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0034_alter_itemimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemimage',
            name='image',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]