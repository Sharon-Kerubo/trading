# Generated by Django 4.0 on 2022-02-18 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itrader', '0003_trade_dateplaced'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itrader.stockdata'),
        ),
    ]
