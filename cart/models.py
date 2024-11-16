from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Sum
from django.utils.encoding import smart_str
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from decimal import Decimal

from core.functions import get_default_currency
from shop.models import ProductAttribute
from .managers import OpenCartManager,SavedCartManager


class Cart(models.Model):
    """
    Cart object
    """
    # Carts can be anonymously owned - hence this field is nullable.  When a
    # anon user signs in, their two carts are merged.
    owner = models.ForeignKey(
        get_user_model(),
        null=True,
        related_name='carts',
        on_delete=models.CASCADE,
        verbose_name=_("Owner"))

    # Cart statuses
    # - Frozen is for when a cart is in the process of being submitted
    #   and we need to prevent any changes to it.
    OPEN, MERGED, SAVED, FROZEN, SUBMITTED = (
        "Open", "Merged", "Saved", "Frozen", "Submitted")
    STATUS_CHOICES = (
        (OPEN, _("Open - currently active")),
        (SAVED, _("Saved - for items to be purchased later")),
        (FROZEN, _("Frozen - the cart cannot be modified")),
        (SUBMITTED, _("Submitted - has been ordered at the checkout")),
    )
    status = models.CharField(
        _("Status"), max_length=128, default=OPEN, choices=STATUS_CHOICES)

 

    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_submitted = models.DateTimeField(_("Date submitted"), null=True,
                                          blank=True)

    # Only if a cart is in one of these statuses can it be edited
    editable_statuses = (OPEN, SAVED)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    objects = models.Manager()
    open = OpenCartManager()
    saved = SavedCartManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

      
     

    def __str__(self):
        return _(
            "%(status)s cart (owner: %(owner)s") \
            % {'status': self.status,
               'owner': self.owner}





    @property
    def time_since_creation(self, test_datetime=None):
        if not test_datetime:
            test_datetime = now()
        return test_datetime - self.date_created


    @property
    def is_submitted(self):
        return self.status == self.SUBMITTED

    @property
    def can_be_edited(self):
        """
        Test if a cart can be edited
        """
        return self.status in self.editable_statuses
    
    def get_currency(self) :
        from core.models import Currency
        return Currency.objects.all().first()
    
    def get_total_amount(self) :
        return 1000



class CartLine(models.Model):
    """A line of a cart (product and a quantity)

    Common approaches on ordering cart lines:

        a) First added at top. That's the history-like approach; new items are
           added to the bottom of the list. Changing quantities doesn't impact
           position.
           Oscar does this by default. It just sorts by Line.pk, which is
           guaranteed to increment after each creation.

        b) Last modified at top. That means items move to the top when you add
           another one, and new items are added to the top as well.  Amazon
           mostly does this, but doesn't change the position when you update
           the quantity in the cart view.
           To get this behaviour, change Meta.ordering and optionally do
           something similar on wishlist lines. Order lines should already
           be created in the order of the cart lines, and are sorted by
           their primary key, so no changes should be necessary there.

    """
    cart = models.ForeignKey(
        'cart.Cart',
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name=_("Cart"))

    # This is to determine which products belong to the same line
    # We can't just use product.id as you can have customised products
    # which should be treated as separate lines.  Set as a
    # SlugField as it is included in the path for certain views.
    #line_reference = models.SlugField(
        #_("Line Reference"), max_length=128, db_index=True)

    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='cart_lines',
        verbose_name=_("Product"))


    quantity = models.PositiveIntegerField(_('Quantity'), default=1)

    # We store the unit price incl tax of the product when it is first added to
    # the cart.  This allows us to tell if a product has changed price since
    # a person first added it to their cart.
    price_currency = models.CharField(
        _("Currency"), max_length=12, default=get_default_currency
        )
    unit_price = models.DecimalField(
        _('Price '), decimal_places=2, max_digits=12,
        null=True)
  
    # Track date of first addition
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True, db_index=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   

    class Meta:
        app_label = 'cart'
        # Enforce sorting by order of creation.
        ordering = ['date_created', 'pk']
        #unique_together = ("cart", "line_reference")
        verbose_name = _('Cart line')
        verbose_name_plural = _('Cart lines')

    def __str__(self):
        return _(
            "Cart #%(cart_id)d, Product #%(product_id)d, quantity"
            " %(quantity)d") % {'cart_id': self.cart.pk,
                                'product_id': self.product.pk,
                                'quantity': self.quantity}

    def save(self, *args, **kwargs):
        if not self.cart.can_be_edited:
            raise PermissionDenied(
                _("You cannot modify a %s cart") % (
                    self.cart.status.lower(),))
        return super().save(*args, **kwargs)

    

    def get_price_breakdown(self):
        """
        Return a breakdown of line prices after discounts have been applied.

        Returns a list of (unit_price_incl_tax, unit_price_excl_tax, quantity)
        tuples.
        """

        prices = []
        prices.append((self.unit_price, self.unit_price,
                           self.quantity))
        return prices

    # =======
    # Helpers


    @property
    def line_price(self):
        if self.unit_price is not None:
            return self.quantity * self.unit_price

  
   
    @property
    def description(self):
        d = smart_str(self.product)
        ops = []
        for attribute in self.attributes.all():
            ops.append("%s = '%s'" % (attribute.option.name, attribute.value))
        if ops:
            d = "%s (%s)" % (d, ", ".join(ops))
        return d

    def get_warning(self):
        """
        Return a warning message about this cart line if one is applicable

        This could be things like the price has changed
        """
        if not self.product :
            msg = "'%(product)s' is no longer available"
            return _(msg) % {'product': self.product.get_title()}

        if not self.price:
            return
    

      

class CartLineAttribute(models.Model):
    """
    An attribute of a cart line
    """
    line = models.ForeignKey(
        CartLine,
        on_delete=models.CASCADE,
        related_name='attributes',
        verbose_name=_("Line"))
    option = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE,
        verbose_name=_("Option"))
    value = models.CharField(_("Value"), max_length=255)

    class Meta:
        app_label = 'cart'
        verbose_name = _('Line attribute')
        verbose_name_plural = _('Line attributes')
