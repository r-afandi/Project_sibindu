# Generated by Django 5.0.7 on 2024-12-17 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0077_statuspenyakit_badge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diagnosa',
            old_name='status',
            new_name='status_id',
        ),
        migrations.AlterField(
            model_name='statuspenyakit',
            name='badge',
            field=models.CharField(max_length=20),
        ),
    ]
