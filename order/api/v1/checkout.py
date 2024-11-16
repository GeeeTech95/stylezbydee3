from order.models import Order as OrderModel
from cart.api.v1.serializers import CreateCartSerializer
from .serializers import ShippingDetailSerializer
from rest_framework import generics
from rest_framework.response import Response
import ast
import json
from django.urls import reverse



class Checkout(generics.GenericAPIView) :

  
    def post(self,request,*args,**kwargs) :
        data = request.data
        feedback = {}
        shipping_data = ast.literal_eval(data['shipping_details'])
        shipping_details_serializer = ShippingDetailSerializer(data=shipping_data,context={"request" : request})
        if shipping_details_serializer.is_valid() :
            cart_serializer = CreateCartSerializer(data=data['cart'],many =True,context={"request" : request} )
            if cart_serializer.is_valid() :
                #save shipping details
                sd = shipping_details_serializer.save()
                #save cart
                cart = cart_serializer.save()[0]
                print(cart)
                #create order
                order =  OrderModel.objects.create(
                    shipping_info =  sd,
                    cart = cart,
                    total = cart.get_total_amount(),
                    currency = cart.get_currency(),
                    user = request.user if request.user.is_authenticated else None
                )
                return Response(
                    {"detail_url" :  reverse("order-detail",args = [order.number])},
                    status = 201
                )
            else :
                feedback['cart_error'] = True
                feedback['error'] = cart_serializer.errors
       
                return Response(feedback,status = 400)   

        else :
            feedback['shipping_details_error'] = True
            feedback['error'] = shipping_details_serializer.errors
            return Response(
                feedback,
                status = 400
                )        
               
     
        

