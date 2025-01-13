# Generated by Django 5.1.4 on 2025-01-13 23:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_alter_category_options_alter_category_description_and_more'),
        ('command', '0005_command_tooltip'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='copyCount',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='command',
            name='description',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='command',
            name='example',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='command',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commands', to='category.subcategory'),
        ),
    ]
