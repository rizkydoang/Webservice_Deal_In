from django.db.models import fields
from rest_framework import serializers
from deal_in_tb.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TblCategory
        fields = ('id', 'name', 'deleted')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblUser
        fields = ('username', 'password', 'name', 'address', 'birth_date', 'photo_profile')


class StoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblStore
        fields = ('id', 'store', 'pin', 'status', 'deleted', 'nik', 'username')


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblDocuments
        fields = ('nik', 'photo_store', 'deleted')


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblItem
        fields = ('name','quantity', 'id_category', 'id_store', 'description', 'photo_item', 'price')


class ItemsIndexSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    id_store = StoresSerializer()
    id_category = CategorySerializer()
    class Meta:
        model = TblItem
        fields = ('id', 'name', 'quantity', 'id_category', 'id_store', 'description', 'image_url', 'price')
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.photo_item.url
        return request.build_absolute_uri(image_url)


class CartsIndexSerializer(serializers.ModelSerializer):
    id_item = ItemsIndexSerializer()
    class Meta:
        model = TblCart
        fields = ('id','id_item', 'username', 'total', 'qty')


class CartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblCart
        fields = ('id','id_item', 'username')


# class DataTransSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TblDataTrans
#         fields = ('id','id_item', 'id_trans', 'qty')


# class TransactionIndexSerializer(serializers.ModelSerializer):
#     id_item = ItemsSerializer()
#     class Meta:
#         model = TblTransaction
#         fields = ('id', 'username', 'id_item', 'total', 'description')


# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TblTransaction
#         fields = ('id', 'username', 'total', 'get_status_display', 'date')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblTransaction
        fields = ('id', 'username', 'total', 'date')


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblRole
        fields = ('id', 'role', 'deleted')
