
from urllib import request
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


from users.models import Notification
from .serializers import NotificationSerializer

class NotificationList(generics.ListAPIView):
    model = Notification
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.model.objects.all()


class NotificationDetail(generics.RetrieveAPIView) :
    model = Notification
    serializer_class  = NotificationSerializer

    def get_queryset(self) :
       return self.model.objects.all()

    