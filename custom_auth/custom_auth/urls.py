from django.urls import path
from users.views import (RegisterView, LoginView, LogoutView,
                         ProjectView, EditProjectView,
                         AssignPermissionView)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("projects/", ProjectView.as_view()),
    path("projects/edit/", EditProjectView.as_view()),
    path("admin/assign-permission/", AssignPermissionView.as_view()),
]