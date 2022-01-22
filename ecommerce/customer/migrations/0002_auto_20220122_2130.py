# Generated by Django 3.2.11 on 2022-01-22 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.AddField(
            model_name='customer',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Joined'),
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='m@m.com', max_length=120, unique=True, verbose_name='Email Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='first_name',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default='mohit', max_length=255, verbose_name='Password'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated Account at'),
        ),
    ]