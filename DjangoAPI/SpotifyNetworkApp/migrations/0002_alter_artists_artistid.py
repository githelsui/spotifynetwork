# Generated by Django 4.2.8 on 2023-12-30 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SpotifyNetworkApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artists',
            name='ArtistId',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]