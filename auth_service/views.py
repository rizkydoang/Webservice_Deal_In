from deal_in_tb.models import TblDocuments, TblRole, TblStore, TblUser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from deal_in_tb import serializers
from deal_in_tb.decorator import token_required, api_key_required
from rest_framework.response import Response
from rest_framework import status
from deal_in_tb.jwt import JWTAuth

import datetime


@api_view(['POST'])
def Login(request):
    if request.method == 'POST':
        data = request.data
        user = TblUser.objects.filter(username=data['username']).values().first()
        if not user:
            return Response(data={"data": [], "message": "User tidak ditemukan !"}, status=status.HTTP_400_BAD_REQUEST)

        if data['password'] != user['password']:
            return Response(data={"data": [], "message": "Username atau password anda salah !"}, status=status.HTTP_400_BAD_REQUEST)

        jwt = JWTAuth()
        return Response(data={"data": user, "token": jwt.encode({"username": user['username'], "expired": str(datetime.datetime.now() + datetime.timedelta(days=1))}), "message": "Berhasil Login"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def SignUp(request):
    if request.method == 'POST':
        serializer = serializers.UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"status" : 201, "message" : "Berhasil Menambahkan User", "data" : serializer.data},  status=status.HTTP_201_CREATED)

        return Response(data={"status" : 204, "message" : "Username Sudah di gunakan", "data": []}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@api_key_required
def SignUpStore(request, username):
    data = request.data
    if request.method == 'POST':
        docserializer = serializers.DocumentsSerializer(data=data)
        if docserializer.is_valid():
            if not TblDocuments.objects.filter(pk=data['nik']).exists():
                docser = docserializer.save()
                if docser:
                    storeserializer = serializers.StoresSerializer(data=data)
                    if storeserializer.is_valid():
                        storeserializer.save()
                        return Response(data={"status" : 201, "message" : "Berhasil Membuka Toko", "data" : storeserializer.data},  status=status.HTTP_201_CREATED)
                    else:
                        return Response(data={"status" : 400, "message" : "Terjadi Error", "data": []}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data={"status" : 400, "message" : "Terjadi Error", "data": []}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={"status" : 400, "message" : "ID Toko yang anda masukan sudah terdaftar", "data": []}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"status" : 400, "message" : "ID Toko sudah digunakan", "data": []}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        try:
            store = TblStore.objects.filter(username=username).values().first()
            if not store:
                return Response(data={"status" : 400, "message" : "Anda perlu Daftar terlebih dahulu!", "data": []}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"status" : 400, "message" : "Anda perlu Daftar terlebih dahulu!", "data": ["available"]}, status=status.HTTP_200_OK)
        except:
            return Response(data={"status" : 400, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@token_required
def SignUpStoreAuth(request):
    if request.method == 'POST':
        data = request.data
        store = TblStore.objects.filter(username=data['username']).values().first()
        if not store:
            return Response(data={"status" : 400, "message" : "Anda perlu Daftar terlebih dahulu!", "data": []}, status=status.HTTP_400_BAD_REQUEST)
        if store['pin'] == data['pin']:
            jwt = JWTAuth()
            store = TblStore.objects.filter(username=data['username']).values().first()
            return Response(data={"data": store, "token": jwt.encode({"pin": store['pin']}), "message": "Berhasil"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"data": [], "status" : 400, "message" : "PIN anda salah!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET', 'POST', 'PUT', 'DELETE'))
@token_required
@api_key_required
def Role(request, id=0):
    if request.method == 'GET':
        if id == 0:
            try:
                role = TblRole.objects.filter(deleted=0)
                ser = serializers.RolesSerializer(role, many=True)
                return Response(data={"status" : 200, "message" : "Berhasil Mengambil Data", "data" : ser.data}, status=status.HTTP_200_OK)
            except:
                return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=204)
        else:
            try:
                role = TblRole.objects.filter(pk=id, deleted=0)
                ser = serializers.RolesSerializer(role, many=True)
                return Response(data={"status" : 200, "message" : "Berhasil Mengambil Data", "data" : ser.data}, status=status.HTTP_200_OK)
            except:
                return Response(data={"status" : 400, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = serializers.RolesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"status" : 201, "message" : "Berhasil Menambahkan Data", "data" : serializer.data},  status=status.HTTP_201_CREATED)

        return Response(data={"status" : 400, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        serializer = serializers.RolesSerializer(get_object_or_404(TblRole, pk=id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"status" : 201, "message" : "Berhasil Mengupdate Data", "data" : serializer.data},  status=status.HTTP_201_CREATED)

        return Response(data={"status" : 400, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if id != 0:
            try:
                delete = TblRole.objects.get(pk=id).delete()
                if delete:
                    return Response(data={"status" : 201, "message" : "Berhasil Menghapus Data"},  status=status.HTTP_201_CREATED)
                return Response(data={"status" : 400, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(data={"status" : 400, "message" : "Category Tidak dietmukan"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"status" : 400, "message" : "Pilih Category yang mau di hapus"}, status=status.HTTP_400_BAD_REQUEST)