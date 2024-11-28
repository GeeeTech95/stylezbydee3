from .models import (
    BespokeOrder,
    BespokeOrderStaffInfo,
    BespokeOrderStatusLog,
    Client,
    Catalogue,
    Staff,
)
from django.forms import inlineformset_factory
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Submit, Column, Div
from .models import Client, ClientBodyMeasurement,CatalogueImage,Catalogue
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit
from .models import BespokeOrder, Client, Catalogue, BespokeOrderStaffInfo
from django.contrib.auth import get_user_model
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.helper import FormHelper
from django.forms.models import inlineformset_factory



from django import forms
from .models import Catalogue

class CatalogueForm(forms.ModelForm):
    """Form for creating or updating a Catalogue."""
    
    class Meta:
        model = Catalogue
        fields = ['title', 'description_text', 'cost', 'discount_price', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter catalogue title'
            }),
            'description_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter description here'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter cost'
            }),
            'discount_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter discount price'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        """Customize form fields and add more classes if necessary."""
        super().__init__(*args, **kwargs)
        
        # Example: Add custom CSS classes to any form field
        for field in self.fields.values():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'



class CatalogueImageForm(forms.ModelForm):
    """Form for creating or updating Catalogue Images."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Styling for the image field
        self.fields['image'].widget.attrs.update({
            'class': 'form-control custom-file-input',
            'id': 'id_image',
        })
        self.fields['alt_text'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter alternative text',
        })
        self.fields['position'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter display position',
        })
    class Meta:
        model = CatalogueImage
        fields = ['image', 'alt_text', 'position']
        widgets = {
            'alt_text': forms.TextInput(attrs={'placeholder': 'Image description'}),
        }


# Inline formset for CatalogueImage
CatalogueImageFormSet = inlineformset_factory(
    Catalogue,  # Parent model
    CatalogueImage,  # Related model
    form=CatalogueImageForm,
    extra=1,  # Number of empty image forms
    can_delete=False,  # Allow deletion of images
)




class ClientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # Adjust this if using a different URL name
        self.helper.form_action = 'client_form'
        self.helper.layout = Layout(
            Div(
                Row(
                    Column(Field('full_name', css_class='form-control'),
                           css_class='col-md-6'),
                    Column(Field('gender', css_class='form-control'),
                           css_class='col-md-6'),

                    css_class='row'
                ),
                Row(
                    Column(Field('home_address', css_class='form-control'),
                           css_class='col-md-6'),
                    Column(Field('office_address',
                           css_class='form-control'), css_class='col-md-6'),
                    css_class='row'
                ),
                Row(
                    Column(Field('phone_number', css_class='form-control'),
                           css_class='col-md-6'),
                    Column(Field('whatsapp_number',
                           css_class='form-control'), css_class='col-md-6'),
                    css_class='row'
                ),
                Row(
                    Column(Field('email', css_class='form-control'),
                           css_class='col-12'),

                    css_class='row'
                ),
                Row(

                    Column(Field('passport', css_class='form-control'),
                           css_class='col-12'),
                    css_class='row'
                ),
                css_class='container-fluid'
            ),

            Submit('submit', 'Submit',
                   css_class='btn bg-primary color-white w-100 waves-effect waves-light fs-18 font-w500 mt-5'),

        )

    class Meta:
        model = Client
        fields = [
            'full_name', 'gender',
            'phone_number', 'whatsapp_number', 'home_address',
            'office_address',
            'email', 'passport'
        ]


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = ClientBodyMeasurement
        exclude = ['client']  # Initially include all fields

    def __init__(self, *args, **kwargs):
        client_gender = kwargs.pop('client_gender', None)
        super(MeasurementForm, self).__init__(*args, **kwargs)

        # Configure the FormHelper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # Adjust this if using a different URL name
        self.helper.form_action = 'measurement_form'

        # Configure the layout based on gender
        if client_gender == 'male':
            field_names = self.instance.male_measurement_fields
        elif client_gender == 'female':
            field_names = self.instance.female_measurement_fields  # Changed to female fields
        else:
            # Fallback to all fields if gender is not specified
            field_names = list(self.fields.keys())

        # Dynamically build the layout with Bootstrap 4 grid system
        rows = []

        for i in range(0, len(field_names), 3):
            columns = [
                Column(field_name, css_class='col-md-4')
                for field_name in field_names[i:i + 3]
            ]
            rows.append(Row(*columns, css_class='row-fluid row'))

        layout = Layout(
            Div(
                *rows,
                css_class='container-fluid'
            ),
            Submit('submit', 'Update Measurement',
                   css_class='btn bg-primary color-white w-100 waves-effect waves-light fs-18 font-w500 mt-5'),

        )

        self.helper.layout = layout


class BespokeOrderForms(forms.ModelForm):
    """Main form for creating and updating Bespoke Orders."""

    class Meta:
        model = BespokeOrder
        fields = [
            'style', 'labour_cost', 'material_cost','advance_fee','extra_design_cost',
            # Add other fields as needed
        ]
        widgets = {
           
            'style': forms.Select(attrs={'class': 'form-control'}),
            'labour_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'advance_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'material_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'extra_design_cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        self.fields['style'].queryset = Catalogue.objects.all()


class BespokeOrderStaffInfoForm(forms.ModelForm):
    """Form for assigning tasks to staff within a bespoke order."""

    class Meta:
        model = BespokeOrderStaffInfo
        fields = ['staff', 'delegation', 'pay', 'status',
                  'date_accepted', 'date_completed', 'date_approved']
        widgets = {
            'staff': forms.Select(attrs={'class': 'form-control'}),
            'delegation': forms.Select(attrs={'class': 'form-control'}),
            'pay': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date_accepted': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'date_completed': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'date_approved': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }


class BespokeOrderStatusLogForm(forms.ModelForm):
    """Form for logging status updates for a bespoke order."""

    class Meta:
        model = BespokeOrderStatusLog
        fields = ['status',]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class BespokeOrderForm(forms.ModelForm):
    """Main form for creating and updating Bespoke Orders."""

    class Meta:
        model = BespokeOrder
        fields = [
            'style', 'labour_cost', 'advance_fee','material_cost', 'extra_design_cost',"expected_date_of_delivery"
            # Add other fields as needed
        ]
        widgets = {
         
            'style': forms.Select(attrs={'class': 'form-control'}),
            'labour_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'advance_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'material_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'extra_design_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'expected_date_of_delivery': forms.DateInput(attrs={'class': 'form-control date-picker', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['style'].queryset = Catalogue.objects.all()


class BespokeOrderStaffInfoForm(forms.ModelForm):
    """Form for assigning tasks to staff within a bespoke order."""

    class Meta:
        model = BespokeOrderStaffInfo
        fields = ['staff', 'delegation', 'pay',
                 ]
        widgets = {
            'staff': forms.Select(attrs={'class': 'form-control'}),
            'delegation': forms.Select(attrs={'class': 'form-control'}),
            'pay': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date_accepted': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'date_completed': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'date_approved': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }



# Inline formsets
BespokeOrderStaffInfoFormSet = inlineformset_factory(
    BespokeOrder, BespokeOrderStaffInfo, form=BespokeOrderStaffInfoForm, extra=0, can_delete=True
)

BespokeOrderStatusLogFormSet = inlineformset_factory(
    BespokeOrder, BespokeOrderStatusLog, form=BespokeOrderStatusLogForm, extra=0, can_delete=True
)
