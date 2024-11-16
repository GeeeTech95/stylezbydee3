from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .serializers import UserSerializer


class UpdateProfile(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    model = get_user_model()
    feedback = {}
    status_code = 200

    def get_object(self, **kwargs):
        return self.request.user


    def post(self,request,*args,**kwargs) :

        user = self.get_object()
        serializer = self.serializer_class(
                data=request.data,
            )

        if serializer.is_valid():
            instance = serializer.update(
                user,
                serializer.validated_data)
            self.feedback = self.serializer_class(instance).data,

        else:
            self.feedback = serializer.errors
            self.status_code = 400  
        
        return Response(self.feedback,self.status_code)
