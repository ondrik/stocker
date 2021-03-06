# Generated by Django 3.0.3 on 2020-02-28 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('unit_price', models.DecimalField(decimal_places=6, max_digits=20)),
                ('fee', models.DecimalField(decimal_places=6, max_digits=20)),
                ('date', models.DateTimeField(verbose_name='Execution date and time')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stockerapp.Stock')),
            ],
        ),
    ]
