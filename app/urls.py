from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    
    path('api-token-auth/', obtain_auth_token),
    path('menu-items',views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>',views.RetriveUpateDestroyMenu.as_view()),
    path('categories',views.CategoryView.as_view()),
    #path('cart/menu-items', views.CartItemListCreateView, name='cartOperations'),

    path('cart/menu-items', views.CartListCreate.as_view(), name='cartOperations'),
    #groups-Management

    path('groups/', views.GroupListCreate.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', views.GroupRetriveupdateDestroy.as_view(), name='group-retrieve-update-delete'),
    path('groups/manager/users/',views.ManagerUserListCreateView.as_view(), name='manager-users-create'),
    path('groups/manager/users/<int:user_id>',views.ManagerUserDeleteView.as_view(), name='manager-users-Delete'),
    path('groups/delivery-crew/users/',views.DeliveryUserListCreateView.as_view(), name='delivery-users-list'),
    path('groups/delivery-crew/users/<int:user_id>',views.DeliveryUserDeleteView.as_view(), name='delivery-users-Delete'),

    #orders
    #path('orders/', views.orders, name='order-list-create'),
    path('orders/', views.OrderView.as_view(), name='order-list-create'),
    path('orders/<int:pk>', views.SingleOrderView.as_view(), name='order-edit'),


]

