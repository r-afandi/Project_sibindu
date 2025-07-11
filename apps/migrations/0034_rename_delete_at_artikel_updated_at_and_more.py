# Generated by Django 5.0.6 on 2024-06-05 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0033_rename_kontak_about_sosmed_remove_about_update_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artikel',
            old_name='delete_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='datasdp',
            old_name='delete_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='laporankegiatan',
            old_name='delete_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='laporansdp',
            old_name='delete_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='pengumuman',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.RemoveField(
            model_name='artikel',
            name='update_at',
        ),
        migrations.RemoveField(
            model_name='datasdp',
            name='update_at',
        ),
        migrations.RemoveField(
            model_name='gejala',
            name='update_at',
        ),
        migrations.RemoveField(
            model_name='laporankegiatan',
            name='update_at',
        ),
        migrations.RemoveField(
            model_name='laporansdp',
            name='update_at',
        ),
        migrations.RemoveField(
            model_name='pakar',
            name='update_at',
        ),
        migrations.AddField(
            model_name='artikel',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datasdp',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gejala',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='laporankegiatan',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='laporansdp',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pakar',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='datasuspek',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='datasuspek',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
