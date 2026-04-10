from django.urls import path
from .views import order  ,RectificativeOrder,get_order
urlpatterns = [
    path('order/',order),
    path('rectificative/', RectificativeOrder),
    path('order/<int:id>', get_order)
    
]