from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User, UserPermission


# ================= REGISTER =================

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["password_repeat"]:
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("User already exists")

        return data

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            password=make_password(validated_data["password"])
        )

        UserPermission.objects.create(
            user=user,
            resource="project",
            action="view"
        )

        return user


def is_admin(user):
    return user and user.is_admin


class AssignPermissionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    resource = serializers.CharField()
    action = serializers.ChoiceField(
        choices=["view", "edit", "delete"]
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class ProjectSerializer(serializers.Serializer):
    projects = serializers.ListField(
        child=serializers.CharField()
    )


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
