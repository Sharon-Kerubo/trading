# Generated by Django 4.0 on 2022-03-15 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itrader', '0004_alter_room_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
                ('content', models.CharField(max_length=200)),
                ('date', models.CharField(max_length=200)),
            ],
        ),
    ]