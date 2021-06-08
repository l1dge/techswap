# Generated by Django 3.2.3 on 2021-06-04 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0028_auto_20210604_0729'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(default=None, max_length=500)),
                ('condition', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('swap_comp', models.BooleanField(default=False)),
                ('archived', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('swap_agrd', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='', verbose_name='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='items',
            name='category',
        ),
        migrations.RemoveField(
            model_name='items',
            name='upload',
        ),
    ]