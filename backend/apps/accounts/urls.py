from django.urls import path

from .views import (
    login,
    list_users,
    create_user,
    update_user,
    delete_user,
    reset_password,
)

urlpatterns = [

    path("login/", login),

    path("users/", list_users),

    path("users/create/", create_user),

    path("users/<int:user_id>/update/", update_user),

    path("users/<int:user_id>/delete/", delete_user),

    path("users/<int:user_id>/reset-password/", reset_password),

]