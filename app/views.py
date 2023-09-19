from django.contrib.auth.models import Group,User
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from .models import Category, MenuItem
from rest_framework.decorators import api_view
from .serializers import CategorySerializer, GroupSerializer,UserSerializer, MenuItemSerializer
from rest_framework import generics,permissions,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Create your views here.

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class CategoryView(generics.ListAPIView):
      queryset = Category.objects.all()
      serializer_class = CategorySerializer

#====================================================================
#                  MenuItems Management
#              ===============================
class MenuItemsView(generics.ListCreateAPIView):
      queryset = MenuItem.objects.all()
      serializer_class = MenuItemSerializer
           
      def get_permissions(self):
           if self.request.method == 'GET':
                 return [IsAuthenticated()]
           elif self.request.method == 'POST':
                 return [IsAuthenticated(),IsManager()]
      
      
class RetriveUpateDestroyMenu(generics.RetrieveUpdateDestroyAPIView):
     
      serializer_class = MenuItemSerializer
      permission_classes= [IsAuthenticated,IsManager]
      def get_object(self):
            pk = self.kwargs.get('pk')
            return get_object_or_404(MenuItem,pk=pk)
           
#groups management
class GroupListCreate(generics.ListCreateAPIView):
      queryset = Group.objects.all()
      serializer_class = GroupSerializer
      permission_classes = [IsAuthenticated,IsManager]
      
class GroupRetriveupdateDestroy(generics.RetrieveUpdateDestroyAPIView):
      queryset = Group.objects.all()
      serializer_class = GroupSerializer
      permission_classes = [IsAuthenticated,IsManager]
 #================================================================================
 
      
#                 Manager group management
#              ===============================


class ManagerUserListCreateView(generics.ListCreateAPIView):
      model = User
      
      def get_queryset(self):
            return User.objects.filter(groups__name = 'Manager')
      def post(self, request, *args, **kwargs):
            queryset =User.objects.all()
            return self.create(request,*args, **kwargs)

      serializer_class = UserSerializer
      permission_classes = [IsAuthenticated,IsManager]
      
      def perform_create(self, serializer):
            manager_group, created = Group.objects.get_or_create(name= "Manager")
            user = serializer.save()
            user.groups.add(manager_group)

class ManagerUserDeleteView(generics.DestroyAPIView):
      queryset = User.objects.all()
      
      def destroy(self, request, *args, **kwargs):
            user = self.get_object()
            manager_group = Group.objects.get(name='Manager')
            
            if manager_group in user.groups.all():
                  user.groups.remove(manager_group)
                  return Response(status=status.HTTP_200_OK)
            else:
                  return Response(status=status.HTTP_404_NOT_FOUND)


#=================================================================================
#                  Delivery group management
#              ===============================


class DeliveryUserListCreateView(generics.ListCreateAPIView):
      
      model = User
      def get_queryset(self):
            return User.objects.filter(groups__name = 'Delivery')
      def post(self, request, *args, **kwargs):
            queryset =User.objects.all()
            return self.create(request,*args, **kwargs)
      
      serializer_class = UserSerializer
      permission_classes = [IsAuthenticated, IsManager]
      
      def perform_create(self, serializer):
            delivery_group , created = Group.objects.get_or_create(name = "Delivery")
            user = serializer.save()
            user.groups.add(delivery_group)
            
class DeliveryUserDeleteView(generics.DestroyAPIView):
      queryset = User.objects.all()
      
      def destroy(self, request, *args, **kwargs):
            user = self.get_object()
            delivery_group = Group.objects.get(name = 'Delivery')
            if delivery_group in user.groups.all():
                  user.groups.remove(delivery_group)
                  return Response( status= status.HTTP_200_OK)
            else:
                  return Response( status= status.HTTP_404_NOT_FOUND)