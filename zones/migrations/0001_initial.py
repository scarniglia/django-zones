# Generated by Django 2.1.7 on 2019-02-14 14:45

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('language', models.CharField(max_length=2)),
                ('currency', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('poly', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='zones.Provider')),
            ],
        ),
    ]
