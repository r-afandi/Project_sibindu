# Generated by Django 5.0.7 on 2024-10-15 07:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0070_alter_laporansdp_kondisi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laporansdp',
            name='kondisi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.kondisi'),
        ),
    ]
