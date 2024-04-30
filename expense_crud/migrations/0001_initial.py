# Generated by Django 5.0.3 on 2024-04-24 09:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='IncomeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('full_name', models.CharField(max_length=100)),
                ('profile_picture', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('income_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_crud.incometype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_crud.user')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_crud.currency')),
                ('expense_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_crud.expensetype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_crud.user')),
            ],
        ),
    ]
