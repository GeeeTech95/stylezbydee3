
from django.conf import settings
from django.core.signing import BadSignature, Signer
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.crypto import constant_time_compare
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.urls import reverse
from django.conf import settings
from django.contrib.auth  import  get_user_model
from core.models import Country,Currency
from shop.models import Product,ProductAttributeOption
from . import exceptions

import logging,uuid
from collections import OrderedDict
from decimal import Decimal as D
from cart.models import Cart


class ShippingDetail(models.Model) :
    user = models.ForeignKey(get_user_model(),null = True,blank=True,on_delete=models.CASCADE,related_name="shipping_detail")
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    country = models.ForeignKey(Country,related_name = "shipping",on_delete = models.CASCADE )
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=10)
    address = models.TextField()

    class Meta:
        ordering = ['pk']

        



class Order(models.Model):
    AWAITING_PAYMENT, PAID, PROCESSING, SHIPPED = (
        "Awaiting Payment", "Paid", "Processing", "Shipped")
    STATUS_CHOICES = (
        (AWAITING_PAYMENT, _("On hold - Awaiting Payment")),
        (PAID, _("Paid - to be processed")),
        (PROCESSING, _("Processing - Order is being processed")),
        (SHIPPED, _("Ready yo be shipped")),
    )

    number = models.CharField(
        _("Order number"), max_length=128, db_index=True, unique=True)
    
    shipping_info = models.ForeignKey(
        ShippingDetail,related_name = "order",on_delete = models.PROTECT
    )
    cart = models.ForeignKey(
        Cart, verbose_name=_("Cart"),
        null=True, blank=True, on_delete=models.SET_NULL)

    # Orders can be placed without the user authenticating so we don't always
    # have a customer ID.
    user = models.ForeignKey(
        get_user_model(), related_name='orders', null=True, blank=True,
        verbose_name=_("User"), on_delete=models.SET_NULL)

 
    currency =  models.ForeignKey(Currency,on_delete = models.PROTECT)
    total = models.DecimalField(
        _("Order total"), decimal_places=2, max_digits=12)
   

    # Use this field to indicate that an order is on hold / awaiting payment
    status = models.CharField(_("Status"), max_length=100,choices=STATUS_CHOICES, default=AWAITING_PAYMENT)

    # Index added to this field for reporting
    date_placed = models.DateTimeField(db_index=True)

   
 

    def set_status(self, new_status):
        """
        Set a new status for this order.

        If the requested status is not valid, then ``InvalidOrderStatus`` is
        raised.
        """
        if new_status == self.status:
            return

        old_status = self.status
        self.save()

    @property
    def chat_payment_link(self) :
        link = "https://wa.me/{}?text= i want to make payment for this order {}".format(
            settings.SITE_WHATSAPP_NO,
            settings.SITE_URL + reverse("order-detail",args=[self.number])
        )
        return link


    @property
    def is_anonymous(self):
        # It's possible for an order to be placed by a customer who then
        # deletes their profile.  Hence, we need to check that a guest email is
        # set.
        return self.user is None and bool(self.guest_email)

    @property
    def is_paid(self) :
        return self.status == self.PAID

    class Meta:
        app_label = 'order'
        ordering = ['-date_placed']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return "#%s" % (self.number,)

    def verification_hash(self):
        signer = Signer(salt='oscar.apps.order.Order')
        return signer.sign(self.number)

    def check_verification_hash(self, hash_to_check):
        """
        Checks the received verification hash against this order number.
        Returns False if the verification failed, True otherwise.
        """
        signer = Signer(salt='oscar.apps.order.Order')
        try:
            signed_number = signer.unsign(hash_to_check)
        except BadSignature:
            return False

        return constant_time_compare(signed_number, self.number)

    @property
    def email(self):
        if not self.user:
            return self.guest_email
        return self.user.email
    
    @property
    def absolute_url(self) :
        return 

   

    def set_date_placed_default(self):
        if self.date_placed is None:
            self.date_placed = now()


    def save(self, *args, **kwargs):
        # Ensure the date_placed field works as it auto_now_add was set. But
        # this gives us the ability to set the date_placed explicitly (which is
        # useful when importing orders from another system).
        self.set_date_placed_default()
        if not self.number :
            self.number = str(uuid.uuid4().int)[:8]
        super().save(*args, **kwargs)




class OrderStatusChange(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_changes',
        verbose_name=_('Order Status Changes')
    )
    old_status = models.CharField(_('Old Status'), max_length=100, blank=True)
    new_status = models.CharField(_('New Status'), max_length=100, blank=True)
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True, db_index=True)


    class Meta:
        app_label = 'order'
        verbose_name = _('Order Status Change')
        verbose_name_plural = _('Order Status Changes')
        ordering = ['-date_created']


    def __str__(self):
        return _("%(order)s has changed status from %(old_status)s to %(new_status)s") \
            % {'order': self.order, 'old_status': self.old_status, 'new_status': self.new_status, }






class OrderNote(models.Model):
    """
    A note against an order.
    This are often used for audit purposes too.  IE, whenever an admin
    makes a change to an order, we create a note to record what happened.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name=_("Order"))

    # These are sometimes programatically generated so don't need a
    # user everytime
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_("User"))

    # We allow notes to be classified although this isn't always needed
    INFO, WARNING, ERROR, SYSTEM = 'Info', 'Warning', 'Error', 'System'
    note_type = models.CharField(_("Note Type"), max_length=128, blank=True)

    message = models.TextField(_("Message"))
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True)

    # Notes can only be edited for 5 minutes after being created
    editable_lifetime = 300

    class Meta:
        app_label = 'order'
        ordering = ['-date_updated']
        verbose_name = _("Order Note")
        verbose_name_plural = _("Order Notes")

    def __str__(self):
        return "'%s' (%s)" % (self.message[0:50], self.user)

    def is_editable(self):
        if self.note_type == self.SYSTEM:
            return False
        delta = timezone.now() - self.date_updated
        return delta.seconds < self.editable_lifetime




class OrderLine(models.Model):
    """
    An order line
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name=_("Order"))

  
    # We don't want any hard links between orders and the products table so we
    # allow this link to be NULLable.
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name=_("Product"))
   
   
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)



    # Normal site price for item (without discounts)
    unit_price = models.DecimalField(
        _("Unit Price"), decimal_places=2, max_digits=12,
        blank=True, null=True)
 

 
    class Meta:
        app_label = 'order'
        # Enforce sorting in order of creation.
        ordering = ['pk']
        verbose_name = _("Order Line")
        verbose_name_plural = _("Order Lines")

    def __str__(self):
        if self.product:
            title = self.product.title
        else:
            title = _('<missing product>')
        return _("Product '%(name)s', quantity '%(qty)s'") % {
            'name': title, 'qty': self.quantity}

    def set_status(self, new_status):
        """
        Set a new status for this line

        If the requested status is not valid, then ``InvalidLineStatus`` is
        raised.
        """
        if new_status == self.status:
            return

        old_status = self.status

        if new_status not in self.available_statuses():
            raise exceptions.InvalidLineStatus(
                _("'%(new_status)s' is not a valid status (current status:"
                  " '%(status)s')")
                % {'new_status': new_status, 'status': self.status})
        self.status = new_status
        self.save()


    @property
    def description(self):
        """
        Returns a description of this line including details of any
        line attributes.
        """
        desc = self.title
        ops = []
        for attribute in self.attributes.all():
            ops.append("%s = '%s'" % (attribute.type, attribute.value))
        if ops:
            desc = "%s (%s)" % (desc, ", ".join(ops))
        return desc


    # Shipping status helpers
    @property
    def shipping_status(self):
        """
        Returns a string summary of the shipping status of this line
        """
        status_map = self.shipping_event_breakdown
        if not status_map:
            return ''

        events = []
        last_complete_event_name = None
        for event_dict in reversed(list(status_map.values())):
            if event_dict['quantity'] == self.quantity:
                events.append(event_dict['name'])
                last_complete_event_name = event_dict['name']
            else:
                events.append("%s (%d/%d items)" % (
                    event_dict['name'], event_dict['quantity'],
                    self.quantity))

        if last_complete_event_name == list(status_map.values())[0]['name']:
            return last_complete_event_name

        return ', '.join(events)


    @property
    def is_product_deleted(self):
        return self.product is None



class OrderLineAttribute(models.Model):
    """
    An attribute of a line
    """
    line = models.ForeignKey(
        OrderLine,
        on_delete=models.CASCADE,
        related_name='attributes',
        verbose_name=_("Line")
        )
    option = models.ForeignKey(
        ProductAttributeOption, null=True, on_delete=models.SET_NULL,
        related_name="line_attributes", verbose_name=_("Option"))
    type = models.CharField(_("Type"), max_length=128)
    value = models.CharField(_("Value"), max_length=255)

    class Meta:
        app_label = 'order'
        verbose_name = _("Line Attribute")
        verbose_name_plural = _("Line Attributes")

    def __str__(self):
        return "%s = %s" % (self.type, self.value)



