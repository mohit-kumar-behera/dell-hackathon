# Generated by Django 3.2.11 on 2022-01-22 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20220122_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=120, null=True, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Password'),
        ),
    ]
