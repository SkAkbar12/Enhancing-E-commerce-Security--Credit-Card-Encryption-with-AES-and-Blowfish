from django.contrib import admin
from bankdetails.models import Bankdetails,EncryptData

class Bankadmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'marriage', 'Fname', 'Mname', 'pan', 'Wnet', 'number', 'Dcc', 'city', 'state', 'pin', 'Email', 'desg')


class CardEncryptData(admin.ModelAdmin):
    list_display = ('user', 'cardnumber', 'date_cvv', 'key1','key2', 'pin', 'password')

admin.site.register(EncryptData, CardEncryptData)

admin.site.register(Bankdetails, Bankadmin)

