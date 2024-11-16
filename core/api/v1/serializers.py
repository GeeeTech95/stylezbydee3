from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer) :  
    class Meta() :
        fields  = '__all__'