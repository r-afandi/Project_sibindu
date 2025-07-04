# Generated by Django 5.0.7 on 2024-10-08 03:01

import apps.base.posbindu.models.informasi.m_artikel
import apps.base.posbindu.models.laporan.m_laporan_kegiatan
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0066_alter_artikel_judul_alter_notifikasi_nama'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artikel',
            name='gambar',
            field=models.ImageField(max_length=255, null=True, upload_to=apps.base.posbindu.models.informasi.m_artikel.upload_path_img),
        ),
        migrations.AlterField(
            model_name='laporankegiatan',
            name='foto',
            field=models.ImageField(max_length=255, null=True, upload_to=apps.base.posbindu.models.laporan.m_laporan_kegiatan.upload_path_img),
        ),
        migrations.AlterField(
            model_name='laporansdp',
            name='bukti',
            field=models.ImageField(max_length=255, null=True, upload_to=''),
        ),
    ]
