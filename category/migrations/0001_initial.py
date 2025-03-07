# Generated by Django 5.1.4 on 2025-03-02 01:02

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('title', models.CharField(blank=True, max_length=40, null=True)),
                ('title_en', models.CharField(blank=True, max_length=40, null=True)),
                ('title_de', models.CharField(blank=True, max_length=40, null=True)),
                ('description', models.TextField(blank=True, max_length=10000, null=True)),
                ('description_en', models.TextField(blank=True, max_length=10000, null=True)),
                ('description_de', models.TextField(blank=True, max_length=10000, null=True)),
                ('type', models.CharField(choices=[('command', 'Command'), ('routine', 'Routine'), ('function', 'Function')], default='command', max_length=10)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('title', models.CharField(blank=True, max_length=40, null=True)),
                ('title_en', models.CharField(blank=True, max_length=40, null=True)),
                ('title_de', models.CharField(blank=True, max_length=40, null=True)),
                ('description', models.TextField(blank=True, max_length=10000, null=True)),
                ('description_en', models.TextField(blank=True, max_length=10000, null=True)),
                ('description_de', models.TextField(blank=True, max_length=10000, null=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='category.category')),
            ],
            options={
                'verbose_name': 'Subcategory',
                'verbose_name_plural': 'Subcategories',
            },
        ),
    ]
