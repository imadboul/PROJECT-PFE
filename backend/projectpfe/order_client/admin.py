from django.contrib import admin
from .models import *


<<<<<<< HEAD:backend/projectpfe/order_client/admin.py
@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display=['id','order','product','qte','unit']
=======
admin.site.register(Order)
admin.site.register(OrderProduct)

>>>>>>> 194df305d46839cb162395484a3dec9965a2e5f6:backend/projectpfe/Orders_Manage/admin.py
