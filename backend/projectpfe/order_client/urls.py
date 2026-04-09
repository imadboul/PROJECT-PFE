from django.urls import path
from .views import order , validateorder ,RectificativeOrder,get_order
urlpatterns = [
<<<<<<< HEAD:backend/projectpfe/order_client/urls.py
    path('create/',views.OrderCreateView.as_view()),
    path('validat/',views.OrderValidateView.as_view()),
    path('rectificative/',views.RectificativeOrderView.as_view()),
    path('<int:type>/', views.OrderListView.as_view()),
    path('invalid',views.inValid)
=======
    path('order/',order),
    path('validateorder/',validateorder),
    path('rectificative/', RectificativeOrder),
    path('order/<int:id>', get_order)
>>>>>>> 194df305d46839cb162395484a3dec9965a2e5f6:backend/projectpfe/Orders_Manage/urls.py
    
]