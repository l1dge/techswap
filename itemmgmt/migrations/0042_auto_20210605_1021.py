# Generated by Django 3.2.3 on 2021-06-05 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("itemmgmt", "0041_rename_categories_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="item",
            name="category",
        ),
        migrations.AddField(
            model_name="item",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="itemmgmt.category",
            ),
            preserve_default=False,
        ),
    ]