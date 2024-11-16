from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, HTML
from .models import Staff, StaffTransactionLog,Department, StaffRole,StaffSalaryLog
from django.contrib.auth import get_user_model






User = get_user_model()

class StaffForm(forms.ModelForm):
    user_id = forms.CharField(required=True, label="User ID", help_text="Enter the unique account ID of the user")

    class Meta:
        model = Staff
        fields = [
            'user_id', 'employee_id', 'department', 'role', 'employment_status', 'date_terminated', 'is_salary_fixed', 
            'salary', 'salary_cycle', 'national_id_number', 'bank_account_number', 
            'bank_name', 'bank_account_name', 'contract_type', 
            'emergency_contact_name', 'emergency_contact_phone'
        ]
        widgets = {
            'date_terminated': forms.DateInput(attrs={'type': 'date'}),
            'salary': forms.NumberInput(attrs={'step': '0.01'}),
            'employment_status': forms.Select(choices=Staff.EMPLOYMENT_STATUS_CHOICES),
            'role': forms.Select(),  # Assuming role is a ForeignKey to StaffRole
        }

    department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),  # Assuming you have a Department model
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes to select multiple departments
        required=True,
        label="Department(s)"
    )
    
    role = forms.ModelMultipleChoiceField(
        queryset=StaffRole.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Roles",
        help_text="Select roles assigned to the staff member."
    )

    def __init__(self, *args, **kwargs):

        # Check if an instance is provided to determine if it's an edit operation
        self.instance = kwargs.get('instance', None)
        super(StaffForm, self).__init__(*args, **kwargs)

        # If instance is provided (indicating an edit operation), set user_id to not required
        if self.instance and self.instance.pk:
            self.fields['user_id'].required = False
        else :
            #edit fields 
            self.fields.pop('date_terminated')  
            self.fields.pop('employment_status')
            
 
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''  # Replace with your view name or URL pattern name
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'

        self.helper.layout = Layout(
            Row(
                Column(Field('user_id'), css_class='form-group'),
                Column(Field('employee_id'), css_class='form-group'),
                css_class='form-row'
            ),
            Row(
                Column(Field('department'), css_class='form-group'),  # Updated for multiple departments
                Column(Field('role'), css_class='form-group'),
                css_class='form-row'
            ),
            Row(
                Column(Field('employment_status'), css_class='form-group'),
                Column(Field('date_terminated'), css_class='form-group'),
                css_class='form-row'
            ),
            Row(
                Column(Field('is_salary_fixed'), css_class='form-group'),
                Column(Field('salary'), css_class='form-group'),
                css_class='form-row'
            ),
            Row(
                Column(Field('salary_cycle'), css_class='form-group'),
                Column(Field('national_id_number'), css_class='form-group'),
                css_class='form-row'
            ),
            Row(
                Column(Field('bank_account_number'), css_class='form-group'),
                Column(Field('bank_name'), css_class='form-group'),
                css_class='form-row'
            ),
            Row(
                Column(Field('bank_account_name'), css_class='form-group'),
                Column(Field('contract_type'), css_class='form-group'),
                css_class='form-row'
            ),
            Row(
                Column(Field('emergency_contact_name'), css_class='form-group'),
                Column(Field('emergency_contact_phone'), css_class='form-group'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit', css_class='btn bg-primary color-white w-100 waves-effect waves-light fs-18 font-w500 mt-5'),
        )

    def clean(self):
        cleaned_data = super().clean()
        is_salary_fixed = cleaned_data.get('is_salary_fixed')
        salary = cleaned_data.get('salary')
        
        # Check if salary is fixed and salary is not provided
        if is_salary_fixed and not salary:
            raise forms.ValidationError("Salary must be entered if it is fixed.")
    

    def save(self, commit=True):
        staff = super(StaffForm, self).save(commit=False)
        user_id = self.cleaned_data.get('user_id')

        # Attempt to get the user; handle the case where the user does not exist
        try:
            if self.instance and self.instance.pk:  # Check if editing
                # If editing, don't set user; assume it is already set
                pass
            else:
                staff.user = User.objects.get(account_id=user_id)
        except User.DoesNotExist:
            raise forms.ValidationError(f"No user found with User ID: {user_id}")

        if commit:
            staff.save()
            self.save_m2m()  # Save many-to-many relationships
            # Save M2M relationships
            #staff.department.set(self.cleaned_data['department'])
            #staff.role.set(self.cleaned_data['role'])
            staff.user.user_type = 'staff'  # Set user_type to 'staff'
            staff.user.save()  # Save user to update user_type
        return staff


class StaffTransactionLogForm(forms.ModelForm):
    class Meta:
        model = StaffTransactionLog
        fields = ['transaction_type', 'amount',  'notes','status']

    def __init__(self, *args, **kwargs):
        super(StaffTransactionLogForm,self).__init__(*args, **kwargs)
        
        # Initialize crispy form helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'row g-3'  # Bootstrap row for grid system

        # Define the layout
        self.helper.layout = Layout(
            Row(
                Column(Field('transaction_type', css_class='form-select'), css_class='col-md-6'),
                Column(Field('amount', css_class='form-control'), css_class='col-md-6'),
            ),
            Row(
                Column(Field('status', css_class='form-control'), css_class='col-md-6'),
                Column(Field('notes', css_class='form-control', rows="3"), css_class='col-md-6'),
            ),
            HTML("<hr>"),  # Horizontal line for visual separation
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )






class StaffSalaryLogForm(forms.ModelForm):
    class Meta:
        model = StaffSalaryLog
        fields = ['staff', 'amount_due', 'amount_paid', 'is_paid', 'date_paid']

    # Optional custom validations or form logic
    def clean(self):
        cleaned_data = super().clean()
        amount_due = cleaned_data.get('amount_due')
        amount_paid = cleaned_data.get('amount_paid')

        if amount_paid is not None and amount_paid > amount_due:
            raise forms.ValidationError('Amount paid cannot be more than amount due.')
        return cleaned_data
