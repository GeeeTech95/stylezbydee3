from datetime import date, datetime
from logging import root
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language
from django.template.defaultfilters import striptags
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.core.validators import RegexValidator
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.urls import reverse
from treebeard.mp_tree import MP_Node

from core.validators import non_python_keyword
from core.loading import get_model


from .managers import CategoryQuerySet





class AbstractCategory(MP_Node):

    """
    A product category. Merely used for navigational purposes; has no
    effects on business logic.

    Uses :py:mod:`django-treebeard`.
    """
    #: Allow comparison of categories on a limited number of fields by ranges.
    #: When the Category model is overwritten to provide CMS content, defining
    #: this avoids fetching a lot of unneeded extra data from the database.
    COMPARISON_FIELDS = ('pk', 'path', 'depth')

    name = models.CharField(_('Name'), max_length=255, db_index=True)
    _name_verbose = models.CharField(
        _('verbose name'), max_length=255, null=True, blank=False)
    description = models.TextField(_('Description'), blank=True)
    slug = models.SlugField(blank=True, max_length=100)
    meta_title = models.CharField(
        _('Meta title'), max_length=255, blank=True, null=True)
    meta_description = models.TextField(
        _('Meta description'), blank=True, null=True)

    is_public = models.BooleanField(
        _('Is public'),
        default=True,
        db_index=True,
        help_text=_("Show this category in search results listings."))

    ancestors_are_public = models.BooleanField(
        _('Ancestor categories are public'),
        default=True,
        db_index=True,
        help_text=_("The ancestors of this category are public"))

    _slug_separator = '/'
    _full_name_separator = ' > '

    objects = CategoryQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ['path']

    def __str__(self):
        return self.name

    @property
    def name_verbose(self):
        return self._name_verbose or self.name

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return ""

    @property
    def full_name(self):
        """
        Returns a string representation of the category and it's ancestors,
        e.g. 'Books > Non-fiction > Essential programming'.

        used to be stored as a CharField and is
        hence kept for backwards compatibility. It's also sufficiently useful
        to keep around.
        """
        names = [category.name for category in self.get_ancestors_and_self()]
        return self._full_name_separator.join(names)

    def get_full_slug(self, parent_slug=None):
        if self.is_root():
            return self.slug

        parent_slug = parent_slug if parent_slug is not None else self.get_parent().full_slug
        full_slug = "%s%s%s" % (parent_slug, self._slug_separator, self.slug)
        return full_slug

    @property
    def full_slug(self):
        """
        Returns a string of this category's slug concatenated with the slugs
        of it's ancestors, e.g. 'books/non-fiction/essential-programming'.

        Oused to store this as in the 'slug' model field, but this field
        has been re-purposed to only store this category's slug and to not
        include it's ancestors' slugs.
        """
        return self.get_full_slug()

    def generate_slug(self):
        """
        Generates a slug for a category. This makes no attempt at generating
        a unique slug.
        """
        if self.pk:
            name = "{} {}".format(self.name_verbose, self.pk)
            return slugify(name)
        return slugify(self.name_verbose)

    def save(self, *args, **kwargs):
        """
        auto-generated slugs from names. As that is
        often convenient, we still do so if a slug is not supplied through
        other means. If you want to control slug creation, just create
        instances with a slug already set, or expose a field on the
        appropriate forms.
        """
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def get_meta_title(self):
        return self.meta_title or self.name

    def get_meta_description(self):
        return self.meta_description or striptags(self.description)

    def get_ancestors_and_self(self):
        """
        Gets ancestors and includes itself. Use treebeard's get_ancestors
        if you don't want to include the category itself. It's a separate
        function as it's commonly used in templates.
        """
        if self.is_root():
            return [self]

        return list(self.get_ancestors()) + [self]

    def get_descendants_and_self(self):
        """
        Gets descendants and includes itself. Use treebeard's get_descendants
        if you don't want to include the category itself. It's a separate
        function as it's commonly used in templates.
        """
        return self.get_tree(self)

    def _get_absolute_url(self, parent_slug=None):
        """
        Our URL scheme means we have to look up the category's ancestors. As
        that is a bit more expensive, we cache the generated URL. That is
        safe even for a stale cache, as the default implementation of
        ProductCategoryView does the lookup via primary key anyway. But if
        you change that logic, you'll have to reconsider the caching
        approach.
        """
        return reverse('shop:category', kwargs={
            'category_slug': self.get_full_slug(parent_slug=parent_slug), 'pk': self.pk
        })

    def get_absolute_url(self):
        return self._get_absolute_url()

    @property
    def root(self):
        try : return self.get_root()
        except  : return 

        
    @property
    def has_children(self):
        return self.get_children_count() > 0

    @property
    def children(self):
        return self.get_children()

    @property
    def product_type(self):
        # same as product class but on the root element
        return self.root.product_class


    def get_descendants_and_self(self):
        return list(self.get_descendants()) + [self]


class AbstractClass(models.Model):
    """
    Used for defining options and attributes for a subset of products.
    E.g. Books, DVDs and Toys. A product can only belong to one product class.

    Not necessarily equivalent to top-level categories but usually will be.
    """
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(blank=True, max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['name']

    def has_related_attributes(self):
        return self.attributes.count() > 0


class AbstractAttributeOptionGroup(models.Model):
    """
    Defines a group of options that collectively may be used as an
    attribute type

    For example, Language
    """
    name = models.CharField(_('Name'),   max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    @property
    def option_summary(self):
        options = [o.option for o in self.options.all()]
        return ", ".join(options)

    @property
    def option_values(self):
        return [o.option for o in self.options.all()]


class AbstractAttributeOption(models.Model):
    """
    Provides an option within an option group for an attribute type
    Examples: In a Language group, English, Greek, French
    """

    option = models.CharField(_('Option'), max_length=255)
    #optional image field for optiona that comes with images
    img  = models.FileField(upload_to="option_images",blank = True, null=True)

    def __str__(self):
        return self.option
    

    @property
    def img_src(self) :
        return self.img.url

    @property
    def slug(self) :
        return slugify(self.option)

    class Meta:
        abstract = True


class AbstractAttributeValue(models.Model):

    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_integer = models.IntegerField(
        _('Integer'), blank=True, null=True, db_index=True)
    value_boolean = models.BooleanField(
        _('Boolean'), blank=True, null=True, db_index=True)
    value_float = models.FloatField(
        _('Float'), blank=True, null=True, db_index=True)
    value_richtext = models.TextField(_('Richtext'), blank=True, null=True)
    value_date = models.DateField(
        _('Date'), blank=True, null=True, db_index=True)
    value_datetime = models.DateTimeField(
        _('DateTime'), blank=True, null=True, db_index=True)

    class Meta:
        abstract = True

    def _get_value(self):
        value = getattr(self, 'value_%s' % self.attribute.type)
        if hasattr(value, 'all'):
            value = value.all()
        return value

    def _set_value(self, new_value):
        attr_name = 'value_%s' % self.attribute.type

        if self.attribute.is_option and isinstance(new_value, str):
            # Need to look up instance of AttributeOption
            new_value = self.attribute.option_group.options.get(
                option=new_value)

        elif self.attribute.is_multi_option:
            getattr(self, attr_name).set(new_value)
            return

        setattr(self, attr_name, new_value)
        return

    def _save_value(self, new_value):
        attr_name = 'value_{}'.format(self.attribute.type)
        option_model = get_model("shop", "ProductAttributeOption")

        if self.attribute.is_option and isinstance(new_value, option_model):
            # is_option accepts just one value
            self.value_option = new_value

        elif self.attribute.is_multi_option:

            self.value_multi_option.add(*new_value)
            return

        else:
            setattr(self, attr_name, new_value)

        self.save()

    def save_value(self, values):
        # values must be an iterable to accomodate for multioptions
        if self.attribute.is_multi_option:
            self._save_value(values)
        else:
            self._save_value(values[0])

    value = property(_get_value, _set_value)

    def __str__(self):
        return self.verbose

    @property
    def verbose(self):
        """
        Gets a string representation of both the attribute and it's value,
        used e.g in product summaries.
        """
        return "{}: {}".format(self.attribute.name, self.value_as_text)

    @property
    def value_as_text(self):
        """
        Returns a string representation of the attribute's value. To customise
        e.g. image attribute values, declare a _image_as_text property and
        return something appropriate.
        """
        property_name = '_%s_as_text' % self.attribute.type
        return getattr(self, property_name, self.value)

    @property
    def _multi_option_as_text(self):
        return ', '.join(str(option) for option in self.value_multi_option.all())

    @property
    def _option_as_text(self):
        return str(self.value_option)

    @property
    def _richtext_as_text(self):
        return strip_tags(self.value)

    @property
    def _entity_as_text(self):
        """
        Returns the unicode representation of the related model. You likely
        want to customise this (and maybe _entity_as_html) if you use entities.
        """
        return str(self.value)

    @property
    def value_as_html(self):
        """
        Returns a HTML representation of the attribute's value. To customise
        e.g. image attribute values, declare a ``_image_as_html`` property and
        return e.g. an ``<img>`` tag.  Defaults to the ``_as_text``
        representation.
        """
        property_name = '_%s_as_html' % self.attribute.type
        return getattr(self, property_name, self.value_as_text)

    @property
    def _richtext_as_html(self):
        return mark_safe(self.value)

    @property
    def value_as_tuple(self):
        value = self.value_as_text
        return (self.attribute.name, value)


class AbstractAttribute(models.Model):
    # Attribute types
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    RICHTEXT = "richtext"
    DATE = "date"
    DATETIME = "datetime"
    OPTION = "option"
    MULTI_OPTION = "multi_option"
    ENTITY = "entity"

    TYPE_CHOICES = (
        (TEXT, _("Text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("True / False")),
        (FLOAT, _("Float")),
        (RICHTEXT, _("Rich Text")),
        (DATE, _("Date")),
        (DATETIME, _("Datetime")),
        (OPTION, _("Option")),
        (MULTI_OPTION, _("Multi Option")),
        (ENTITY, _("Entity")),

    )

    name = models.CharField(_('Name'), max_length=128)
    code = models.SlugField(
        _('Code'), max_length=128,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z_][0-9a-zA-Z_]*$',
                message=_(
                    "Code can only contain the letters a-z, A-Z, digits, "
                    "and underscores, and can't start with a digit.")),
            non_python_keyword
        ])

    type = models.CharField(
        choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],
        max_length=20, verbose_name=_("Type")
    )

    required = models.BooleanField(_('Required'), default=False)

    class Meta:
        abstract = True
        ordering = ['code']

    @property
    def is_option(self):
        return self.type == self.OPTION

    @property
    def is_multi_option(self):
        return self.type == self.MULTI_OPTION

    def __str__(self):
        return self.name

    def clean(self):
        if self.type == self.BOOLEAN and self.required:
            raise ValidationError(
                _("Boolean attribute should not be required."))

    def _save_multi_option(self, value_obj, value):
        # ManyToMany fields are handled separately
        if value is None:
            value_obj.delete()
            return
        try:
            count = value.count()
        except (AttributeError, TypeError):
            count = len(value)
        if count == 0:
            value_obj.delete()
        else:
            value_obj.value = value
            value_obj.save()

    def _save_value(self, value_obj, value):
        if value is None or value == '':
            value_obj.delete()
            return
        if value != value_obj.value:
            value_obj.value = value
            value_obj.save()

    def save_value(self, product, value):   # noqa: C901 too complex
        ProductAttributeValue = get_model('shop', 'ProductAttributeValue')
        try:
            value_obj = product.attribute_values.get(attribute=self)
        except ProductAttributeValue.DoesNotExist:
            # FileField uses False for announcing deletion of the file
            # not creating a new value
            delete_file = self.is_file and value is False
            if value is None or value == '' or delete_file:
                return
            value_obj = ProductAttributeValue.objects.create(
                product=product, attribute=self)

        if self.is_file:
            self._save_file(value_obj, value)
        elif self.is_multi_option:
            self._save_multi_option(value_obj, value)
        else:
            self._save_value(value_obj, value)

    def validate_value(self, value):
        validator = getattr(self, '_validate_%s' % self.type)
        validator(value)

    # Validators
    def _validate_text(self, value):
        if not isinstance(value, str):
            raise ValidationError(_("Must be str"))

    _validate_richtext = _validate_text

    def _validate_float(self, value):
        try:
            float(value)
        except ValueError:
            raise ValidationError(_("Must be a float"))

    def _validate_integer(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError(_("Must be an integer"))

    def _validate_date(self, value):
        if not (isinstance(value, datetime) or isinstance(value, date)):
            raise ValidationError(_("Must be a date or datetime"))

    def _validate_datetime(self, value):
        if not isinstance(value, datetime):
            raise ValidationError(_("Must be a datetime"))

    def _validate_boolean(self, value):
        if not type(value) == bool:
            raise ValidationError(_("Must be a boolean"))

    def _validate_entity(self, value):
        if not isinstance(value, models.Model):
            raise ValidationError(_("Must be a model instance"))

    def _validate_multi_option(self, value):
        try:
            values = iter(value)
        except TypeError:
            raise ValidationError(
                _("Must be a list or AttributeOption queryset"))
        # Validate each value as if it were an option
        # Pass in valid_values so that the DB isn't hit multiple times per iteration
        valid_values = self.option_group.options.values_list(
            'option', flat=True)
        for value in values:
            self._validate_option(value, valid_values=valid_values)

    def _validate_option(self, value, valid_values=None):
        if not isinstance(value, get_model('shop', 'AttributeOption')):
            raise ValidationError(
                _("Must be an AttributeOption model object instance"))
        if not value.pk:
            raise ValidationError(_("AttributeOption has not been saved yet"))
        if valid_values is None:
            valid_values = self.option_group.options.values_list(
                'option', flat=True)
        if value.option not in valid_values:
            raise ValidationError(
                _("%(enum)s is not a valid choice for %(attr)s") %
                {'enum': value, 'attr': self})
