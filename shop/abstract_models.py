from datetime import date, datetime
import uuid
import itertools

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language
from django.template.defaultfilters import striptags
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.core.validators import RegexValidator
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import settings
from treebeard.mp_tree import MP_Node

from core.validators import non_python_keyword
from core.loading import get_model
from core.models import Currency



class AbstractProductMedia(models.Model):

    def get_path(instance, filename):
        return "shop/products/product_{}/{}".format(instance.product.product_id, filename)

    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name="media")
    media = models.FileField(
        upload_to=get_path, blank=True, null=True, max_length=300)
    tag = models.CharField(max_length=20, null=True, blank=True)
    #: Use display_order to determine which is the "primary" image
    display_order = models.PositiveIntegerField(
        _("Display order"), default=0, db_index=True,
        help_text=_("An image with a display order of zero will be the primary"
                    "image for a product"))

    class Meta():
        abstract = True

    def __str__(self):
        try:
            return self.product.product_id
        except:
            return self.pk

    @property
    def media_url(self):
        """ if a file is missing we return default"""
        try:
            return self.media.url
        except:
            return "This file no longer exists"


class AbstractProductRecommendation(models.Model):
    """
    'Through' model for product recommendations
    """
    primary = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='primary_recommendations',
        verbose_name=_("Primary product"))
    recommendation = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        verbose_name=_("Recommended product"))
    ranking = models.PositiveSmallIntegerField(
        _('Ranking'), default=0, db_index=True,
        help_text=_('Determines order of the products. A product with a higher'
                    ' value will appear before one with a lower ranking.'))

    class Meta:
        abstract = True
        app_label = 'shop'
        ordering = ['primary', '-ranking']
        unique_together = ('primary', 'recommendation')
        verbose_name = _('Product recommendation')
        verbose_name_plural = _('Product recomendations')


class AbstractProduct(models.Model):
 
    def get_product_id():
        return str(uuid.uuid4().int)[:15]

    GENDER_CHOICES = (
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Unisex', 'Unisex'),
) 
    
    product_id = models.CharField(
        max_length=30,
        default=get_product_id,
        unique=True,
        editable=False)

 
    product_class = models.ForeignKey(
        'shop.ProductClass',
        related_name="products",
        on_delete=models.PROTECT,
        null=True,
    )

    category = models.ManyToManyField(
        'shop.ProductCategory',
        related_name="products"
    )
   
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(blank=True, null=True)

    gender = models.CharField(choices=GENDER_CHOICES,max_length = 10)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    currency = models.ForeignKey(
        Currency,
        on_delete = models.PROTECT,
        null = True
    )
    # to monitor price change,used for deals of the day
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )


    attributes = models.ManyToManyField(
        'shop.ProductAttribute',
        through='ProductAttributeValue',
        verbose_name=_("Attributes"),
        help_text=_("A product attribute is something that this product may "
                    "have, such as a size, as specified by its class"
                    ),
        related_name="products"
    )

    recommended_products = models.ManyToManyField(
        'shop.Product', through='ProductRecommendation', blank=True,
        verbose_name=_("Recommended products"),
        help_text=_("These are products that are recommended to accompany the "
                    "main product."))

    # average of all individual ratings on comfirmed purchases
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True
    )
    in_stock = models.BooleanField(default=True, blank=True)
    available_units = models.PositiveIntegerField(default=1)
    slug = models.SlugField(_('Slug'), max_length=255, blank=True)

    class Meta():
        abstract = True



    @property
    def price_change(self) :
        if not self.old_price : return 0
        #price change in percentage
        change  = self.price - self.old_price
        return int((change/self.old_price) * 100) 

    @property
    def attribute_values_as_tuple(self) :
        """
        returns a tuple of attribute and its values 
        """
        attribute_values = self.get_attribute_values()
        return  [(attr_val.attribute, attr_val.value) for attr_val in attribute_values ]   
         

    def get_attribute_values(self):
        attribute_values = self.attribute_values.all()
        return attribute_values

    def product_attribute_values(self, attribute):
        # reurns list of values/value for the attribute of a partucular product
        if isinstance(attribute, str):
            # then use lookup
            attr_values = self.attribute_values.filter(attribute__pk=attribute)
        else:
            attr_values = self.attribute_values.filter(attribute=attribute)

        if attr_values:
            # convert to actual values using the model 'value' property in a list
            # to make flatenning easier
            attr_values = list(attr_values)
            attr_values = [val.value for val in attr_values]
            # flatten list incase of multi option values
            if attribute.is_multi_option :
                attr_values = list(itertools.chain(*attr_values))
            return attr_values

    @property
    def title_verbose(self):
        return "{} {}".format(self.title, "for rent")

    @property
    def item_type(self) :
        return self.product_class.item_type    

    @property
    def attribute_summary(self):
        """
        Return a string of all of a product's attributes
        """
        attributes = self.get_attribute_values()
        pairs = [attribute.verbose for attribute in attributes]
        return ", ".join(pairs)

    @property
    def thumbnail(self):
        if self.has_media:
            return self.media.all().first().media_url
        else :
            return  

    @property
    def page_title(self):
        return "{}, for #{}.".format(self.title, self.price)
    


    @property
    def has_media(self):
        return self.media.count() > 0

    def __str__(self):
        if self.title:
            return self.title
        if self.attribute_summary:
            return "%s (%s)" % (self.get_title(), self.attribute_summary)
        else:
            return self.get_title()

    def get_title(self):
        """
        Return a product's title or it's parent's title if it has no title
        """
        title = self.title
        if not title and self.parent_id:
            title = self.parent.title
        return title

    def generate_slug(self):
        return slugify(self.title + "-{}".format(self.product_id))

  
