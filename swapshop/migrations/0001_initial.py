# Generated by Django 3.2.4 on 2021-06-17 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import location_field.models.plain


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('comments', models.TextField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(default='', editable=False, max_length=255, unique=True)),
                ('description', models.TextField(default=None, max_length=500)),
                ('image', models.FileField(upload_to='items')),
                ('condition', models.CharField(choices=[('Like New', 'Like New'), ('Excelllent', 'Excelllent'), ('Good', 'Good'), ('Used', 'Used'), ('Poor', 'Poor'), ('Spares or Repair', 'Spares or Repair')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.CharField(max_length=255)),
                ('location', location_field.models.plain.PlainLocationField(max_length=63)),
                ('swap_comp', models.BooleanField(default=False)),
                ('archived', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('swap_agrd', models.BooleanField(default=False)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('category', models.ManyToManyField(to='swapshop.Category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('town', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('county', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('zip', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Wanted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_req', models.CharField(max_length=200)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swapshop.item')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swapshop.location')),
                ('user_id', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Swap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_by', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('swap_status', models.CharField(choices=[('Item Active', 'Item Active'), ('Item Wanted', 'Item Wanted'), ('Swap Initiated', 'Swap Initiated'), ('Swap Agreed', 'Swap Agreed'), ('Swap Complete', 'Swap Complete'), ('Swap Cancelled', 'Swap Cancelled')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('swap_completed', models.BooleanField(blank=True, default=False, null=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='swapshop.cart')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='profile_images')),
                ('rating', models.IntegerField(blank=True, default=0)),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='bio')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('feedback', models.ManyToManyField(blank=True, related_name='Feedback', to='swapshop.Feedback')),
                ('items', models.ManyToManyField(blank=True, related_name='Items', to='swapshop.Item')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='items/multimages/')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swapshop.item')),
            ],
        ),
        migrations.CreateModel(
            name='ForSwap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('swap_avail', models.BooleanField(default=False)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ItemID', to='swapshop.item')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swapshop.location')),
                ('user_id', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='feedback',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='swapshop.item'),
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swapshop.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swapshop.item')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_num', models.CharField(blank=True, max_length=200, null=True)),
                ('street', models.CharField(blank=True, max_length=200, null=True)),
                ('town', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('county', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
