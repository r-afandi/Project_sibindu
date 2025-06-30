from django.db import models
from django.urls import reverse

class About(models.Model):
    id = models.IntegerField
    nama = models.CharField(max_length=50)
    alamat = models.TextField(null=True)
    maps = models.TextField()
    tentang = models.TextField()
    tentang_footer= models.TextField()
    email = models.CharField(max_length=50,null=True)
    telp = models.CharField(max_length=14,null=True)
    sosmed=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table="about"