# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib import messages
# from datetime import datetime


from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
import logging
import json
from django.views.decorators.csrf import csrf_exempt

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            username = body.get("userName")
            password = body.get("password")
        except Exception:
            return JsonResponse({"status": "Invalid JSON"}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse(
                {"userName": username, "status": "Authenticated"},
                status=200
            )
        else:
            return JsonResponse({"status": "Invalid credentials"}, status=401)

    return JsonResponse({"status": "Bad request"}, status=400)


@csrf_exempt
def logout_user(request):
    if request.method == "GET":
        logout(request)          # Destroy session
        data = {"userName": ""}  # Return empty username
        return JsonResponse(data, status=200)

    return JsonResponse({"status": "Bad request"}, status=400)
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            username   = body.get("userName")
            password   = body.get("password")
            first_name = body.get("firstName")
            last_name  = body.get("lastName")
            email      = body.get("email")
        except Exception:
            return JsonResponse({"status": False, "error": "Invalid JSON"}, status=400)

        # If username already exists, return error expected by React
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"status": False, "error": "Already Registered"},
                status=400
            )

        # Create the user
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name or "",
            last_name=last_name or "",
            email=email or "",
        )

        # Log the user in
        login(request, user)

        # React expects `status` truthy and `userName`
        return JsonResponse(
            {"status": True, "userName": username},
            status=201
        )

    return JsonResponse({"status": False, "error": "Bad request"}, status=400)
