from django.db import models

# Create your models here.
class Bankdetails(models.Model):
    name=models.CharField(max_length=20)
    gender=models.CharField(max_length=20)
    marriage=models.CharField(max_length=20)
    Fname=models.CharField(max_length=80)
    Mname=models.CharField(max_length=80)
    pan=models.CharField(max_length=20)
    Wnet=models.CharField(max_length=20)
    number=models.CharField(max_length=80)
    Dcc=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    pin=models.CharField(max_length=80)
    Email=models.CharField(max_length=80)
    desg=models.CharField(max_length=20)
    

    def __str__(self):
        return self.name
    
class EncryptData(models.Model):
    user = models.CharField(max_length=20)
    cardnumber = models.CharField(max_length=70)
    date_cvv = models.CharField(max_length=70)
    key1 = models.CharField(max_length=70)
    key2 = models.CharField(max_length=70)
    pin = models.CharField(max_length=70)
    password = models.CharField(max_length=70)

    def __str__(self):
        return self.user

    