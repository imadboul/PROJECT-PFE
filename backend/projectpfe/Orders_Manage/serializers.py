from rest_framework import serializers
from rest_framework.response import Response
from .models import Order,OrderProduct
from catalog.models import Client,Contract,ProductType,Product
from django.db import transaction
from django.shortcuts import get_object_or_404
from finance.views import check_if_enough
from order_client.models import OrderProductclient
from django.db import models


#serializer for client contract order productType filter
class ProductTypeFilterSerializerOne(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['name']

class OrderFilterSerializerOne(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'type', 'states', 'date_created','parent_order']
           
class ContractFilterSerializerOne(serializers.ModelSerializer):
    contract_order_items = OrderFilterSerializerOne(many=True)
    product_type = ProductTypeFilterSerializerOne(read_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'product_type', 'contract_order_items']

class ClientFilterSerializerOne(serializers.ModelSerializer):
    client_contracts = ContractFilterSerializerOne(many=True)

    class Meta:
        model = Client
        fields = ['id', 'firstName', 'lastName','phoneNumber','client_contracts']
        
   




#serializer for orderProduct with product name filter
class ProductFilterSerializerOne(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['name']

class OrderProductFilterSerializerOne(serializers.ModelSerializer):
    product=ProductFilterSerializerOne(many=False)
    class Meta:
        model=OrderProduct
        fields=["id","qte","unit","order","product" ]
   
 
 
#serializer for orders filter
class ClientFilterSerializerTow(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields=['id','firstName','lastName','phoneNumber']
        
class ContractFilterSerializerTow(serializers.ModelSerializer):
    product_type = ProductTypeFilterSerializerOne(read_only=True)
    class Meta:
        model=Contract
        fields=['id','product_type']
        
        
class OrderFilterSerializerTow(serializers.ModelSerializer):
       client=ClientFilterSerializerTow(many=False)
       contract=ContractFilterSerializerTow(many=False)
       class Meta:
           model=Order
           fields=['client','contract']


#----------------------------------------------------------------------------------------------------
class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderProduct
        fields=['product','qte']
        
class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True,allow_empty=False)

    class Meta:
        model = Order
        fields = ['contract', 'products', 'client_order', 'client']

    def validate(self, data):
        client_order = data.get('client_order')

        if not client_order:
            raise serializers.ValidationError("client_order is required")

        for item in data.get('products', []):
            product_id = item['product'].id if hasattr(item['product'], 'id') else item['product']

            exists = OrderProductclient.objects.filter(
                order=client_order,
                product_id=product_id
            ).exists()

            if not exists:
                raise serializers.ValidationError(
                    f"Client does not have product {product_id} in his order"
                )

        return data

    def create(self, validated_data):
        with transaction.atomic():
            order_items = validated_data.pop('products')

            order = Order.objects.create(**validated_data)

            for item in order_items:
                OrderProduct.objects.create(
                    product=item['product'],
                    qte=item['qte'],
                    order=order,
                )

                OrderProductclient.objects.filter(
                    order=order.client_order,
                    product=item['product']
                ).update(
                    qte_taken=models.F('qte_taken') + item['qte']
                )

        return order
    

class RectificativeOrderSerializer(serializers.ModelSerializer):
        products=OrderProductSerializer(many=True)
        parent_order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=True)
        type = serializers.CharField( required=True)
        
        
        class Meta:
            model=Order
            fields=['parent_order','type','products']
            
        def validate(self,data):
            request_user_id = self.context.get('user_id') 
            contract = data.get('parent_order')
            try:
                order = data.get('parent_order')
                
            
            except Order.DoesNotExist:
                raise serializers.ValidationError("parent order does not exist ")
            
            return data
                
        
            
        def create(self,validated_data):
            with transaction.atomic():  
                parent_order =  validated_data['parent_order'] 
                order_products=validated_data['products']
                request_user_id = self.context.get('user_id')
                
                newOrder=Order.objects.create(
                    contract=parent_order.contract,
                    client=parent_order.client,
                    parent_order=parent_order,
                    type=validated_data['type'],
                )
                
                for order_product in order_products :
                    orderProduct=OrderProduct(
                       product=order_product['product'],
                       qte=order_product['qte'],
                       order= newOrder
                    )
                    orderProduct.save()
                    
                    order_product_client = OrderProductclient.objects.get(order = newOrder.client_order , product = order_product['product']) # type: ignore
                    order_product_client.qte_taken += order_product['qte'], # type: ignore
                return newOrder   
   
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OrderreadSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source ="client.lastName")
    products=OrderProductSerializer(many=True)

    class Meta:
        model=Order
        fields='__all__'

            
#=============================================================================================================     
class ValidateOrdersSerializer(serializers.Serializer):
    id=serializers.IntegerField()  
    state = serializers.CharField()
    
    def validate_state(self, value):
          
          
          STATES = ["pending","validated","rejected"]
          if not value in STATES:
              raise serializers.ValidationError("state does not exist ")
          return value

    def validate(self, data):
        try:
            order = Order.objects.get(id = data.get('id'))
        except Order.DoesNotExist:
             raise serializers.ValidationError("order does not exist ")
        
        return data
    