from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta
from myadmin.models import Staff
import random
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.apps import apps
from shop.models import ProductCategory
from PIL import Image

from django.utils.text import slugify
from decimal import Decimal

from .managers import BespokeOrderManager,ClientManager


def validate_image(image):
    """Validate image dimensions."""
    """img = Image.open(image)
    if img.width < 800 or img.height < 600:
        raise ValidationError("Image must be at least 800x600 pixels.")"""
    return True
   




class Catalogue(models.Model):
    title = models.CharField(
        max_length=255,
        help_text="Title of the catalogue item.",
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        blank=True,
        help_text="Unique URL-friendly identifier for the catalogue item.",
    )
    description_text = models.TextField(
        help_text="Detailed description of the item."
    )
    cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Base cost of the item in your currency.",
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional discounted price for the item.",
    )
    category = models.ForeignKey(
        ProductCategory,
        related_name = 'catalogue',
        on_delete=models.PROTECT,
        null = True, 
        blank = True
        )
    
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="Timestamp when the item was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        help_text="Timestamp when the item was last updated."
    )

    @property
    def thumbnail(self):
        """Retrieve the URL of the first associated image."""
        first_image = self.images.first()
        return first_image.image.url if first_image else None

    class Meta:
        verbose_name = "Catalogue Item"
        verbose_name_plural = "Catalogue Items"
        ordering = ['title']  # Default ordering by title
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['cost']),
        ]

    def save(self, *args, **kwargs):
        """Generate a slug from the title if not already set."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_final_price(self):
        """Return the discounted price if available, otherwise the base cost."""
        return self.discount_price if self.discount_price else self.cost

    def is_discounted(self):
        """Check if the item has a discounted price."""
        return bool(self.discount_price and self.discount_price < self.cost)

class CatalogueImage(models.Model):
    catalogue = models.ForeignKey(
        'Catalogue',  # Reference to the Catalogue model
        related_name='images',  # Allows accessing related images via `catalogue.images`
        on_delete=models.CASCADE,  # Deletes related images when the catalogue is deleted
    )
    image = models.ImageField(
        upload_to='catalogue_images/',  # Path to store uploaded images
        validators=[validate_image],  # Ensures uploaded images meet requirements
    )
    alt_text = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Alternative text for the image, used for accessibility.",
    )
    position = models.PositiveIntegerField(
        default=0, 
        help_text="Position of the image in the display order.",
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updates on save

    class Meta:
        verbose_name = "Catalogue Image"
        verbose_name_plural = "Catalogue Images"
        ordering = ['position']  # Orders images by their position field

    def __str__(self):
        return f"Image for {self.catalogue.title} (Position: {self.position})"





class Client(models.Model):
    """Model representing a client with contact details and status tracking."""
    
    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]


    def get_client_id():
        """Generate a unique 6-digit client ID."""
        return str(uuid.uuid4().int)[:6]



    client_id = models.CharField(
        max_length=30, default=get_client_id, blank=True, unique=True
    )
    full_name = models.CharField(max_length=50)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    
    # Addresses
    home_address = models.CharField(max_length=255, blank=True, null=True)
    office_address = models.CharField(max_length=255, blank=True, null=True)

    # Contact Information
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(
        max_length=20, blank=True, null=True, help_text="Enter in international format"
    )
    email = models.EmailField(blank=True, null=True)
    
    # Other Details
    passport = models.ImageField(
        upload_to="clients/passports", blank=True, null=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Managers
    objects = ClientManager()  # Custom manager (returns only active clients)
    all_objects = models.Manager()  # Default manager (returns all clients)

    class Meta:
        ordering = ["-date_added"]  # Default ordering by most recent clients
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        """Return a string representation of the client."""
        return self.full_name or f"Client {self.client_id}"
   
    @property
    def whatsapp_link(self):
        """Return a WhatsApp contact link if a number is provided."""
        return f"https://wa.me/{self.whatsapp_number}" if self.whatsapp_number else None

    @property
    def is_male(self):
        return self.gender == "male"

    @property
    def is_female(self):
        return self.gender == "female"

    @property
    def last_worked_with(self):
        """Return the last date the client was worked with based on their latest order."""
        last_order = self.bespoke_order.order_by("-date_created").first()
        return last_order.date_created if last_order else None

    @property
    def pending_outfit_orders(self):
        """Return the count of pending outfit orders."""
        return self.outfit_order.exclude(status_log__status="READY_FOR_DELIVERY").count()

    @property
    def pending_bespoke_orders(self):
        """Return the count of pending bespoke orders."""
        return self.bespoke_order.exclude(status_log__status="DELIVERED").count()


class Measurement(models.Model):
    # Common measurements (unisex)
    neck_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Neck Circumference")
    shoulder_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Shoulder Length")
    sleeve_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Sleeve Length")
    armhole_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Armhole Circumference")
    round_sleeves_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Round Sleeves Circumference")
    hip_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Hip Circumference")
    trouser_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Trouser Length")
    lap_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Lap Circumference")
    knee_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Knee Circumference")
    calf_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Calf Circumference")
    jacket_sleeve_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Jacket Sleeve Length")

    # Women's measurements
    shoulder_to_underbust = models.CharField(max_length=50, blank=True, null=True, verbose_name="Shoulder to Underbust")
    shoulder_to_halflength = models.CharField(max_length=50, blank=True, null=True, verbose_name="Shoulder to Halflength")
    shoulder_to_hip = models.CharField(max_length=50, blank=True, null=True, verbose_name="Shoulder to Hip")
    shoulder_to_knee = models.CharField(max_length=50, blank=True, null=True, verbose_name="Shoulder to Knee")
    bust_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bust Circumference")
    round_underbust = models.CharField(max_length=50, blank=True, null=True, verbose_name="Underbust Circumference")
    waist_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Waist Circumference")
    blouse_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Blouse Length")
    jacket_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Jacket Length")
    nipple_point_2_point_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nipple Point-to-Point Length")
    bust_point = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bust Point")
    back_depth = models.CharField(max_length=50, blank=True, null=True, verbose_name="Back Depth")
    skirt_waist_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Skirt Waist Circumference")

    short_gown_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Short Gown Length")
    long_gown_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Long Gown Length")
    short_skirt_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Short Skirt Length")
    long_skirt_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Long Skirt Length")

    # Men's measurements
    chest_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Chest Circumference")
    top_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Top Length")
    trouser_waist_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Trouser Waist Circumference")
    bottom_circumference = models.CharField(max_length=50, blank=True, null=True, verbose_name="Bottom Circumference")
    waistcoat_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Waistcoat Length")

    # Measurements for traditional outfits
    kaftan_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Kaftan Length")
    senator_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Senator Length")
    agbada_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Agbada Length")
    buba_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Buba Length")
    iro_length = models.CharField(max_length=50, blank=True, null=True, verbose_name="Iro Length")

    def __str__(self):
        return f"Measurements ID: {self.id}"

    @property
    def male_measurement_fields(self):
        """Returns the list of fields specific to the client's gender."""
        return [
            'neck_circumference', 'shoulder_length', 'chest_circumference', 'top_length', 'sleeve_length', 'armhole_circumference',
            'round_sleeves_circumference',  'trouser_waist_circumference', 'hip_circumference', 'trouser_length', 'lap_circumference',
            'knee_circumference',  'bottom_circumference', 'jacket_length', 'waistcoat_length', 'kaftan_length', 'senator_length', 'agbada_length', 'buba_length', 'calf_circumference'
        ]

    @property
    def female_measurement_fields(self):
        """Returns the list of fields specific to the client's gender."""
        return [
            'neck_circumference', 'shoulder_length',   'shoulder_to_underbust', 'shoulder_to_halflength', 'shoulder_to_hip', 'shoulder_to_knee',
            'bust_circumference',
            'round_underbust', 'waist_circumference',
            'blouse_length', 'jacket_length', 'nipple_point_2_point_length', 'bust_point', 'back_depth',
            'skirt_waist_circumference',
            'hip_circumference', 'short_gown_length', 'long_gown_length', 'short_skirt_length', 'long_skirt_length', 'trouser_length', 'lap_circumference',
            'knee_circumference', 'calf_circumference', 'sleeve_length',  'armhole_circumference', 'round_sleeves_circumference',
        ]

    class Meta:
        abstract = True

class ClientBodyMeasurement(Measurement):
    """ associates a client with his body measurement"""
    client = models.OneToOneField(
        Client, related_name='measurement', on_delete=models.PROTECT)
    """
    """

    def __str__(self):
        return f"Measurement for {self.client}"


#class BespokeOrderStaffInfoStatusLog(models.Model) :

class BespokeOrder(Measurement):
    
    # Add the custom manager to BespokeOrder
    objects = BespokeOrderManager()

    def get_order_id():
        return "SBDO" + str(uuid.uuid4().int)[:6]


    order_id = models.CharField(
        max_length=20, default=get_order_id, blank=True,null=False,unique=True,editable=False)


    client = models.ForeignKey(
        Client, related_name='bespoke_order', on_delete=models.PROTECT)
    style = models.ForeignKey(Catalogue, related_name='bespoke_order', on_delete=models.CASCADE,
                              null=True, blank=True, help_text="You can leave style blank")
    staff = models.ManyToManyField(
        Staff, related_name='bespoke_order', through='BespokeOrderStaffInfo')

    # Price breakdown
    labour_cost = models.DecimalField(max_digits=10, decimal_places=2)
    material_cost = models.DecimalField(max_digits=10, decimal_places=2)
    extra_design_cost = models.DecimalField(
        max_digits=10, default=0.00, decimal_places=2)
    advance_fee = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateField(auto_now_add=True, editable=False)
    expected_date_of_delivery = models.DateField(null=False, blank=False)

    # status
    last_status_log = models.CharField(max_length=30)

    @property
    def created_at(self):
        return self.status_log.filter(status=BespokeOrderStatusLog.ORDER_CREATED).first().date
    

    @property
    def balance_fee(self) :
        return float(self.total_cost) - float(self.advance_fee)  
    

    @property
    def is_advance_payment_made(self) :
  
        if not self.advance_fee > 0  : return True 
        return BespokeOrderStatusLog.objects.filter(
            outfit=self, 
            status=BespokeOrderStatusLog.ADVANCE_PAYMENT_MADE
            ).exists() 
    
    @property
    def is_payment_completed(self):
        return BespokeOrderStatusLog.objects.filter(
            outfit=self, 
            status=BespokeOrderStatusLog.PAYMENT_COMPLETED
            ).exists()
        
    

    def save(self, *args, **kwargs):
        # Generate a unique 8-digit order ID if it doesn't already exist
        if not self.order_id:
            self.order_id = self.get_order_id()
             

        if not self.advance_fee:
            self.advance_fee = self.get_advance_payment()
        super().save(*args, **kwargs)

    def can_staff_acceptance_commence(self):
        # Check if all requirements are met for sewing to commence
        required_statuses = {BespokeOrderStatusLog.MEASUREMENT_ACQUIRED,
                             BespokeOrderStatusLog.ADVANCE_PAYMENT_MADE}
        existing_statuses = set(
            BespokeOrderStatusLog.objects.filter(
                outfit=self,
                status__in=required_statuses
            ).values_list('status', flat=True)
        )

        return required_statuses.issubset(existing_statuses)

    def have_all_staff_accepted(self):
        """
        Checks if all staff assigned to the order have accepted via BespokeOrderStaffInfo.
        Returns True if all staff have accepted, otherwise False.
        """
        staff_info_qs = self.staff_info.all()  # Access related staff info records
        # Check if all staff have their "accepted" field set to True
        result = all(staff_info.status ==
                     "accepted" for staff_info in staff_info_qs)

        return result

    def have_all_staff_being_approved(self):
        """
        Checks if all staff assigned to the order have approved via BespokeOrderStaffInfo.
        Returns True if all staff have approved, otherwise False.
        """
        staff_info_qs = self.staff_info.all()  # Access related staff info records
        # Check if all staff have their "accepted" field set to True
        result = all(staff_info.status ==
                     "approved" for staff_info in staff_info_qs)

        return result

    def get_advance_payment(self):
        return float(self.total_cost) * 0.6

    @classmethod
    def created_in_last_week(cls, return_count=False):
        one_week_ago = timezone.now() - timedelta(days=7)
        recent_logs = BespokeOrderStatusLog.objects.filter(
            date__gte=one_week_ago)
        queryset = cls.objects.filter(id__in=recent_logs.values('outfit_id'))
        if return_count:
            return queryset.count()
        return queryset

    @classmethod
    def get_completed_bespoke_orders(cls, return_count=False):
        logs = BespokeOrderStatusLog.objects.filter(
            status=BespokeOrderStatusLog.READY_FOR_DELIVERY
        )
        # make this faster by using distict, count latter
        orders = [log.outfit for log in logs if log not in logs]
        if return_count:
            return len(orders)
        return orders

    @property
    def total_cost(self):
        return self.labour_cost + self.material_cost + self.extra_design_cost

    @property
    def advance_payment(self):
        return self.get_advance_payment()

    @property
    def status(self):
        try : 
            latest_status_log = self.status_log.order_by("-date").first()
        except :
            latest_status_log = None
        return latest_status_log 

    def __str__(self):
        return f"Order #{self.order_id} for {self.client} - Due: {self.expected_date_of_delivery}"

    def save(self, *args, **kwargs):
        self.last_status_log = self.status.status if self.status else "No status updates available."
        super().save(*args, **kwargs)



class BespokeOrderStaffInfo(models.Model):
    Delegationchoices = (
        ("tailor", "tailor"),
        ("beader", "beader"),
        ("stoner", "stoner"),
        ("embellishment", "embellishment"),  # Spelling corrected here
    )

    StatusChoices = (
        ("assigned", "assigned"),
        ("accepted", "accepted"),
        ("completed", "completed"),
        ("approved", "approved"),
        ("paid", "paid"),
    )

    order = models.ForeignKey(
        "BespokeOrder", related_name="staff_info", on_delete=models.PROTECT)
    staff = models.ForeignKey(
        Staff, related_name="bespoke_order_staff_info", on_delete=models.PROTECT)
    delegation = models.CharField(
        max_length=20, choices=Delegationchoices, default="tailor")
    # Adjusted max_digits to a more reasonable value
    pay = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    # Added default value for status
    status = models.CharField(
        max_length=20, choices=StatusChoices, default="assigned")
    date_assigned = models.DateTimeField(auto_now_add=True)
    date_accepted = models.DateTimeField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    date_approved = models.DateTimeField(blank=True, null=True)
    date_staff_is_paid = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}-{}".format(self.staff, self.delegation)

    def save(self, *args, **kwargs):
        if self.status == "accepted":
            self.date_accepted = timezone.now()
        if self.status == "completed":
            self.date_completed = timezone.now()
        if self.status == "approved":
            self.date_approved = timezone.now()
        if self.status == "paid":
            self.date_staff_is_paid = timezone.now()
        # Check if the current status is "accepted" and sewing has not yet commenced
        """if self.status == "accepted" and not BespokeOrderStatusLog.objects.filter(
            outfit=self.order, status=BespokeOrderStatusLog.ADVANCE_PAYMENT_MADE
        ).exists():
            # Verify if order processing can commence
            if not self.order.can_order_processing_commence():
                # Raise a validation error if processing requirements are not met
                raise ValidationError("Order processing requirements are not fulfilled; cannot commence sewing.")

            # Create a new status log entry for sewing commenced if requirements are met
            BespokeOrderStatusLog.objects.create(
                outfit=self.order,
                status=BespokeOrderStatusLog.SEWING_COMMENCED,
                date=timezone.now()
            )"""
        if self.status == "accepted":
            if not self.order.can_staff_acceptance_commence():
                # Raise a validation error if processing requirements are not met
                raise ValidationError(
                    "Order processing requirements are not fulfilled; cannot commence sewing.")

        super().save(*args, **kwargs)


class BespokeOrderStatusLog(models.Model):
    outfit = models.ForeignKey(
        BespokeOrder, related_name="status_log", on_delete=models.PROTECT)
    ORDER_CREATED, MEASUREMENT_ACQUIRED, ADVANCE_PAYMENT_MADE, \
        SEWING_COMMENCED, READY_FOR_DELIVERY, PAYMENT_COMPLETED, DELIVERED , CANCELLED = (
            "order created", "measurement acquired", "advance payment made",
            "sewing commenced", "ready for delivery", "payment completed", "delivered", "cancelled"
        )
    outfit_status_choices = (
        (ORDER_CREATED, "order created - wating for measurements."),
        (MEASUREMENT_ACQUIRED, "measurement acquired - waiting for a advance on payment."),
        (ADVANCE_PAYMENT_MADE,
         "advanced payment made - advance payment has been confirmed, awaiting order processing."),
        (SEWING_COMMENCED, "sewing commenced - order is been processed."),
        (READY_FOR_DELIVERY, "ready for delivery - order is ready for delivery."),
        (PAYMENT_COMPLETED, "payment completed - order payment has been completed."),
        (DELIVERED, "delivered - this order has been delivered."),
        (CANCELLED, "cancelled - this order has been cancelled.")
    )
    status = models.CharField(max_length=20, choices=outfit_status_choices)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # check make sure yoy dont crteate sewing commnced if advance has not been paid
        if self.status == BespokeOrderStatusLog.SEWING_COMMENCED:
            if not BespokeOrderStatusLog.objects.filter(status=BespokeOrderStatusLog.ADVANCE_PAYMENT_MADE,
                                                    outfit=self.outfit).exists():
                raise ValidationError("Advance payment has not been made")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.outfit.order_id} - {self.get_status_display()} on {self.date.strftime('%Y-%m-%d %H:%M')}"


class Inventory():
    pass
