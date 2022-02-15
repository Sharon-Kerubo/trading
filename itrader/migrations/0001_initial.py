# Generated by Django 4.0 on 2022-02-15 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('security', models.CharField(max_length=20)),
                ('lastprice', models.IntegerField()),
                ('demandqty', models.IntegerField()),
                ('demandprice', models.IntegerField()),
                ('supplyprice', models.IntegerField()),
                ('supplyqty', models.IntegerField()),
                ('lastqty', models.IntegerField()),
                ('high', models.IntegerField()),
                ('low', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buysell', models.CharField(max_length=20)),
                ('market', models.CharField(max_length=20)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('validupto', models.DateField()),
                ('delivery', models.CharField(max_length=20)),
                ('clientcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('security', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itrader.stockdata')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('users', models.ManyToManyField(blank=True, help_text='users who are connected to the chat', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('date_added', models.DateTimeField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'ordering': ('date_added',),
            },
        ),
    ]
