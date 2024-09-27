# Generated by Django 4.2 on 2024-09-26 02:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('liquor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='my_liquor',
            name='liquor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_liquor', to='liquor.liquor'),
        ),
        migrations.AddField(
            model_name='my_liquor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
