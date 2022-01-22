# Generated by Django 3.2.11 on 2022-01-22 08:33

from django.db import migrations, models
import product.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Product Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Product Description')),
                ('quantity', models.IntegerField(blank=True, default=1, null=True, validators=[product.models.positive_value])),
                ('price', models.FloatField(blank=True, default=0, null=True, validators=[product.models.positive_value])),
            ],
        ),
    ]
