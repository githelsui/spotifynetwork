# Generated by Django 4.2.8 on 2023-12-22 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SpotifyNetworkApp', '0005_alter_users_useremail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='UserEmail',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]