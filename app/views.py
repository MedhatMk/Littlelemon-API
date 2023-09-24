from django.contrib.auth.models import Group,User
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from .models import Cart, Category, MenuItem, Order,OrderItem
from rest_framework.decorators import api_view
from .serializers import CartItemSerializer, CategorySerializer, GroupSerializer, OrderItemSerializer, OrderSerializer,UserSerializer, MenuItemSerializer
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

#=======================================================================================
#                                   Cart management endpoints
#                             ===========================================



class CartListCreate(generics.ListCreateAPIView):
      serializer_class = CartItemSerializer
      permission_classes = [IsAuthenticated]
      def get_queryset(self):
            user = self.request.user
            return Cart.objects.filter(user=user)

      def perform_create(self, serializer):
            menuitem = self.request.data.get('menuitem')
            quantity = self.request.data.get('quantity')
            unit_price = MenuItem.objects.get(pk=menuitem).price
            quantity = int(quantity)
            price = quantity * unit_price
            serializer.save(user=self.request.user, price=price)

      def delete(self, request):
            user = self.request.user
            Cart.objects.filter(user=user).delete()
            return Response(status=204)

#=======================================================================================
#                                   Order management endpoints
#                             ===========================================
# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# def orders(request):
#       user = request.user
#       if request.method == 'GET':
#             orders = Order.objects.filter(user = user)
#             serializer = OrderSerializer(orders, many = True)
#             return Response(serializer.data)
#       elif request.method == 'POST':
#             cart_items = Cart.objects.filter(user = user)
#             total =sum(item.price for item in cart_items)
#             orders = Order.objects.create(user = user, total = total)

#             if not cart_items:
#                   return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

#             for item in cart_items:
#                   OrderItem.objects.create(
#                         order = orders,
#                         menuitem = item.menuitem,
#                         quantity = item.quantity,
#                         unit_price = item.unit_price,
#                         price = item.price
#                   )
#             Cart.objects.delete(user = user)
#             return Response({'The order was created successfully.'},status=status.HTTP_201_CREATED)

class OrderView(generics.ListCreateAPIView):
      serializer_class = OrderSerializer
      permission_classes = [IsAuthenticated]

      def get_queryset(self):
            user = self.request.user
            if user.groups.filter(name = 'Manager').exists():
                  return Order.objects.all()
            elif user.groups.filter(name = 'Delivery').exists():
                  return Order.objects.filter(delivery_crew = user)
            return Order.objects.filter(user = user)

      def perform_create(self, serializer):
            user = self.request.user
            cart_items = Cart.objects.filter(user = user)
            total = sum(item.price for item in cart_items)
            order = serializer.save(user = user , total = total)

            for item in cart_items:
                  OrderItem(
                        order = order,
                        menuitem = item.menuitem,
                        quantity = item.quantity,
                        unit_price = item.unit_price,
                        price = item.price
                  )
                  item.delete()

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
      serializer_class = OrderSerializer
      permission_classes = [IsAuthenticated]
      def get_queryset(self):
            user = self.request.user
            if user.groups.filter(name='manager').exists():
                  return Order.objects.all()
            return Order.objects.filter(user=user)