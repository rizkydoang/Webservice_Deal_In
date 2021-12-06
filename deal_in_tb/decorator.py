from deal_in_tb.jwt import JWTAuth
from rest_framework.response import Response
from deal_in_tb.models import TblStore, TblUser
from rest_framework import status

import datetime


def token_required(func):
    def inner(request, *args, **kwargs):
        # try:
        jwt = JWTAuth()
        if 'Authorization' in request.headers:
            data = jwt.decode(request.headers['Authorization'])
            TblUser.objects.filter(username=data['username']).values().first()
            if datetime.datetime.now() < datetime.datetime.fromisoformat(data['expired']):
                return func(request, *args, **kwargs)
            else:
                return Response(data={"message": "Token Expired !"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"message": "Masukan Token !"}, status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response(data={"message": "Token tidak Valid"}, status=status.HTTP_400_BAD_REQUEST)

    return inner


def api_key_required(func):
    def inner(request, *args, **kwargs):
        try:
            if 'api_key' in request.GET:
                store = TblStore.objects.filter(api_key=request.GET['api_key']).values().first()
                if store:
                    if store['limited'] < 100:
                        TblStore.objects.filter(api_key=request.GET['api_key']).update(limited=store['limited'] + 1)
                        return func(request, *args, **kwargs)
                    else:
                        return Response(data={"message": "Api Key Limit Akses"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data={"message": "Api Key Tidak Valid"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"message": "Masukan Api Key !"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={"message": "Api Key Tidak Valid"}, status=status.HTTP_400_BAD_REQUEST)

    return inner