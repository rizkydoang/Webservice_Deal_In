from django.shortcuts import get_object_or_404
from deal_in_tb.models import TblCategory, TblItem, TblCart, TblTransaction, TblUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from deal_in_tb import serializers
from deal_in_tb.decorator import token_required, api_key_required
from deal_in_tb.jwt import JWTAuth
from django.db.models import Q
from deal_in_tb.midtrans import api_client, snap
import requests


def TransactionToken(request, order_id, gross_amount):
    transaction_token = snap.create_transaction_token({
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": gross_amount
        }
    })

    return transaction_token


# Create your views here.
@api_view(['GET'])
def Index(request):
    if request.method == 'GET':
        try:
            item = TblItem.objects.filter(deleted=0)
            ser = serializers.ItemsIndexSerializer(item, context={"request": request}, many=True)
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
                return Response(data={"item_store" : ser.data}, status=status.HTTP_200_OK)
            else:
                return Response(data={"item_store" : []}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={"item_store" : []}, status=status.HTTP_400_BAD_REQUEST)


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
def Item(request, id=0):
    if request.method == 'GET':
        if id == 0:
            try:
                Item = TblItem.objects.filter(deleted=0)
                ser = serializers.ItemsIndexSerializer(Item, context={"request": request}, many=True)
                return Response(data={"status" : 200, "message" : "Berhasil Mengambil Data", "data" : ser.data}, status=status.HTTP_200_OK)
            except:
                return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=204)
        else:
            # try:
            Item = TblItem.objects.filter(pk=id, deleted=0)
            ser = serializers.ItemsIndexSerializer(Item, context={"request": request}, many=True)
            return Response(data={"status" : 200, "message" : "Berhasil Mengambil Data", "data" : ser.data}, status=status.HTTP_200_OK)
            # except:
            #     return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=204)

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


@api_view(['GET', 'POST', 'DELETE'])
@token_required
def Cart(request, id=0):
    if request.method == 'GET':
        jwt = JWTAuth()
        try:
            data = jwt.decode(request.headers['Authorization'])
            Cart = TblCart.objects.filter(username=data['username'], deleted=0)
            ser = serializers.CartsIndexSerializer(Cart, context={"request": request}, many=True)
            return Response(data={"status" : 200, "message" : "Berhasil Mengambil Data", "data" : ser.data}, status=status.HTTP_200_OK)
        except:
            return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        try:
            if not TblCart.objects.filter(id_item=request.data['id_item'], username=request.data['username'], deleted=0).exists():
                serializer = serializers.CartsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data={"status" : 200, "message" : "Berhasil menambahkan data", "data" : serializer.data},  status=status.HTTP_201_CREATED)
            else:
                return Response(data={"status" : 400, "message" : "Item sudah ditambahkan sebelumnya"},  status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={"status" : 400, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if id != 0:
            jwt = JWTAuth()
            try:
                data = jwt.decode(request.headers['Authorization'])
                delete = TblCart.objects.get(pk=id, username=data['username']).delete()
                if delete:
                    return Response(data={"status" : 200, "message" : "Berhasil menghapus data"},  status=status.HTTP_201_CREATED)
                return Response(data={"status" : 204, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(data={"status" : 204, "message" : "Cart Tidak dietmukan"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"status" : 204, "message" : "Pilih Cart yang mau di hapus"}, status=status.HTTP_400_BAD_REQUEST)


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
def Transaction(request):
    if request.method == 'POST':
        jwt = JWTAuth()
        try:
            data_header = jwt.decode(request.headers['Authorization'])
            # if TblTransaction.objects.filter(username=data_header['username'], deleted=0).exists():
            #     data_trans = TblTransaction.objects.filter(username=data_header['username'], deleted=0)
            #     ser = serializers.TransactionSerializer(data_trans, many=True)
            #     return Response(data={"status" : 204, "data": ser.data, "message" : "Transaksi Sebelumnya Belum di bayar"},  status=status.HTTP_400_BAD_REQUEST)

            data = request.data
            detail_qty = []
            detail_total = []
            total = 0
            for idx, i in enumerate(data.getlist('id_item')):
                data_item = TblItem.objects.filter(pk=i, deleted=0).first()

                if int(data_item.quantity) < int(data.getlist('qty')[idx]):
                    return Response(data={"status" : 400, "message" : "Quantity melebihi yang tersedia"}, status=status.HTTP_400_BAD_REQUEST)

                detail_qty.append(int(data.getlist('qty')[idx]))
                detail_total.append(int(data_item.price) * int(data.getlist('qty')[idx]))
                total += int(data_item.price) * int(data.getlist('qty')[idx])

            trans = TblTransaction.objects.create(total=total, username=TblUser.objects.get(pk=data_header['username']))
            token = TransactionToken(request, trans.id, trans.total)
            TblTransaction.objects.filter(id=trans.id).update(token=token)
            for idx, i in enumerate(data.getlist('id_cart')):
                TblCart.objects.filter(id=i).update(id_transaction=trans.id, qty=detail_qty[idx], total=detail_total[idx], deleted=1)

            data_cart = TblCart.objects.filter(id_transaction=trans.id)
            ser = serializers.CartsIndexSerializer(data_cart, context={"request": request}, many=True)
            data_response = {
                "id_transaction": trans.id,
                "token": token,
            }
            return Response(data={"status" : 200, "message" : "Berhasil membuat transaksi", "data": data_response, "cart": ser.data},  status=status.HTTP_201_CREATED)
        except:
            return Response(data={"status" : 400, "message" : "Terjadi Kesalahan"},  status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        jwt = JWTAuth()
        try:
            data_header = jwt.decode(request.headers['Authorization'])
            trans = TblTransaction.objects.filter(username=data_header['username'])
            ser = serializers.TransactionSerializer(trans, many=True)
            return Response(data={"status" : 200, "message" : "Berhasil mengambil data", "data" : ser.data}, status=status.HTTP_200_OK)
        except:
            return Response(data={"status" : 400, "message" : "Terjadi Error"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@token_required
def Pay(request):
    if request.method == 'POST':
        jwt = JWTAuth()
        try:
            data_header = jwt.decode(request.headers['Authorization'])

            header = {
                'Authorization': 'Basic U0ItTWlkLXNlcnZlci02OUpaSDlCNS1XS0hpczNXdkxzd3Nmdnk6'
            }
            response = requests.get('https://api.sandbox.midtrans.com/v2/'+ request.data['id_transaction']+ '/status', headers=header).json()

            print(response)

            if response['status_code'] != '404':
                TblTransaction.objects.filter(id=request.data['id_transaction']).update(deleted=1)

            data_cart = TblCart.objects.filter(id_transaction=request.data['id_transaction'], username=data_header['username'])
            ser = serializers.CartsIndexSerializer(data_cart, context={"request": request}, many=True)
            data_response = {
                "token": TblTransaction.objects.get(pk=request.data['id_transaction']).token,
                "detail": response
            }
            return Response(data={"status" : 200, "message" : "Berhasil membuat transaksi", "data": data_response, "cart": ser.data},  status=status.HTTP_200_OK)
        except:
            return Response(data={"status" : 400, "message" : "Terjadi Kesalahan"},  status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@token_required
def Cancel(request):
    if request.method == 'POST':
        jwt = JWTAuth() 
        # try:
        data_header = jwt.decode(request.headers['Authorization'])

        header = {
            'Authorization': 'Basic U0ItTWlkLXNlcnZlci02OUpaSDlCNS1XS0hpczNXdkxzd3Nmdnk6'
        }
        response = requests.post('https://api.sandbox.midtrans.com/v2/'+ request.data['id_transaction']+ '/cancel', headers=header).json()

        print(response)

        data_response = {
            "response": response
        }
        return Response(data={"status" : 200, "message" : "Berhasil cancel transaksi", "data": data_response},  status=status.HTTP_200_OK)
        # except:
        #     return Response(data={"status" : 400, "message" : "Terjadi Kesalahan"},  status=status.HTTP_400_BAD_REQUEST)
