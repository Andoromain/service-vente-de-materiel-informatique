from django.db import models
from enum import auto
from ProjetVrai.settings import BASE_DIR
import os

class client(models.Model):

    def __str__(self):
        return self.numClient+"\t"+self.nomClient
    numClient=models.CharField(max_length=4);
    nomClient=models.CharField(max_length=50);
    password=models.CharField(max_length=12);
class materiel(models.Model):
    def __str__(self):
        return self.numMat+"\t"+self.design
    numMat=models.CharField(max_length=4);
    design=models.CharField(max_length=20);
    Pu=models.IntegerField();
    Stock=models.IntegerField();
    image=models.ImageField()
class achat(models.Model):
    def __str__(self):
        return self.numMat+"\t"+self.numClient+"\t"+"\t";
    numClient=models.CharField(max_length=4);
    numMat=models.CharField(max_length=4);
    qte=models.IntegerField();
    date_achat=models.DateField(auto_now_add=True)
    
     
    
    