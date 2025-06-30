from django.db import models
from django.contrib.auth.models import User

class TipePengumuman(models.Model):
    id= models.IntegerField
    tipe= models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = "tipepengumuman"
    def __str__(self):
        return self.tipe
class Pengumuman(models.Model):
    id= models.IntegerField
    judul= models.CharField(max_length=50)
    tanggal= models.CharField(max_length=50)
    waktu= models.CharField(max_length=50)
    tempat= models.CharField(max_length=50,null=True)
    jenis= models.ForeignKey(TipePengumuman, on_delete=models.CASCADE,db_constraint=False,null=True)
    pengumuman=models.TextField()
    petugas=models.ForeignKey(User, on_delete=models.CASCADE,db_constraint=False,null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = "pengumuman"