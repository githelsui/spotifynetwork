# Generated by Django 4.2.8 on 2023-12-16 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SpotifyNetworkApp', '0002_artistassocs'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistassocs',
            name='UserId',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]