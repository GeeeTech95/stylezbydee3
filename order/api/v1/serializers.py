
from rest_framework import serializers
from order.models import ShippingDetail
from cart.api.v1.serializers import CreateCartSerializer
from core.api.v1.serializers import CountrySerializer
from core.models import Country
from users.api.v1.serializers import UserSerializer


class ShippingDetailSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Country.objects.all())
    user = UserSerializer(read_only=True)

    class Meta():
        model = ShippingDetail
        fields = '__all__'

    def create(self, validated_data):
        ship_detail = ShippingDetail(**validated_data)
        user = self.context['request'].user
        if user.is_authenticated:
            ship_detail.user = user
        ship_detail.save()
        return ship_detail
