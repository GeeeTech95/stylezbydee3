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

    def get_success_url(self):
        user = self.request.user
        """if not user.email_verified:
            #url = reverse("verify-email")
            pass

        elif not user.phone_number_verified:
            #url = reverse("verify-phone-number")
            pass

        else:"""
        if user.is_staff :
            url = reverse("myadmin:dashboard")
        if user.is_company_staff :
            
            url = reverse("staff-dashboard")    
        url = reverse("dashboard")
        return url



    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            email = data.get("email")
            password = data.get("password")
            print(email,password)

            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                auth_token, created = Token.objects.get_or_create(user=user)

                return Response(
                    {
                        "auth_token": auth_token.key,
                        "success_url": self.get_success_url()
                    }
                )

            else:
                return Response(
                    {"detail": "authentication failed, please enter the correct credentials"},
                    status=400
                )

        else:
            return Response(
                serializer.errors,
                status=400
            )


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
