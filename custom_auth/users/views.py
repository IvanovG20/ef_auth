import os
import jwt
from datetime import datetime, timedelta

from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User, TokenBlackList, UserPermission
from users.permissions import HasPermission

from users.serializers import (RegisterSerializer, LoginSerializer,
                               TokenSerializer, MessageSerializer,
                               ProjectSerializer, AssignPermissionSerializer,
                               is_admin)

SECRET = os.getenv("JWT_SECRET", "super_secret_key_123")


def generate_token(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(hours=2),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=["HS256"])


def get_user_from_request(request):
    header = request.headers.get("Authorization")

    if not header:
        return None

    token = header.split()[1]

    if TokenBlackList.objects.filter(token=token).exists():
        return None

    payload = decode_token(token)
    if not payload:
        return None

    return User.objects.filter(
        id=payload["user_id"],
        is_active=True
    ).first()


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = serializer.save()

        return Response({"id": user.id})


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data

        user = User.objects.filter(email=data["email"]).first()

        if not user or not check_password(data["password"], user.password):
            return Response({"error": "Invalid credentials"}, status=401)

        token = generate_token(user)

        return Response(TokenSerializer({"token": token}).data)


class LogoutView(APIView):
    def post(self, request):
        header = request.headers.get("Authorization")

        if not header:
            return Response(status=401)

        token = header.split()[1]
        TokenBlackList.objects.create(token=token)

        return Response(MessageSerializer({"message": "logout"}).data)


class ProjectView(APIView):
    def get(self, request):
        user = get_user_from_request(request)

        if not user:
            return Response(status=401)

        permission = HasPermission("project", ["view", "edit"])

        if not permission.has_permission(request, self):
            return Response(status=403)

        data = {"projects": ["A", "B"]}

        return Response(ProjectSerializer(data).data)


class EditProjectView(APIView):
    def post(self, request):
        user = get_user_from_request(request)

        if not user:
            return Response(status=401)

        permission = HasPermission("project", "edit")

        if not permission.has_permission(request, self):
            return Response(status=403)

        return Response(MessageSerializer({"message": "project updated"}).data)


class AssignPermissionView(APIView):

    def post(self, request):
        user = get_user_from_request(request)

        if not user:
            return Response(status=401)

        if not is_admin(user):
            return Response(status=403)

        serializer = AssignPermissionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data

        target_user = User.objects.filter(id=data["user_id"]).first()

        if not target_user:
            return Response({"error": "user not found"}, status=404)

        permission, created = UserPermission.objects.get_or_create(
            user=target_user,
            resource=data["resource"],
            action=data["action"]
        )

        return Response({"status": "granted"})
