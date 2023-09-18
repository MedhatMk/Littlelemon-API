from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem, Category 
from django.contrib.auth.models import Group,User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'groups')
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'



class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']
 
class MenuItemSerializer(serializers.ModelSerializer):
    #category = CategorySerializer()
    class Meta:
        model = MenuItem
        fields = ['id','title','price' ,'featured','category']
    
