from django.contrib import admin
from shoppingapp.models import registerdetails,Image,Addtocart,savecarddetails

class registration(admin.ModelAdmin):
    list_display=('username','email','password')

class productimage(admin.ModelAdmin):
    list_display=('name','desc','newimg')

class addtocard(admin.ModelAdmin):
    list_display=('email','productname','image')
class savedcarddata(admin.ModelAdmin):
    list_display=('email','cardnumber','date_cvv','key1','key2','pin')

admin.site.register(registerdetails,registration)
admin.site.register(Image,productimage)
admin.site.register(Addtocart,addtocard)
admin.site.register(savecarddetails,savedcarddata)
