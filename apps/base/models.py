from django.db import models
from django.conf import settings
from django.contrib.auth.models import User,Group
from .expert.models.m_kepakaran import Diagnosa
from .posbindu.models.data_suspek.m_data_suspek import Gender
from django.urls import reverse


class Dashboard (models.Model):
    id = models.IntegerField
    alamat = models.TextField()
    umur = models.CharField(max_length=3,null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE,db_constraint=False,null=True)    
    diagnosa = models.ForeignKey(Diagnosa, on_delete=models.CASCADE,db_constraint=False,null=True) 
    hasil= models.CharField(max_length=10,null=True)
    total= models.CharField(max_length=10,null=True)

    class Meta:
        db_table="dashboard"
class Menu(models.Model):
    id = models.IntegerField
    nama = models.TextField()
    link = models.TextField()
    group= models.CharField(max_length=40,null=True)
    icon = models.CharField(max_length=40)

    class Meta:
        db_table = "menu"
class MenuHome(models.Model):
    id = models.IntegerField
    nama = models.TextField()
    link = models.TextField()
    level = models.CharField(max_length=3,null=True)

    class Meta:
        db_table = "menu_general"

class Notifikasi(models.Model):
    id = models.AutoField(primary_key=True)
    nama= models.CharField(max_length=255,null=True)
    fitur = models.CharField(max_length=50)
    verb = models.CharField(max_length=50)
    user = models.CharField(max_length=50, null=True)
    url=models.CharField(max_length=50, null=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    read_by = models.ManyToManyField(User, related_name='read_notifications', blank=True)
    deleted_by = models.ManyToManyField(User, related_name='delete_notifications', blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "notifikasi"

class WilayahKerja(models.Model):
    id = models.AutoField(primary_key=True)
    wilayah_kerja = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "wilayah_kerja"

    def __str__(self):
        return self.wilayah_kerja
class Satuan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wilayah_kerja = models.ForeignKey(WilayahKerja, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "satuan"

