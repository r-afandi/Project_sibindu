# Generated by Django 5.0.7 on 2024-10-08 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0065_alter_artikel_judul'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artikel',
            name='judul',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='notifikasi',
            name='nama',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
