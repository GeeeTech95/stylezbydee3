
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.core import exceptions
from django.contrib.auth import password_validation
from django.conf import settings
from django.urls import reverse
from django.forms.models import model_to_dict

from users.models import Notification, NotificationCategory


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['full_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        user = get_user_model()(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            gender=validated_data['gender'],
           
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user





class NotificationCategorySerializer(serializers.ModelSerializer):

    class Meta():
        model = NotificationCategory
        fields = ['name', 'pk']


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category = NotificationCategorySerializer()

    class Meta():
        model = Notification
        fields = ['user', 'category', 'message', 'title', 'date', 'image','id']


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    def validate_email(self, email):
        if email:
            if not get_user_model().objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    "No user with this email was found")
        return email

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        # at least one must be supplied
        if not username and not email:
            raise serializers.ValidationError(
                "Credentials are incomplete, email or username is expected")
        return data


class SettingSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(
        max_length=10, write_only=True, validators=[validate_password])
    old_password = serializers.CharField(max_length=10, write_only=True)

    class Meta():
        model = get_user_model()
        fields = [
            'pk',
            'passport',
            'gender',
            'first_name',
            'last_name',
            'phone_number',
            'otp',
            'email',
            'old_password',
            'new_password'
        ]

    def validate_new_password(self, password):
        user = self.context['request'].user
        if check_password(password, user.password):
            raise serializers.ValidationError(
                "Your new password is the same as your old password. it is not allowed")
        return password

    def validate_comfirm_password(self, phone_number):
        return phone_number

    def validate(self, data):
        user = self.context['request'].user
        # check if secured credentials is about to change
        if data.get("email") or data.get("phone_number") or data.get("password"):
            # make sure password was entered
            old_password = data.get("old_password")
            if not old_password:
                raise serializers.ValidationError(
                    "You need to enter your password in order to effect this change")

            if not check_password(old_password, user.password):
                raise serializers.ValidationError(
                    "The password you entered is not correct please crosscheck")

            # if user is changing new password
            new_password = data.get("new_password")
            if new_password:
                user.set_password(new_password)
        return data

    """def perform_update(self) :
        print("ss")
        _update_fields = self.data.keys() 
        user = self.context['request'].user
        for _field in _update_fields :
            setattr(user,self.data[_field])
        user.save()  """


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True,
    )

    new_password_comfirmation = serializers.CharField(
        write_only=True
    )

    def validate_old_password(self, password):
        user = self.context['request'].user
        if not check_password(password, user.password):
            raise serializers.ValidationError(
                "You enetered a wrong password, please crosscheck")
        return password

    def validate_new_password(self, password):
        user = self.context['request'].user
        if check_password(password, user.password):
            raise serializers.ValidationError(
                "Your new password cannot be the same as your old password.")
        errors = dict()
        try:
            # validate the password and catch the exception
            password_validation.validate_password(password=password, user=user)
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return password

    def validate(self, data):
        new_password = data.get("new_password")
        new_password_comfirm = data.get("new_password_comfirmation")

        if new_password != new_password_comfirm:
            raise serializers.ValidationError(
                "New password and new password comfirmation must match.")
        return data

    def update(self, validated_data):
        # change password
        user = self.context['request'].user
        user.set_password(validated_data['new_password'])
        user.save()


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate_username(self, username):
        if username and not get_user_model().objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError(
                "We couldn't find an account associated with that username. Please try a different username"
            )
        return username

    def validate_email(self, email):
        if email and not get_user_model().objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "We couldn't find an account associated with that email. Please try a different e-mail address"
            )
        return email

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        if not username and not email:
            raise serializers.ValidationError(
                "username or email address was expected"
            )

        return data
