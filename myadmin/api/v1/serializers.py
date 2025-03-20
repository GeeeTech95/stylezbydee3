from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework.authtoken.models import Token




from fashion.models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_id', 'gender', 'full_name', 'home_address', 'office_address', 'phone_number', 'whatsapp_number', 'email', 'passport']




