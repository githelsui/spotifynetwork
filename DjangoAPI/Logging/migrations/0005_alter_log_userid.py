# Generated by Django 4.2.8 on 2024-01-04 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Logging', '0004_log_sessionid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='UserId',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
