from unicodedata import decimal
from rest_framework import generics
from rest_framework.response import Response

from django.shortcuts import get_list_or_404, get_object_or_404
from django.template.loader import render_to_string


from .serializers import ProductSerializer, FilterSerializer
from shop.models import Product


class UpdateFilters(generics.GenericAPIView):
    """
    client sends a request to
    """

    def __init__(self):
        self.feedback = {}
        self.search_filters = {}

    serializer_class = FilterSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        # recreate filters based on passed search params
        # so user can modify them
        filters = {}
        filters_list = []

        serializer = self.serializer_class(
            data=request.GET,
            context={
                "category_slug": request.GET.get("cat"),
                    "request" : request
                }
        )
        if serializer.is_valid():
       
            context, filters_list = serializer.build_client_filters(
                serializer.validated_data)
          
        else:
            context = {}

        filters['html'] = render_to_string(
            "filters.html",
            context,
            request=self.request
        )

        self.feedback['filters_list'] = filters_list
        self.feedback['filters'] = filters

        return Response(
            self.feedback
        )


        

class SearchProduct(generics.GenericAPIView):
    serializer_class = ProductSerializer
    model = Product
    error = None
    permission_classes = []

    def __init__(self):
        self.search_result = {}
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
            self.search_result['html'] = render_to_string(
                "products.html",
                {"products": queryset},
                request=request
            )

        else:
            self.search_result['html'] = render_to_string(
                "no-content.html",
                {"title": "No products",
                    "text": "No product matched your search parameters, edit and search again"}
            )

        self.search_result["json"] = self.serializer_class(
            queryset, many=True).data

        self.feedback['search_result'] = self.search_result
        self.feedback['navigation'] = self.category_navigation

        return Response(
            self.feedback
        )
