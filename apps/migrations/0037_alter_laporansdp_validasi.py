# Generated by Django 5.0.6 on 2024-06-13 06:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0036_about_alamat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laporansdp',
            name='validasi',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='apps.validasi'),
        ),
    ]
