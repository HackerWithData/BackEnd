from rest_framework.views import APIView
from rest_framework.permissions import (
    BasePermission,
    AllowAny,
)
from users.models import User
from ..serializers.user_serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import PBKDF2PasswordHasher

class IsAdminOrSelf(BasePermission):
    def has_permission(self, request, view):
        return request.user.uuid == view.kwargs['uuid'] or (request.user and request.user.is_staff)


class UserDetail(APIView):

    permission_classes = [IsAdminOrSelf]

    def get_object(self, uuid):
        try:
            user = User.objects.get(uuid=uuid)
            return user
        except User.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        uuid = kwargs['uuid']
        user = self.get_object(uuid)
        if user is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pwd = serializer.validated_data['password']
        pwdhaser = PBKDF2PasswordHasher()
        pwd = pwdhaser.encode(password=pwd, salt=pwdhaser.salt())
        serializer.validated_data['password'] = pwd
        serializer.save()
        return Response(serializer.data)






