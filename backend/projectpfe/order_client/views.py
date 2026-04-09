from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from user.models import Client
from .models import Order,States,OrderProduct
<<<<<<< HEAD:backend/projectpfe/order_client/views.py
from .serializers import OrderSerializer,ValidateOrdersSerializer,RectificativeOrderSerializer,OrderProductFilterSerializerOne,OrderFilterSerializerOne,OrderFilterSerializerTow,ClientFilterSerializerOne
=======
from .serializers import *
>>>>>>> 194df305d46839cb162395484a3dec9965a2e5f6:backend/projectpfe/Orders_Manage/views.py
from rest_framework import generics
from django.db import transaction
from .filters import FilterOrderProduct,FilterOrder,FilterOrderAll
<<<<<<< HEAD:backend/projectpfe/order_client/views.py
from Tax_Service.taxCalcul import mains_balances
import logging
=======
from django.utils.decorators import method_decorator
from user.wraps import *
from user.views import notify_all_admin , notify_a_client
>>>>>>> 194df305d46839cb162395484a3dec9965a2e5f6:backend/projectpfe/Orders_Manage/views.py

logging=logging.getLogger(__name__)



@api_view(['POST','GET'])
@jwt_must
def order(request):
    if request.method == 'POST':
        try:
            serializer = OrderSerializer(data=request.data, context = {'user_id': request.user_id})
            if serializer.is_valid():
                order = serializer.save(client_id=request.user_id)  # type: ignore
                notify_all_admin('VALIDATE AN ORDER',f'validate order {order.id}','') # type: ignore
                return Response({'data': 'Order created successfully wait for validation'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errorssss': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    if request.method == 'GET':
        if request.role == 'client':
            orders = OrderreadSerializer(Order.objects.filter(client_id = request.user_id), many= True)
            return Response({"orders": orders.data}, status=status.HTTP_200_OK)
        else:
            orders = OrderreadSerializer(Order.objects.all(), many= True)
            return Response({"orders": orders.data}, status=status.HTTP_200_OK)
    
    

<<<<<<< HEAD:backend/projectpfe/order_client/views.py
class OrderValidateView(generics.UpdateAPIView):
    
    def update(self, request, *args, **kwargs):
        
        try:
            with transaction.atomic():
                 logging.info("Starting order validation process")
                 serializer=ValidateOrdersSerializer(data=request.data)
                 serializer.is_valid(raise_exception=True)
                 ids=serializer.validated_data['ids']
                 
                 nbOrdes=Order.objects.filter(id__in=ids, states=States.PENDING).update(states=States.VALID)
                 
                 
                 if nbOrdes!=0:
                    mains_balances(Order.objects.filter(id__in=ids) )
                    logging.info("Updated client balances for validated orders ended successfully") 
                 
                 return Response({"message": "Orders validated successfully" , "Number of Orders valid":nbOrdes}, status=status.HTTP_200_OK)
        except Exception as e :
            return  Response({"message": "Failed to validate orders","error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
=======
        

        
        
        
@api_view(['POST'])     
@jwt_must
def validateorder(request):
    try:
        with transaction.atomic():
            serializer=ValidateOrdersSerializer(data=request.data)
            if serializer.is_valid():
                order = Order.objects.get(id= serializer.validated_data['id'] ) # type: ignore
                
                order.state = serializer.validated_data['state'] # type: ignore
                order.validated_by_id = request.user_id # type: ignore
                order.save()
                return Response({"message": "Order validated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e :
        return  Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) # type: ignore
>>>>>>> 194df305d46839cb162395484a3dec9965a2e5f6:backend/projectpfe/Orders_Manage/views.py
 
    
    

<<<<<<< HEAD:backend/projectpfe/order_client/views.py
class OrderListView(generics.ListAPIView):
   
   def get(self,request,*args,**kwargs):
       try:
           type=kwargs['type']
           if type==1:
              self.queryset=OrderProduct.objects.select_related('order','product').all().distinct()
              self.serializer_class=OrderProductFilterSerializerOne
              self.filterset_class=FilterOrderProduct
           elif type == 2:
                     filtered = FilterOrder(
                         request.GET,
                         queryset=Order.objects.select_related('client', 'contract__product_type')
                     ).qs
                 
                     seen = set()
                     result = []
                 
                     for order in filtered:
                         key = (order.client.id, order.contract.id)
                 
                         if key not in seen:
                             seen.add(key)
                             result.append(order)
                 
                     serializer = OrderFilterSerializerTow(result, many=True)
                     return Response(serializer.data)
              
           elif type==3:
               self.queryset=Order.objects.select_related('client','contract__product_type').prefetch_related('order_orderProduct_items__product').all().distinct()
               self.serializer_class=OrderFilterSerializerOne
               self.filterset_class=FilterOrder   
           elif type==4:
               self.queryset=Client.objects.prefetch_related('client_contracts__contract_order_items','client_contracts__product_type').all().distinct()
               self.serializer_class=ClientFilterSerializerOne
               self.filterset_class=FilterOrderAll

           return self.list(request,*args,**kwargs)  
       except Exception as e:
             return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST) 
         
@api_view(['PUT'])     
def inValid(request):
    Order.objects.update(states=States.PENDING)
    return Response({'data':'bien'})
            
=======
        
@api_view(['POST'])
@jwt_must
def RectificativeOrder(request):
    
    
    try:
        with transaction.atomic():
            serializer = RectificativeOrderSerializer(data = request.data, context = {'user_id': request.user_id})
                         
    
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Order created successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e :
        return  Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) # type: ignore
        
     
@api_view(['GET'])
@jwt_must
def get_order(request,id):
    try:
        if request.role == 'client':
            order = OrderreadSerializer(Order.objects.get(id=id,client_id= request.user_id))
            return Response({"orders": order.data}, status=status.HTTP_200_OK)
        else:
            order = OrderreadSerializer(Order.objects.get(id=id))
            return Response({"orders": order.data}, status=status.HTTP_200_OK)
            
    except Order.DoesNotExist:
        return Response({'error': 'does not exist or you do not have permission' }, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
    
    

    

    
   
    
    
    
>>>>>>> 194df305d46839cb162395484a3dec9965a2e5f6:backend/projectpfe/Orders_Manage/views.py
