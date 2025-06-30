from itertools import count
from re import L
from django.db import models
from django.urls import reverse
from ....expert.models.m_kepakaran import Diagnosa
from ...models.informasi.m_pengumuman import Pengumuman
from django.contrib.auth.models import User
#from ....models import  WilayahKerja
class Gender(models.Model):
    id = models.IntegerField
    nama= models.CharField(max_length=10,null=True)
    alias= models.CharField(max_length=2,null=True)
    class Meta:
        db_table="gender"
    def __str__(self):
        return self.nama

class DataSuspek(models.Model):
    id = models.IntegerField
    #tanggal= models.ForeignKey(Pengumuman, on_delete=models.CASCADE,db_constraint=False,null=True)
    tanggal= models.CharField(max_length=50)
    #pos = models.ForeignKey(WilayahKerja, on_delete=models.SET_NULL, null=True)
    nik = models.CharField(max_length=16,null=True)
    nama = models.TextField()
    umur = models.CharField(max_length=3,null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE,db_constraint=False,null=True)  
    alamat = models.TextField()
    diagnosa = models.ForeignKey(Diagnosa, on_delete=models.CASCADE,db_constraint=False,null=True) 
    data_gejala= models.TextField(null=True)
    data_khusus = models.TextField(null=True) 
    data_luar = models.TextField(null=True)
    data_dalam = models.TextField(null=True)
    penanganan = models.TextField(null=True)
    petugas = models.ForeignKey(User, on_delete=models.CASCADE,db_constraint=False,null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table="data_suspek"
    def __str__(self):
        return self.nik
    