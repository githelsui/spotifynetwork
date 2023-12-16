# Generated by Django 4.2.8 on 2023-12-15 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artists',
            fields=[
                ('ArtistId', models.AutoField(primary_key=True, serialize=False)),
                ('ArtistName', models.CharField(max_length=100)),
                ('ArtistFollowers', models.IntegerField()),
                ('ArtistGenre', models.CharField(max_length=100)),
                ('ArtistRank', models.IntegerField()),
                ('SimilarArtists', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('UserId', models.AutoField(primary_key=True, serialize=False)),
                ('UserName', models.CharField(max_length=100)),
            ],
        ),
    ]