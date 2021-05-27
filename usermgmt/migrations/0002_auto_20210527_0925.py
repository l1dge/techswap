# Generated by Django 3.2.3 on 2021-05-27 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('swaplist', '0002_auto_20210527_0925'),
        ('usermgmt', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='City',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='Country',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='County',
            new_name='county',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='HouseNum',
            new_name='house_num',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='Street',
            new_name='street',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='Town',
            new_name='town',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='Zip',
            new_name='zip',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='Comments',
            new_name='comments',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='Status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='Address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='Email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='EmailVerified',
            new_name='email_verified',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='Phone',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='Rating',
            new_name='rating',
        ),
        migrations.RemoveField(
            model_name='address',
            name='ID',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='ID',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='ID',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='Username',
        ),
        migrations.AddField(
            model_name='address',
            name='id',
            field=models.BigAutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedback',
            name='id',
            field=models.BigAutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='feedback',
            field=models.ManyToManyField(related_name='Feedback', to='usermgmt.Feedback'),
        ),
        migrations.AddField(
            model_name='profile',
            name='id',
            field=models.BigAutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]