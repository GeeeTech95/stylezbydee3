
from django.contrib.auth import get_user_model
from urllib import response
from rest_framework import generics
from rest_framework.response import Response

from django.shortcuts import get_list_or_404, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import Max
from .serializers import ProductMediaSerializer, ProductSerializer,FilterSerializer
from shop.models import Product, ProductCategory


class SearchProduct(generics.GenericAPIView):
    serializer_class = ProductSerializer
    model = Product
    error = None
    permission_classes = []

    def __init__(self):
        self.product_list = {}
        self.category_navigation = {}
        self.feedback = {}
        self.recommendation = False
        self.category = None
        super().__init__()

    def get(self, request, *args, **kwargs):
        # the category slug is passed in to the serializer to create the necssary
        # field for attribute search
        ctx = {
            "request": request, 
            "category_slug": request.GET.get("cat"),
            "item_domain" : kwargs['item_domain']
            }
        serializer = SearchFilterSerializer(
            data=request.GET,
            context=ctx
        )
        if serializer.is_valid():
            validated_data = serializer.validated_data
            queryset, query, filters = serializer.get_queryset(
                validated_data
            )

            if query:
                queryset = queryset.filter(query)

            if filters:
                queryset = queryset.filter(**filters)

            # if category is available
            cat = validated_data.get('cat')
            if cat:
                self.category_navigation['html'] = cat.navigation_crumbs(kwargs['item_domain'])

        else:

            # just recommend
            queryset = Product.objects.all()

        if self.error:
            return Response(
                {"detail": self.error},
                status=400
            )

        if queryset:
            self.product_list['html'] = render_to_string(
                "products.html",
                {"products": queryset},
                request=request
            )

        else:
            self.product_list['html'] = render_to_string(
                "no-content.html",
                {"title": "No products",
                    "text": "No product matched your search parameters, edit and search again"}
            )

        self.product_list["json"] = self.serializer_class(
            queryset, many=True).data

        self.feedback['product_list'] = self.product_list
        self.feedback['navigation'] = self.category_navigation

        return Response(
            self.feedback
        )


class ProductListX(generics.ListAPIView):
    model = Product
    serializer_class = ProductSerializer
    permission_classes = []
    products = None
    status_code = 200
    response = {}

    def __init__(self,*args,**kwargs):
        super(ProductListX, self).__init__(*args,**kwargs)
       
      
    def on_category_slug(self):
        slug = self.request.GET.get('category_slug')
        if not slug:
            self.response = {"detail": "A category slug was expected"}
            self.error = 400
            return
        category = get_object_or_404(ProductCategory, slug=slug)
        products = category.get_product_recommendation(self.request.user)

        if not products:
            self.response['json'] = {}
            self.response['html'] = render_to_string(
                "no-content.html", {"title": "No products yet", "text": "There are no products in this category yet."})
        return products

    def build_filters(self,products) :
        ctx = {
            "ready_to_ship" : products.filter(is_ready_to_ship = True).count(),
            "free_delivery" : products.filter(is_free_delivery  = True).count(),
            "categories" : [cat.name for cat in ProductCategory.objects.all()],
            "attributes" : [ product.product_attribute_values()  for product in products ],
            "max_price" : products.aggregate(
                              max_price=Max("price")
                         )['max_price'] 
        }
        html_filters  = render_to_string("filters.html",ctx,request = self.request)
        return html_filters

    def get(self, request, *args, **kwargs):
        params = request.GET
        products = self.model.objects.all()
        gender = params.get('g')

        if gender and gender.lower() in ['men','women','unisex'] :
            products = products.filter(gender = gender )
    
        if products:
            self.response['json'] = self.serializer_class(
                products, many=True).data
            self.response['html'] = render_to_string(
                "product-list.html", {"products": products}, request=self.request
                )
            #self.response['filters'] = self.build_filters(products)

        return Response(
            self.response,
            self.status_code
        )


class ProductList(generics.ListAPIView):
    model = Product
    serializer_class = ProductSerializer
    permission_classes = []
    products = None
    status_code = 200
    response = {}

    def __init__(self,*args,**kwargs):
        self.product_list = {}
        self.feedback = {}
        self.recommendation = False
        self.category = None
        self.error = None
        super(ProductList, self).__init__(*args,**kwargs)
       
      
    def get(self, request, *args, **kwargs):
        # the category slug is passed in to the serializer to create the necssary
        # field for attribute search
        ctx = {
            "request": request, 
            "category_slug": request.GET.get("cat"),
           
            }
        data = {key.strip("?"):value for key,value in request.GET.items()}

        serializer = FilterSerializer(
            data= data,
            context=ctx
        )
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            queryset, query, filters = serializer.get_queryset(
                validated_data
            )

            if query:
                queryset = queryset.filter(query)

            if filters:
                queryset = queryset.filter(**filters)

        else:
            print(serializer.errors)
            # just recommend
            queryset = Product.objects.all()

        if self.error:
            return Response(
                {"detail": self.error},
                status=400
            )
        currency = request.GET.get("currency","USD")
        
        queryset = ProductSerializer(
            queryset,
            many = True,
            context = { "currency" : currency}
        ).data
        
        self.product_list['html'] = render_to_string(
            "product-list.html",
            {"products": queryset,"currency" : currency},
            request=request
        )

        self.product_list["json"] = queryset

        self.feedback['product_list'] = self.product_list
      

        return Response(
            self.feedback
        )


