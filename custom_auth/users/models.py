from django.db import models


class User(models.Model):
    """Кастомная модель пользователя(не из коробки)"""

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TokenBlackList(models.Model):
    token = models.TextField()


class UserPermission(models.Model):

    ACTION_VIEW = "view"
    ACTION_EDIT = "edit"
    ACTION_DELETE = "delete"

    ACTION_CHOICES = [
        (ACTION_VIEW, "View"),
        (ACTION_EDIT, "Edit"),
        (ACTION_DELETE, "Delete"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.CharField(max_length=50)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)

    class Meta:
        unique_together = ("user", "resource", "action")