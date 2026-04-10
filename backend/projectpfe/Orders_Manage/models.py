from django.db import models
from catalog.models import Contract,Client,Product
from order_client.models import Orderclient


class Types(models.TextChoices):
    
       NORMAL='normal','Normal'
       PLUS=  'plus','Plus'
       MINUS= 'minus','Minus' 
       
class States(models.TextChoices):
    
       PENDING='pending','Pending'
       INVOICED = 'invoiced','Invoiced'      

    

class Order(models.Model):
    id=models.AutoField(primary_key=True)
    date_created=models.DateTimeField(auto_now_add=True)
    contract=models.ForeignKey(Contract,related_name='orders',null=False,blank=False,on_delete=models.PROTECT)
    client=models.ForeignKey(Client,related_name='orders',null=False,blank=False,on_delete=models.PROTECT)
    client_order= models.ForeignKey(Orderclient ,related_name='fufilled_orders',null=False,blank=False,on_delete=models.PROTECT)
    parent_order = models.ForeignKey('self',related_name='children',null=True,blank=True,on_delete=models.PROTECT)
    invoice=models.ForeignKey('Invoices.Invoice',related_name='invoice_order_items',null=True,blank=False,on_delete=models.PROTECT)
    type=models.CharField(null=False,blank=False,choices=Types.choices,max_length=20,default=Types.NORMAL)
    state=models.CharField(choices=States.choices,max_length=20,default=States.PENDING)
    stated_by = models.ForeignKey(Client,null=True,on_delete=models.PROTECT)
    
 
class OrderProduct(models.Model):
    
    
    id=models.AutoField(primary_key=True)
    order=models.ForeignKey(Order,related_name='products',null=False,blank=False,on_delete=models.PROTECT)
    product=models.ForeignKey(Product,related_name='products',null=False,blank=False,on_delete=models.PROTECT)
    qte=models.DecimalField(null=False,blank=False,max_digits=12,decimal_places=3)
        



