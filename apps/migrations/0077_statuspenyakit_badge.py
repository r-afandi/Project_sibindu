# Generated by Django 5.0.7 on 2024-12-17 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0076_alter_diagnosa_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuspenyakit',
            name='badge',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
