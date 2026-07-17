from typing import cast

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login as django_login

from .models import UserProfile


# ==========================================================
# LOGIN
# ==========================================================

@api_view(["POST"])
def login(request):

    username = request.data.get("username", "")
    password = request.data.get("password", "")

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:
        return Response(
            {
                "success": False,
                "message": "Invalid Username or Password"
            },
            status=401
        )
    django_login(request, user)
    
    user = cast(User, user)

    if user.is_superuser:
        role = "SYSTEM_OWNER"
    else:
        profile = UserProfile.objects.filter(user=user).first()
        role = profile.role if profile else "OPERATOR"

    return Response({
        "success": True,
        "username": user.username,
        "role": role,
        "is_superuser": user.is_superuser
    })


# ==========================================================
# LIST USERS
# ==========================================================

@api_view(["GET"])
def list_users(request):

    users = []

    for u in User.objects.all():

        u = cast(User, u)

        if u.is_superuser:
            role = "SYSTEM_OWNER"
        else:
            profile = UserProfile.objects.filter(user=u).first()
            role = profile.role if profile else "OPERATOR"

        users.append({
            "id": u.pk,
            "username": u.username,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email,
            "role": role,
            "active": u.is_active
        })

    return Response(users)


# ==========================================================
# CREATE USER
# ==========================================================

@api_view(["POST"])
def create_user(request):

    creator = cast(User, request.user)

    if not creator.is_superuser:
        return Response(
            {
                "success": False,
                "message": "Permission Denied"
            },
            status=403
        )

    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")
    role = request.data.get("role", "OPERATOR")

    if not username or not password:
        return Response(
            {
                "success": False,
                "message": "Username and Password are required"
            },
            status=400
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {
                "success": False,
                "message": "Username already exists"
            },
            status=400
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    profile = UserProfile.objects.get(user=user)

    profile.role = role
    profile.created_by = creator
    profile.save()

    return Response(
        {
            "success": True,
            "message": "User Created Successfully"
        }
    )


# ==========================================================
# UPDATE USER
# ==========================================================

@api_view(["PUT"])
def update_user(request, user_id):

    creator = cast(User, request.user)

    if not creator.is_superuser:
        return Response(
            {
                "success": False,
                "message": "Permission Denied"
            },
            status=403
        )

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "User not found"
            },
            status=404
        )

    profile = UserProfile.objects.get(user=user)

    user.username = request.data.get("username", user.username)
    user.email = request.data.get("email", user.email)
    user.first_name = request.data.get("first_name", user.first_name)
    user.last_name = request.data.get("last_name", user.last_name)

    if "active" in request.data:
        user.is_active = request.data["active"]

    profile.role = request.data.get("role", profile.role)

    user.save()
    profile.save()

    return Response(
        {
            "success": True,
            "message": "User Updated Successfully"
        }
    )


# ==========================================================
# DELETE USER
# ==========================================================

@api_view(["DELETE"])
def delete_user(request, user_id):

    creator = cast(User, request.user)

    if not creator.is_superuser:
        return Response(
            {
                "success": False,
                "message": "Permission Denied"
            },
            status=403
        )

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "User not found"
            },
            status=404
        )

    if user.is_superuser:
        return Response(
            {
                "success": False,
                "message": "System Owner cannot be deleted"
            },
            status=400
        )

    user.delete()

    return Response(
        {
            "success": True,
            "message": "User Deleted Successfully"
        }
    )
    
@api_view(["PUT"])
def reset_password(request, user_id):

    creator = cast(User, request.user)

    if not creator.is_superuser:
        return Response(
            {
                "success": False,
                "message": "Permission Denied"
            },
            status=403
        )

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "User not found"
            },
            status=404
        )

    password = request.data.get("password")

    if not password:
        return Response(
            {
                "success": False,
                "message": "Password is required"
            },
            status=400
        )

    user.set_password(password)
    user.save()

    return Response(
        {
            "success": True,
            "message": "Password Updated Successfully"
        }
    )