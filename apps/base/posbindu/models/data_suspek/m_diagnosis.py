from django.db import models
from django.urls import reverse

class MenuDiagnosis(models.Model):
    id = models.IntegerField
    nama=models.TextField(null=True)
    inisial=models.TextField(null=True)
    link=models.TextField()
    class Meta:
        db_table="menu_diagnosis"