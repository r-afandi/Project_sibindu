# Generated by Django 5.0.3 on 2024-05-18 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0018_remove_diagnosa_kode'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosa',
            name='kode',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='apps.tipepenyakit'),
        ),
    ]
