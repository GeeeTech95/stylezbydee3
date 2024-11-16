from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

from rest_framework import status
from .serializers import LoginSerializer



from .serializers import UserSerializer, UpdatePasswordSerializer
from django.urls import reverse


class RegisterAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UpdatePassword(generics.RetrieveUpdateAPIView):
    serializer_class = UpdatePasswordSerializer

    def patch(self, request, *args, **kwargs):
        context = {"request": request}
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid():
            serializer.update(serializer.validated_data)
            # relogin user
            login(request, request.user)
            return Response()
        else:
            return Response(serializer.errors, status=400)
