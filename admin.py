from django.contrib import admin
from coverapp.models import Cover,Cart
# Register your models here.
class CoverAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','description','price','image']
    list_filter = ['id']
admin.site.register(Cover,CoverAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display= ['id','cid','uid','quantity']
    list_filter=['id']

admin.site.register(Cart,CartAdmin)


