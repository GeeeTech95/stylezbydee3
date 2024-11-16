from cgitb import lookup
from rest_framework.response import Response
from rest_framework import generics 
from rest_framework.authtoken.models import Token
from rest_framework import exceptions

from django_rest_passwordreset.models import ResetPasswordToken, clear_expired, get_password_reset_token_expiry_time, \
    get_password_reset_lookup_field

from django_rest_passwordreset.signals import reset_password_token_created

import unicodedata
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from .serializers import (
    ResetPasswordSerializer
)


HTTP_USER_AGENT_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
HTTP_IP_ADDRESS_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')


def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    normalized1 = unicodedata.normalize('NFKC', s1)
    normalized2 = unicodedata.normalize('NFKC', s2)

    return normalized1.casefold() == normalized2.casefold()


class ResetPasswordRequestToken(generics.GenericAPIView):
    """
    An Api View which provides a method to request a password reset token based on
    an e-mail address or username

    Sends a signal reset_password_token_created when a reset token was created
    """
 
    permission_classes = []
    serializer_class = ResetPasswordSerializer
    model = get_user_model()

    def get_users(self,username,email) :
        #try finding users by username first
        if username :
            users = self.model.objects.filter(
                username__iexact = username
            )
            self.lookup = ("username" , username)
        else :
            # find a user by email address (case insensitive search) or email
            users = self.model.objects.filter(email__iexact = email)
            self.lookup = ("email", email)
        
        return users    



    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True) :
            return Response(serializer.errors,400)
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")

        # before we continue, delete all existing expired tokens
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # datetime.now minus expiry hours
        now_minus_expiry_time = timezone.now() - timedelta(hours=password_reset_token_validation_time)

        # delete all tokens where created_at < now - 24 hours
        clear_expired(now_minus_expiry_time)
        
        users = self.get_users(username,email)
        
        active_user_found = False

        # iterate over all users and check if there is any user that is active
        # also check whether the password can be changed (is useable), as there could be users that are not allowed
        # to change their password (e.g., LDAP user)
        for user in users:
            if user.eligible_for_reset():
                active_user_found = True
                break

        # No active user found, raise a validation error
        # but not if DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE == True
        if not active_user_found and not getattr(settings, 'DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE', False):
            raise exceptions.ValidationError({
                self.lookup[0]: [_(
                    "We couldn't find an account associated with that {0}. Please try a different {0}.".format(self.lookup[0]))],
            })

        # last but not least: iterate over all users that are active and can change their password
        # and create a Reset Password Token and send a signal with the created token
        for user in users:
            if user.eligible_for_reset() and \
                _unicode_ci_compare(self.lookup[1], getattr(user,self.lookup[0])):
                
                # define the token as none for now
                token = None

                # check if the user already has a token
                if user.password_reset_tokens.all().count() > 0:
                    # yes, already has a token, re-use this token
                    token = user.password_reset_tokens.all()[0]
                else:
                    # no token exists, generate a new token
                    token = ResetPasswordToken.objects.create(
                        user=user,
                        user_agent=request.META.get(HTTP_USER_AGENT_HEADER, ''),
                        ip_address=request.META.get(HTTP_IP_ADDRESS_HEADER, ''),
                    )
                # send a signal that the password token was created
                # let whoever receives this signal handle sending the email for the password reset
                reset_password_token_created.send(sender=self.__class__, instance=self, reset_password_token=token)
        
        # done, return the hidden(email address receiving the mail, the 
        return Response(
            {'email_receipient': users.first().email_hidden,"status" : "OK"})


