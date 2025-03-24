from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


from django.contrib.auth import authenticate, login, logout

from .serializers import (
    UserSerializer,
    LoginSerializer,
)

from django.urls import reverse


class Register(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    model = get_user_model()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            # log user in
            login(request, user)

            return Response(
                {"status" : "success","account_id" : user.account_id},
                status=201,
            )

        else:
            return Response(
                serializer.errors,
                status=400
            )



class Login(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    model = get_user_model()
    serializer_class = LoginSerializer

    def get_success_url(self, user):
        if user.is_staff:
            return reverse("myadmin:dashboard")
        elif user.is_company_staff:
            return reverse("staff-dashboard")
        return reverse("dashboard")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            email = data.get("email")
            password = data.get("password")

            user = get_user_model().objects.filter(email=email).first()
            if not user:
                return Response({"detail": "No account found with this email."}, status=400)

            user = authenticate(email=email, password=password)
            if user is None:
                return Response({"detail": "Incorrect password. Please try again."}, status=400)

            login(request, user)
            auth_token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "auth_token": auth_token.key,
                    "success_url": self.get_success_url(user),
                }
            )

        return Response(serializer.errors, status=400)


class Logout(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            #request.user.auth_token.delete()
            logout(request)
            
            return Response()
        else:
            return Response(
                {"detail": "You are already logged out"},
                status=400
            )
