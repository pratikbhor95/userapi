from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

class custom_userSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )
    confirm_password = serializers.CharField(
        write_only=True
        )
    
    class Meta:
        model = User
        fields =('id',
                'username',
                'first_name',
                'last_name',
                'email',
                'password',
                'confirm_password',
                'is_staff')


    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    


    def validate(self, attrs):
        print(attrs)
        print(attrs.get("password") , attrs.get("confirm_password"))
        
        if not attrs.get("password") == attrs.pop("confirm_password"):
            return Response(data={"message":"password not matched, Please enter correct password"}, status = status.HTTP_404_NOT_FOUND)
        return attrs



class custom_userSerializer_by_id(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields =('id',
                'first_name',
                'last_name',
                'email',
                'password',
                'is_staff',
                'is_superuser')


