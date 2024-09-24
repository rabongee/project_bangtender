# Generated by Django 4.2 on 2024-09-25 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.PositiveIntegerField()),
                ('img', models.ImageField(upload_to='liquor/')),
            ],
        ),
        migrations.CreateModel(
            name='Liquor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('classification', models.CharField(max_length=20)),
                ('img', models.ImageField(upload_to='liquor/')),
                ('content', models.TextField()),
                ('taste', models.CharField(max_length=100)),
                ('abv', models.FloatField()),
                ('price', models.PositiveIntegerField()),
            ],
        ),
    ]
