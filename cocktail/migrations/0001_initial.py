# Generated by Django 4.2 on 2024-10-07 07:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cocktail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('img', models.ImageField(upload_to='cocktails/')),
                ('content', models.TextField()),
                ('ingredients', models.TextField()),
                ('taste', models.CharField(max_length=500)),
                ('abv', models.DecimalField(decimal_places=1, max_digits=3)),
                ('bookmark', models.ManyToManyField(blank=True, related_name='cocktail_bookmark', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
