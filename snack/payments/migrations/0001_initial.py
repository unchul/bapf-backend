# Generated by Django 5.1.7 on 2025-06-25 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_key', models.CharField(max_length=255)),
                ('order_id', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('provider', models.CharField(max_length=100)),
                ('method', models.CharField(max_length=100)),
                ('paid_at', models.DateTimeField()),
                ('receipt_url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='account.account')),
                ('orders_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='orders.orders')),
            ],
            options={
                'db_table': 'payments',
            },
        ),
    ]
