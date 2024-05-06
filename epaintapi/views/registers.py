import json
from django.http import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from epaintapi.models import UserInfo


@csrf_exempt
def login_user(request):

    body = request.body.decode("utf-8")
    req_body = json.loads(body)

    if request.method == "POST":

        name = req_body["username"]
        pass_word = req_body["password"]
        authenticated_user = authenticate(username=name, password=pass_word)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps(
                {"valid": True, "token": token.key, "id": authenticated_user.id}
            )
            return HttpResponse(data, content_type="application/json")

        else:
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type="application/json")

    return HttpResponseNotAllowed(permitted_methods=["POST"])


@csrf_exempt
def register_user(request):

    req_body = json.loads(request.body.decode())

    email = req_body.get("email")
    username = req_body.get("username")

    if User.objects.filter(email=email).exists():
        return JsonResponse({"message": "Email already exists"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"message": "Username already exists"}, status=400)

    new_user = User.objects.create_user(
        username=req_body["username"],
        email=req_body["email"],
        password=req_body["password"],
        first_name=req_body["first_name"],
        last_name=req_body["last_name"],
    )

    user_info = UserInfo.objects.create(
        phone_number=req_body["phone_number"],
        address=req_body["address"],
        user=new_user,
    )

    user_info.save()

    token = Token.objects.create(user=new_user)

    data = json.dumps({"token": token.key, "id": new_user.id})

    return HttpResponse(
        data, content_type="application/json", status=status.HTTP_201_CREATED
    )
