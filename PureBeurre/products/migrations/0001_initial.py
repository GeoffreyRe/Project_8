# Generated by Django 3.0.5 on 2020-04-06 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('barcode', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=80)),
                ('brand', models.CharField(max_length=80)),
                ('url', models.URLField()),
                ('nutrition_grade', models.CharField(max_length=1)),
                ('nutrition_score', models.SmallIntegerField()),
            ],
        ),
    ]