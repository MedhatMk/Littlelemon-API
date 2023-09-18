from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    
    path('api-token-auth/', obtain_auth_token),
    path('menu-items',views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>',views.RetriveUpateDestroyMenu.as_view()),
    path('categories',views.CategoryView.as_view()),
    path('groups/', views.GroupListCreate.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', views.GroupRetriveupdateDestroy.as_view(), name='group-retrieve-update-delete'),
    path('groups/manager/users/',views.ManagerUserListView.as_view(), name='manager-users-list'),
    path('groups/manager/users/add/',views.ManagerUserCreateView.as_view(), name='manager-users-create'),
    path('groups/manager/users/<int:user_id>',views.ManagerUserDeleteView.as_view(), name='manager-users-Delete'),

]

