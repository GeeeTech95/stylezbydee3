from itertools import product
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.utils.safestring import mark_safe
from django.db.models import Avg
import uuid
from core.abstract_models import *
from .abstract_models import *
from .managers import ProductManager


class ProductClass(AbstractClass):

    class Meta(AbstractClass.Meta):
        verbose_name = ("Product class")
        verbose_name_plural = ("Product classes")


class ProductAttributeOption(AbstractAttributeOption):

    group = models.ForeignKey(
        'shop.ProductAttributeOptionGroup',
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name=_("Group"))

    class Meta(AbstractAttributeOption.Meta):
        app_label = 'shop'
        unique_together = ('group', 'option')
        verbose_name = _('Attribute option group')
        verbose_name_plural = _('Attribute option groups')


class ProductAttributeOptionGroup(AbstractAttributeOptionGroup):

    class Meta(AbstractAttributeOptionGroup.Meta):
        app_label = 'shop'
        verbose_name = _('Attribute option')
        verbose_name_plural = _('Attribute options')


class ProductAttribute(AbstractAttribute):
    product_class = models.ForeignKey(
        'shop.ProductClass',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="attributes",
        verbose_name="type"
    )

    option_group = models.ForeignKey(
        'shop.ProductAttributeOptionGroup',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='product_attributes',
        verbose_name=_("Option Group"),
        help_text=_('Select an option group if using type "Option" or "Multi Option"'))

    class Meta(AbstractAttribute.Meta):
        app_label = 'shop'
        verbose_name = _('Product attribute')
        verbose_name_plural = _('Product attributes')


class ProductAttributeValue(AbstractAttributeValue):
    """
    The "through" model for the m2m relationship between :py:class:`Product <.Abstract>` and
    :py:class:`ProductAttribute <.AbstractAttribute>`  This specifies the value of the attribute for
    a particular product

    For example: ``number_of_pages = 295``
    """

    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='attribute_values',
        verbose_name=_("Product")
    )

    attribute = models.ForeignKey(
        'shop.ProductAttribute',
        on_delete=models.CASCADE,
        verbose_name=_("Attribute")
    )

    value_multi_option = models.ManyToManyField(
        'shop.ProductAttributeOption', blank=True,
        related_name='multi_valued_attribute_values',
        verbose_name=_("Value multi option"))

    value_option = models.ForeignKey(
        'shop.ProductAttributeOption',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Value option"))

    class Meta(AbstractAttributeValue.Meta):
        app_label = 'shop'
        unique_together = ('attribute', 'product')
        verbose_name = _('Product attribute value')
        verbose_name_plural = _('Product attribute values')


class ProductCategory(AbstractCategory):

    def upload_to(instance, filename):
        _path = "shop/categories/{}.{}".format(
            instance.name, filename.split(".")[1])
        return _path

    image = models.ImageField(upload_to=upload_to, blank=True,
                              null=True, max_length=255)
    # special grouping for some us cases like a new collection
    product_class = models.ForeignKey(
        'shop.ProductClass',
        related_name="categories",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    #just for navigational purpose, to identify categories that are gender specific
    gender = models.CharField(
        max_length=10,
        choices=[
            ('Men', 'Men'),
            ('Women', 'Women'),
            ('Unisex', 'Unisex'),
        ],
        default='Unisex',
    )

    def get_product_recommendation(self, user):
        """ returns a set of products in this category for the user
        using cookie history or other data if authenticated"""
        return self.products.all()

    class Meta(AbstractCategory.Meta):
        app_label = 'shop'
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def save(self, *args, **kwargs):

        if not self.product_class:
            if self.root:
                self.product_class = self.root.product_class
        super(ProductCategory, self).save(*args, **kwargs)

    def navigation_crumbs(self):
        paths = []
        # add the index
        # append itself
        paths.append(self.name)
        return mark_safe(" > ".join(paths))






class ProductMedia(AbstractProductMedia):

    """
    """


class Product(AbstractProduct):

    saved_by = models.ManyToManyField(
        get_user_model(),
        related_name='product_saved',
        blank=True
    )

    is_free_delivery = models.BooleanField(default=False)
    is_ready_to_ship = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
       # specify fields to monitor
        self.__fields_to_watch_for_changes = ["price"]
        # set the old values
        for field in self.__fields_to_watch_for_changes:
            setattr(self, '__initial_{}'.format(field), getattr(self, field))

    @property
    def success_url(self):
        return self.detail_url

    @property
    def average_rating(self):
        avg_rating = self.reviews.aggregate(average_rating=Avg('rating'))
        avg_rating = avg_rating['average_rating']
        if avg_rating :
            return round(avg_rating)
        else:
            return 0
        
    @property
    def enquity_text(self) :
        return "Please i want to know about this item: {}".format(self.detail_url)    

    @property
    def related_products(self):
        queryset = Product.objects.filter(
            category__in=self.category.distinct()
        )
        queryset = queryset.exclude(pk=self.pk)
        return queryset

    @property
    def attributes_as_dict_verbose(self):
        """return the stringified version of attributes and their values"""
        attribute_dict = {}
        attributes = self.get_attribute_values()
        for attribute in attributes:
            attr, value = attribute.value_as_tuple
            values = attribute_dict.get(attr, [])
            values.append(value)
            attribute_dict[attr] = values
        return attribute_dict

    @property
    def detail_url(self):
        return reverse("product-detail", args=[self.slug])

    @property
    def absolute_url(self):
        return "{}{}".format(settings.SITE_URL, self.detail_url)

    @property
    def recommendations(self):
        """self.recommended_products.all()"""
        return Product.objects.filter(product_class=self.product_class)

    @property
    def has_attributes(self):
        return self.attributes.count() > 0

    def convert_price(self, to_currency="USD"):
        from core.functions import convert_currency
        # returns a tuple of currency html value and price
        try:
            new_price = convert_currency(
                self.price, self.currency.name, to_currency)
        except TypeError:
            return (self.currency.name, self.price)
        return (to_currency, new_price)

    objects = models.Manager()  # change later to item manager
    products = ProductManager()

    def has_changed(self, field):
        original = "__initial_{}".format(field)
        if not getattr(self, original):
            return False
        return getattr(self, original) != getattr(self, field)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()

        if self.has_changed("price"):
            self.old_price = Product.objects.get(pk=self.pk).price
        super().save(*args, **kwargs)


class ProductCollection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    banner_image = models.ImageField(upload_to='collection_banners/')
    products = models.ManyToManyField(Product, related_name='collections')
    slug = models.SlugField( max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(ProductCollection,self).save(*args,**kwargs)    


    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return self.name



class ProductSalePromotion(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('PERCENTAGE', 'Percentage'),
        ('FIXED', 'Fixed Amount'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    banner_image = models.ImageField(upload_to='promotion_banners/', null=True, blank=True)
    products = models.ManyToManyField(Product, related_name='promotions')

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def apply_discount(self, price):
        if self.discount_type == 'PERCENTAGE':
            return price * (1 - self.discount_value / 100)
        elif self.discount_type == 'FIXED':
            return max(price - self.discount_value, 0)
        return price

    def __str__(self):
        return self.name


class ProductRecommendation(AbstractProductRecommendation):
    """
    """


class ProductReview(models.Model):
    user = models.ForeignKey(get_user_model(
    ), related_name="product_reviews", on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=30)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(max_length=30)
    review = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def user_name(self):
        return self.user or self.username

    def __str__(self):
        return "{} by {}".format(self.review, self.user or self.username)
