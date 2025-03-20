from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from fashion.models import Client
from django.shortcuts import get_object_or_404
from .serializers import ClientSerializer



class ClientUpdateView(generics.UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer



class ClientDeleteView(APIView):
    """API View to delete a client """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args,**kwargs):
        pk = kwargs.get('pk')
        client = get_object_or_404(Client, pk=pk)
        client.is_active = False
        client.save()
        return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
