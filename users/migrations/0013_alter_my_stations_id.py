# Generated by Django 3.2.4 on 2021-07-05 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_my_stations_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='my_stations',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
