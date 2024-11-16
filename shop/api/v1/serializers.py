
from rest_framework import serializers
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q, Max, Min
from django.db.models.query import QuerySet


from shop.models import Product, ProductAttribute, ProductAttributeOption, ProductAttributeOptionGroup, ProductAttributeValue, ProductClass, ProductCategory, ProductMedia
from users.api.v1.serializers import UserSerializer
from core.api.mixins import DynamicSerializerMixin
from shop.models import Currency





class ProductMediaSerializer(serializers.ModelSerializer):

    class Meta():
        model = ProductMedia
        fields = [
            "media",
            "tag"
        ]


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta():
        model = ProductCategory
        fields = ['name', 'image_url', 'children']

    def get_fields(self):
        fields = super(ProductCategorySerializer, self).get_fields()
        fields['children'] = ProductCategorySerializer(many=True)
        return fields


class CurrencySerializer(serializers.ModelSerializer) :

    class Meta() :
        model = Currency
        fields = ['name']

class ProductSerializer(DynamicSerializerMixin, serializers.ModelSerializer):
    media = ProductMediaSerializer(read_only=True)
    currency = CurrencySerializer()

    price_converted = serializers.SerializerMethodField()
    context = None

    #category = ProductCategorySerializer(read_only = True)

    def __init__(self, *args, **kwargs):
        # obtain the media fields and create a temprary serializer field
        media_fields = kwargs.pop('media_fields', None)
        super(ProductSerializer,self).__init__(*args, **kwargs)
        self.context = kwargs.get("context")
        if media_fields:
            field_update_dict = {
                field: serializers.FileField(required=False, write_only=True) for field in media_fields
            }
            self.fields.update(**field_update_dict)
    
    
    def get_price_converted(self, obj):
        currency = self.context['currency']
        return obj.convert_price(currency)

         
    class Meta():
        model = Product
        read_only_fields = [
            "pk",
            "product_id",
            'created_at',
            'last_modified',
            'rating',
            'success_url'
            'thumbnail',
            'price_converted'

        ]
        fields = [
            "pk",
            "media",
            "product_id",
            "description",
            "category",
            "product_class",
            'thumbnail',
            'title',
            'created_at',
            'last_modified',
            'slug',
            'price',
            'price_converted',
            'rating',
            'in_stock',
            'success_url',
            'currency'
           
        ]


     



class ProductClassSerializer(serializers.ModelSerializer):

    class Meta():
        model = ProductAttribute
        fields = [
            'name',
            'product_class'
        ]


class ProductAttributeOptionGroupSerializer(serializers.ModelSerializer):

    class Meta():
        model = ProductAttributeOptionGroup
        fields = ['name', 'option_values']


class ProductAttributeOptionSerializer(serializers.ModelSerializer):
    group = ProductAttributeOptionGroupSerializer(read_only=True)

    class Meta():
        read_only_fields = ['option', 'group']
        model = ProductAttributeOption
        fields = ['group', 'option', 'pk']


class ProductAttributeSerializer(serializers.ModelSerializer):
    product_class = ProductClassSerializer(read_only=True)
    option_group = ProductAttributeOptionGroupSerializer(read_only=True)

    class Meta():
        model = ProductAttribute
        fields = [
            'pk',
            'name',
            'product_class',
            'type',
            'option_group',
            'code'
        ]


class ProductAttributeValueSerializer(serializers.ModelSerializer):

    class Meta():
        model = ProductAttributeValue
        read_only_fields = ['product']
        fields = ['__all__']


class FilterSerializer (serializers.Serializer):
    min_price = serializers.IntegerField(required=False)
    max_price = serializers.IntegerField(required=False)
    ready_to_ship = serializers.BooleanField(required = False)
    free_delivery = serializers.BooleanField(required = False)
    cat = serializers.CharField(required=False)  # category slug
    q = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)
    g = serializers.CharField(required=False)

 
    def __init__(self, *args, **kwargs):
        super(FilterSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context')

        if context:
            category_slug = context.get('category_slug')
        else:
            category_slug = None

        # dynamicaly build fields based on the category
        if category_slug:
            klass = ProductClass.objects.filter(categories__slug=category_slug)
            if klass.exists():
                self.klass = klass.first()
            else:
                self.klass = None
            if self.klass:
                self.attributes = self.klass.attributes.all()

                for attr in self.attributes:
                    # build fields
                    # all filter fields must have required as False
                    if attr.is_multi_option:
                        serializer_class = serializers.PrimaryKeyRelatedField(
                            required=False,
                            queryset=ProductAttributeOption.objects.all()
                        )

                    elif attr.is_option:
                        serializer_class = serializers.PrimaryKeyRelatedField(
                            required=False,
                            queryset=ProductAttributeOption.objects.all()
                        )

                    elif attr.type == "BOOLEAN":
                        serializer_class = serializers.BooleanField(
                            required=False)

                    self.fields[attr.code] = serializer_class
    
    def validate_ready_to_ship(self,rts) :
        return rts
    
    def validate_currency(self,currency) :
        return currency


    def validate_cat(self, cat):
        if cat:
            
            category = ProductCategory.objects.filter(slug=cat)
           
            if category.exists():
                return category.first()
                
            else:
                return  cat

    def validate(self, data):
        # remove up null data
        #validated_data = {key: value for key,value in data.items() if value}
        return data


    def get_attribute_list(self, queryset):
        """ 
        get  map of attribute as key and a list of the attribute values captured in this
         queryset as key values
        e.g -> colour : ['red','orange' ]
        """
        attribute_list = {}
        #if not self.cat:
        #return []

        attr_values = ProductAttributeValue.objects.filter(
            product__in=queryset).distinct()

        for attr_val in attr_values :
            values = attribute_list.get(attr_val.attribute,[])
            #attr.val can either be a queryset for multioptions, 
            # and attribute option object for options
            #or a regular var
            value = attr_val.value
            if isinstance(value,QuerySet) : 
                for val in value :
                    if val not in values : values.append(val) 
            else :
                if value not in values : values.append(value) 

            attribute_list[attr_val.attribute] = values

        for attr,values in attribute_list.items():
         
            yield (attr, values)

    def get_aggregates(self,queryset,query = None,filters = None) :
        
        if filters : 
            queryset = queryset.filter(**filters)
        if query : 
            queryset = queryset.filter(query)   
        ctx = {}
        ctx['ready_to_ship']  =   queryset.filter(is_ready_to_ship = True).count()
        ctx['free_delivery'] = queryset.filter(is_free_delivery  = True).count()

        aggregates = queryset.aggregate(
            min_price_info=Min("price"), 
            max_price_info=Max("price"),
        ) 
        
        ctx.update(aggregates)
        return   ctx

    def get_queryset(self, validated_data):
        queryset, query, filters = Product.objects.all(), Q(), {}
        data = validated_data
        q = data.get('q')
        min_price = data.get("min_price")
        max_price = data.get("max_price")
        ready_to_ship = data.get("ready_to_ship")
        free_delivery = data.get("available-on_preorder")
        cat = data.get("cat")
        gender = data.get('g')
        

        if gender :
            gender = gender.lower()
            if gender.lower() in ['men','women','unisex'] :
             
                query.add(Q(gender__iexact=gender), Q.AND)

        if q:
            query.add(Q(title__icontains=q), Q.AND)
 
        if free_delivery :
            filters["is_free_delivery"] = free_delivery

        if ready_to_ship :
            filters["is_ready_to_ship"] = ready_to_ship
  
        if min_price:
            filters["price__gte"] = min_price

        if max_price:
            filters["price__lte"] = max_price
    
    
        if cat:
            # category is a query param and not necessarily a filter parameter
            self.cat = cat
            query.add(Q(category__in=cat.get_descendants_and_self()), Q.AND)
            klass = cat.product_class
            if klass:
                attributes = klass.attributes.all()
                for attr in attributes:
                    value = data.get(attr.code)
                    if value:
                        filters[
                            "attribute_values__value_{}".format(
                                attr.type.lower())
                        ] = value
    
        return queryset, query, filters



    def build_client_filters(self, validated_data):
        queryset, query, filters = self.get_queryset(validated_data)
       
      
        # apply the main query excluding filters.
        # cause client filters need an unfiltered queryset
        if query:
            queryset = queryset.filter(query)
        
        #apply all filters just to take aggregate not permanently on queryset
        aggregates = self.get_aggregates(queryset,filters=filters,query=query)

        # the list of filters used which will be returned to the client
        filter_list = [param for param in validated_data.keys()
                       if param != "q"]

        validated_data.update(aggregates)
        #validated_data["category_list"] = ProductCategory.objects.exclude(is_collection = True    )
        #validated_data['collection_list'] = ProductCategory.objects.filter(is_collection = True)
        validated_data['attribute_list'] = self.get_attribute_list(queryset)
        #add currency if non existent
        validated_data['currency'] = validated_data.get("currency","USD")

        """
        build filters based on queryset and request parameters
        """
        attribute_items = {}
        cat = validated_data.get("cat")
        if cat:
            klass = cat.product_class
            if klass:
                attributes = klass.attributes.all()
                for attr in attributes:
                    value = validated_data.get(attr.code)
                    if value:
                        attribute_items[attr.code] = value

        validated_data['attribute_items'] = attribute_items
        filter_list.extend([filter for filter in attribute_items.keys() if filter not in filter_list])
        
        return validated_data, filter_list



