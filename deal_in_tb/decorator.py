from deal_in_tb.jwt import JWTAuth
from rest_framework.response import Response
from deal_in_tb.models import TblUser

import datetime


def token_required(func):
    def inner(request, *args, **kwargs):
        try:
            jwt = JWTAuth()
            if 'Authorization' in request.headers:
                data = jwt.decode(request.headers['Authorization'])
                user = TblUser.objects.filter(username=data['username']).values().first()
                if datetime.datetime.now() < datetime.datetime.fromisoformat(data['expired']):
                    return func(request, *args, **kwargs)
                else:
                    return Response(data={"message": "Token Expired !"}, status=400)
            else:
                return Response(data={"message": "Masukan Token !"}, status=400)
            
        except:
            return Response(data={"message": "Token tidak Valid"}, status=400)

    return inner


def api_key_required(func):
    def inner(request, *args, **kwargs):
        try:
            if 'api_key' in request.GET:
                user = TblUser.objects.filter(api_key=request.GET['api_key']).values().first()
                if user:
                    if user['limited'] < 100:
                        TblUser.objects.filter(api_key=request.GET['api_key']).update(limited=user['limited'] + 1)
                        return func(request, *args, **kwargs)
                    else:
                        return Response(data={"message": "Api Key Limit Akses"}, status=400)
                else:
                    return Response(data={"message": "Api Key Tidak Valid"}, status=400)
            return Response(data={"message": "Masukan Api Key !"}, status=400)
                
        except:
            return Response(data={"message": "Api Key Tidak Valid"}, status=400)

    return inner