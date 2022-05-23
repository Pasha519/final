from django.contrib import admin
from testapp.models import Category,Products,Order

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id',"name"]

# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ["first_name","last_name","email","password"]

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id',"name","price","category","description","image"]
    search_fields = ("name",)

class OrderAdmin(admin.ModelAdmin):
    list_display = ["product","customer","quantity","price","address","phone","date","status"]
    ordering = ("-date",)

admin.site.register(Category,CategoryAdmin)
#admin.site.register(Customer, CustomerAdmin)
admin.site.register(Products,ProductsAdmin)
admin.site.register(Order,OrderAdmin)