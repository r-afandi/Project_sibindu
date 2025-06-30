from typing import Any
from django.db import models
from django.urls import reverse
from ...posbindu.models.laporan.m_laporan_sdp import Validasi
class TipePenyakit (models.Model):
    id = models.IntegerField
    kode = models.TextField(null=True)
    nama = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nama

    class Meta:
        db_table = "tipe_penyakit"
class StatusPenyakit (models.Model):
    id = models.IntegerField
    status = models.TextField(null=True)
    badge= models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.status
    class Meta:
        db_table = "status_penyakit"
class Diagnosa(models.Model):
    id = models.IntegerField
    kode = models.CharField(max_length=8)
    diagnosa = models.CharField(max_length=20)
    tipe= models.ForeignKey(TipePenyakit, on_delete=models.CASCADE,db_constraint=False) 
    status = models.ForeignKey(StatusPenyakit, on_delete=models.CASCADE,db_constraint=False)
    data_gejala = models.TextField(null=True)
    data_khusus = models.TextField(null=True) 
    data_luar = models.TextField(null=True)
    data_dalam = models.TextField(null=True)
    penanganan = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.diagnosa

    class Meta:
        db_table = "diagnosa"
 
class Pakar(models.Model):
    id = models.IntegerField
    umur = models.CharField(max_length=20,null=True)
    data_gejala = models.TextField(null=True)  
    data_khusus = models.TextField(null=True)  
    diagnosa = models.ForeignKey(Diagnosa, on_delete=models.CASCADE,db_constraint=False,null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "inference_engine"
class Kepakaran(models.Model):
    id = models.IntegerField
    umur = models.CharField(max_length=20,null=True)
    data_gejala = models.TextField(null=True)  
    data_khusus = models.TextField(null=True) 
    alasan = models.TextField(null=True)
    diagnosa_suspek = models.ForeignKey(Diagnosa, on_delete=models.CASCADE, db_constraint=False, null=True, related_name='kepakaran_suspek') 
    diagnosa_sistem = models.ForeignKey(Diagnosa, on_delete=models.CASCADE, db_constraint=False, null=True, related_name='kepakaran_sistem') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = "knowledge_acquisition"
class Gejala(models.Model):
    id = models.IntegerField
    nama = models.TextField(null=True)
    alias=models.TextField(null=True)
    jenis = models.TextField(null=True)
    pernyataan= models.TextField(null=True)
    penanganan = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.alias

    class Meta:
        db_table = "gejala"