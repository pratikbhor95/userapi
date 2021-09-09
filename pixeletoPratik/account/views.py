from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404 , JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import custom_userSerializer , custom_userSerializer_by_id
from rest_framework.pagination import PageNumberPagination
# Create your views here.

@csrf_exempt
@api_view(['GET', 'POST'])
def get_custom_user_list(request):
    if request.method == "GET":
        acc = User.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(acc, request)
        serialize = custom_userSerializer(result_page , many = True )
        return paginator.get_paginated_response(serialize.data)

    elif request.method == "POST":
        serialize = custom_userSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def get_by_id(request,id):

    try:
        user_obj = User.objects.get(id = id)
    except User.DoesNotExist:
        return Response(data={"message":"data not found, Please enter correct id"}, status = status.HTTP_404_NOT_FOUND)


    if request.method == "GET":
        serialize = custom_userSerializer_by_id(user_obj)
        return Response(serialize.data, status=status.HTTP_200_OK)


    elif request.method == "PUT":
        print(request.data)
        print('id : ' , id)
        user_obj = User.objects.get(id = id)            
        if not user_obj.check_password(request.data.get("password")):
            return Response(data={"message":"password not match"}, status = status.HTTP_404_NOT_FOUND)
        else : 
            serialize = custom_userSerializer_by_id(instance=user_obj , data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response(serialize.data, status=status.HTTP_201_CREATED)
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user_obj.delete()
        return Response(data={"message":"User Removed"}, status = status.HTTP_200_OK)


        

