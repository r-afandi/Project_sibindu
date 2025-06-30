from django.db import models
from django.contrib.auth.models import User

class Validasi (models.Model):
    id= models.IntegerField
    nama= models.CharField(max_length=50,null=True)
    class Meta:
        db_table = "validasi"
    def __str__(self):
        return self.nama
    
class Kondisi(models.Model):
    id= models.IntegerField
    nama= models.CharField(max_length=50,null=True)
    badge= models.CharField(max_length=50,null=True)
    class Meta:
        db_table = "kondisi"
    def __str__(self):
        return self.nama
    
class DataSdp(models.Model):
    id= models.IntegerField
    nama= models.CharField(max_length=50)
    kode= models.CharField(max_length=50,null=True)
    jumlah_masuk= models.CharField(max_length=50,null=True)
    jumlah_keluar=models.CharField(max_length=50,null=True)
    total=models.CharField(max_length=50,null=True)
    satuan=models.CharField(max_length=50,null=True)
    kadaluarsa= models.CharField(max_length=50,null=True)
    kondisi= models.ForeignKey(Kondisi, on_delete=models.CASCADE,db_constraint=False,null=True) 
    produk=models.CharField(max_length=50,null=True)
    info=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = "data_sdp"
    def __str__(self):
        return self.nama
    
class LaporanSdp(models.Model):
    id= models.IntegerField
    kode = models.CharField(max_length=50, null=True)
    nama= models.CharField(max_length=50)
    jenis= models.ForeignKey(DataSdp, on_delete=models.CASCADE,db_constraint=False,null=True)  
    masuk= models.CharField(max_length=50)
    keluar= models.CharField(max_length=50)
    bukti = models.ImageField(null=True, max_length=255) 
    upload = models.CharField(max_length=250,null=True)
    tanggal= models.CharField(max_length=50)
    kadaluarsa= models.CharField(max_length=50,null=True)
    kondisi=models.ForeignKey(Kondisi, on_delete=models.CASCADE,db_constraint=False,null=True,blank=True)  
    keperluan= models.CharField(max_length=250,null=True)
    validasi= models.ForeignKey(Validasi, on_delete=models.CASCADE,db_constraint=False,null=True)
    info=models.CharField(max_length=50)
    petugas = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, null=True, related_name="laporansdp_petugas")
    validator = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, null=True,related_name="laporansdp_validator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = "laporan_sdp"        
    def __str__(self):
        return self.nama