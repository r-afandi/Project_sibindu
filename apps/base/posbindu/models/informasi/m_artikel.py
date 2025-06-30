import os
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from ...models.laporan.m_laporan_sdp import Validasi

def upload_path_img(instance, imagename):
    today = datetime.now().strftime('%Y/%m/%d')
    imagename = f'{today}/{imagename}'
    return upload_path('image/artikel/', imagename)
def upload_path(base, path):
    return os.path.join(base, path)
class Artikel(models.Model):
    id= models.IntegerField
    judul= models.CharField(max_length=255,null=True)
    tanggal= models.CharField(max_length=50,null=True)
    artikel=models.TextField()
    gambar = models.ImageField(upload_to=upload_path_img, null=True, max_length=255) 
    upload=models.CharField(max_length=50,null=True)
    validasi= models.ForeignKey(Validasi, on_delete=models.CASCADE, db_constraint=False, null=True,related_name='validasi')
    info=models.CharField(max_length=50,null=True)
    petugas = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, null=True, related_name='artikel_petugas')
    validator = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, null=True, related_name='artikel_validator')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = "artikel"