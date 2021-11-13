from django.shortcuts import get_object_or_404
from deal_in_tb.models import TblCategory, TblItem, TblCart, TblTransaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from deal_in_tb import serializers
from deal_in_tb.decorator import token_required, api_key_required
from deal_in_tb.jwt import JWTAuth
from django.http import QueryDict
from django.db.models import Q

import datetime

# Create your views here.
@api_view(['GET'])
@api_key_required
def Index(request):
    if request.method == 'GET':
        try:
            item = TblItem.objects.filter(deleted=0)
            ser = serializers.ItemsIndexSerializer(item, many=True)
            return Response(data={"all_item" : ser.data}, status=status.HTTP_200_OK)
        except:
            return Response(data={"all_item" : []}, status=status.HTTP_400_BAD_REQUEST)
            


@api_view(['GET'])
@token_required
@api_key_required
def IndexStore(request, id_store):
    if request.method == 'GET':
        try:
            item = TblItem.objects.filter(id_store=id_store, deleted=0)
            if item.exists():
                ser = serializers.ItemsIndexSerializer(item, context={"request": request}, many=True)
                return Response(data=ser.data, status=status.HTTP_200_OK)
            else:
                return Response(data={"item_store": []}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={"item_store": []}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@token_required
@api_key_required
def Category(request, id=0):
    if request.method == 'GET':
        if id == 0:
            try:
                category = TblCategory.objects.filter(deleted=0)
                ser = serializers.CategorySerializer(category, many=True)
                return Response(data={"status" : 200, "message" : "Berhasil Mengambil Data", "data" : ser.data}, status=status.HTTP_200_OK)
            except:
                return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=204)
        else:
            try:
                category = TblCategory.objects.filter(pk=id, deleted=0)
                ser = serializers.CategorySerializer(category, many=True)
                return Response(data={"status" : 200, "message" : "Berhasil Mengambil Data", "data" : ser.data}, status=status.HTTP_200_OK)
            except:
                return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=204)

    if request.method == 'POST':
        try:
            serializer = serializers.CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"status" : 200, "message" : "Berhasil Menambahkan Data", "data" : serializer.data},  status=status.HTTP_201_CREATED)
        except:
            return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        try:
            serializer = serializers.CategorySerializer(get_object_or_404(TblCategory, pk=id), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"status" : 200, "message" : "Berhasil Mengupdate Data", "data" : serializer.data},  status=status.HTTP_201_CREATED)
        except:
            return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if id != 0:
            try:
                delete = TblCategory.objects.get(pk=id).delete()
                if delete:
                    return Response(data={"status" : 200, "message" : "Berhasil Menghapus Data"},  status=status.HTTP_201_CREATED)
                return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(data={"status" : 204, "message" : "Category Tidak dietmukan"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"status" : 204, "message" : "kehapus cok tapi boong"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST','PUT','DELETE'])
@token_required
def Item(request, id=0):
    if request.method == 'GET':
        if id == 0:
            try:
                Item = TblItem.objects.filter(deleted=0)
                ser = serializers.ItemsIndexSerializer(Item, many=True)
                return Response(data={"status" : 200, "message" : "Berhasil Mengambil Data", "data" : ser.data}, status=status.HTTP_200_OK)
            except:
                return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=204)
        else:
            try:
                Item = TblItem.objects.filter(pk=id, deleted=0)
                ser = serializers.ItemsIndexSerializer(Item, many=True)
                return Response(data={"status" : 200, "message" : "Berhasil Mengambil Data", "data" : ser.data}, status=status.HTTP_200_OK)
            except:
                return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=204)

    if request.method == 'POST':
        try:
            serializer = serializers.ItemsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"status" : 200, "message" : "Berhasil Menambahkan Data", "data" : serializer.data},  status=status.HTTP_201_CREATED)
        except:
            return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        try:
            serializer = serializers.ItemsSerializer(get_object_or_404(TblItem, pk=id), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"status" : 200, "message" : "Berhasil Mengupdate Data", "data" : serializer.data},  status=status.HTTP_201_CREATED)
        except:
            return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        if id != 0:
            try:
                delete = TblItem.objects.get(pk=id).delete()
                if delete:
                    return Response(data={"status" : 200, "message" : "Berhasil Menghapus Data"},  status=status.HTTP_201_CREATED)
                return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(data={"status" : 204, "message" : "Item Tidak dietmukan"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"status" : 204, "message" : "Pilih Item yang mau di hapus"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@token_required
@api_key_required
def Cart(request, id=0):
    if request.method == 'GET':
        jwt = JWTAuth()
        if id == 0:
            try:
                data = jwt.decode(request.headers['Authorization'])
                Cart = TblCart.objects.filter(username=data['username'], deleted=0)
                ser = serializers.CartsIndexSerializer(Cart, many=True)
                return Response(data={"status" : 200, "message" : "Berhasil Mengambil Data", "data" : ser.data}, status=status.HTTP_200_OK)
            except:
                return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=204)
        else:
            try:
                Cart = TblCart.objects.filter(pk=id, deleted=0)
                ser = serializers.CartsIndexSerializer(Cart, many=True)
                return Response(data={"status" : 200, "message" : "Berhasil Mengambil Data", "data" : ser.data}, status=status.HTTP_200_OK)
            except:
                return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=204)

    if request.method == 'POST':
        try:
            serializer = serializers.CartsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"status" : 200, "message" : "Berhasil Menambahkan Data", "data" : serializer.data},  status=status.HTTP_201_CREATED)
        except:
            return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def Search(request, search):
    if request.method == 'GET':
        try:
            Item = TblItem.objects.filter(Q(name__icontains = search) | Q(description__icontains = search), deleted=0)
            ser = serializers.ItemsIndexSerializer(Item, many=True)
            return Response(data={"all_item" : ser.data}, status=status.HTTP_200_OK)
        except:
            return Response(data={"all_item" : []}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@token_required
@api_key_required
def Transaction(request):
    if request.method == 'POST':
        jwt = JWTAuth()
        # try:
        data = request.data
        # print(data['id_item'])
        if TblTransaction.objects.filter(id_item=data['id_item'], status=0).exists():
            Trans = TblTransaction.objects.filter(id_item=data['id_item'], status=0)
            trans_ser = serializers.TransactionIndexSerializer(Trans, many=True)
            Item = TblItem.objects.filter(pk=data['id_item'], deleted=0)
            item_ser = serializers.ItemsIndexSerializer(Item, many=True)
            # print(trans_ser.data)
            return Response(data={"status" : 400, "message" : "Item Sebelumnya Belum di bayar", "trans" : trans_ser.data, "item": item_ser.data},  status=status.HTTP_400_BAD_REQUEST)
        else:
            trans_ser = serializers.TransactionSerializer(data=data)
            if trans_ser.is_valid():
                trans_ser.save()
                Item = TblItem.objects.filter(pk=data['id_item'], deleted=0)
                ser = serializers.ItemsIndexSerializer(Item, many=True)
                # print(trans_ser.data)
                # print(ser.data)
                return Response(data={"status" : 200, "message" : "Berhasil Menambahkan Data", "trans" : trans_ser.data, "item": ser.data},  status=status.HTTP_201_CREATED)
        # except:
        #     return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)