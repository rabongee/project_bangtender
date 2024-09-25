# Generated by Django 4.2 on 2024-09-25 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('liquor', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='My_Liquor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', '내가 보유한 술'), ('2', '좋아하는 술'), ('3', '싫어하는 술')], max_length=1)),
                ('liquor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_liquor', to='liquor.liquor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='likeliquor',
            name='liquor',
        ),
        migrations.RemoveField(
            model_name='likeliquor',
            name='user',
        ),
        migrations.RemoveField(
            model_name='myliquor',
            name='liquor',
        ),
        migrations.RemoveField(
            model_name='myliquor',
            name='user',
        ),
        migrations.DeleteModel(
            name='DislikeLiquor',
        ),
        migrations.DeleteModel(
            name='LikeLiquor',
        ),
        migrations.DeleteModel(
            name='MyLiquor',
        ),
    ]
