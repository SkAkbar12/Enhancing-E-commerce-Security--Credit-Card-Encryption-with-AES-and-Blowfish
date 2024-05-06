from django.db import models

# Create your models here.
class registerdetails(models.Model):
    username=models.CharField(max_length=50)
    email=models.CharField(max_length=80)
    password=models.CharField(max_length=50)

class Image(models.Model):
    name=models.CharField(max_length=30)
    desc=models.CharField(max_length=30)
    newimg=models.FileField(upload_to="images/",max_length=250,null=True,default=None)

class Addtocart(models.Model):
    email=models.EmailField()
    productname=models.CharField(max_length=30)
    image=models.FileField(upload_to="cart/",max_length=250,null=True,default=None)

class savecarddetails(models.Model):
    email = models.CharField(max_length=20)
    cardnumber = models.CharField(max_length=70)
    date_cvv = models.CharField(max_length=70)
    key1 = models.CharField(max_length=70)
    key2 = models.CharField(max_length=70)
    pin = models.CharField(max_length=70)
  



   
    
