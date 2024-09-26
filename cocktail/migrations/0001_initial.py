# Generated by Django 4.2 on 2024-09-26 02:08

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
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='cocktails/')),
                ('content', models.TextField()),
                ('ingredients', models.TextField()),
                ('taste', models.CharField(max_length=100)),
                ('abv', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bookmarked_by', models.ManyToManyField(blank=True, related_name='bookmarked_cocktails', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
