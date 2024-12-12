from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm




class UserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['full_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # Crispy Forms Helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        # Layout configuration
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                Column('gender', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('date_of_birth', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('register', 'Register')
        )





class UserUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()  # Using the custom user model
        fields = ['full_name', 'phone_number', 'gender', 'display_picture']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        # Crispy Forms Helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'

        

        # Layout configuration
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group '),
                Column('phone_number', css_class='form-group '),
            ),
            Row(
                Column('gender', css_class='form-group '),
            ),
            Row(
                Column('display_picture', css_class='form-group '),
            ),
             Submit(
                'update', 'Update',
                css_class='btn bg-primary color-white w-100 waves-effect waves-light fs-18 font-w500 mt-5'
            ),
        )

        # Disable fields that shouldn't be updated in this form
        for field in self.fields:
            if field not in ['full_name', 'phone_number', 'gender', 'display_picture']:
                self.fields[field].disabled = True

    def clean_display_picture(self):
        display_picture = self.cleaned_data.get('display_picture')
        # You can add image validation (size, type, etc.) if needed here
        return display_picture


class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # Crispy Forms Helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'

        # Layout configuration
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('login', 'Login')
        )
