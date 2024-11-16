from rest_framework import serializers
from cart.models import Cart, CartLine, CartLineAttribute
from shop.api.v1.serializers import ProductSerializer
from shop.models import ProductAttribute, Product, ProductAttributeValue


class CreateCartSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super(CreateCartSerializer, self).__init__(*args, **kwargs)
        request = self.context['request']
        if request.user.is_authenticated : user = request.user
        else : user = None
        
        self.cart = Cart.objects.create(
            owner=user
        )
        print('sddd')

    # for creating
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True)
    quantity = serializers.IntegerField()
    attributes = serializers.DictField(allow_empty=False)

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        attributes = validated_data['attributes']
        
        cart_line = CartLine.objects.create(
            cart=self.cart,
            product=product,
            quantity=quantity,
            price_currency=product.currency,
            unit_price=product.price,

        )
        for attribute, value in attributes.items():
            cart_line_attr = CartLineAttribute.objects.create(
                line=cart_line,
                option=attribute,
                value=value
            )

        return self.cart

    def validate_quantity(self, qty):
        # check if the qty is less than stock records
        return qty

    def validate_product(self, product):
        # check if product us still in stock and is still available
        return product

    def validate_attributes(self, attributes):

        # ensure that all selected attributes are in stock
        # ensure that they are valid attributes
        normalized_attributes = {}
        for attr, value in attributes.items():
            attribute = ProductAttribute.objects.filter(code=attr)
            
            if attribute.exists():
                normalized_attributes[attribute.first()] = value
        return normalized_attributes


class CartSerializer(serializers.ModelSerializer):

    class Meta():
        model = Cart
        fields = ['owner']
