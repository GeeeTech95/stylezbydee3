from django.contrib import admin
from .models import Department, StaffRole, Staff, StaffSalaryLog, StaffTransactionLog, StaffLoan, FoodItem, FoodRequest

from fashion.models import Client



@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'client_id', 'gender', 'phone_number', 'email', 'date_added')
    search_fields = ['full_name', 'client_id', 'email', 'phone_number']
    list_filter = ('gender',)
    ordering = ['date_added']
    readonly_fields = ('client_id', 'date_added')  # Making certain fields read-only

    fieldsets = (
        (None, {
            'fields': ('full_name', 'gender', 'phone_number', 'email')
        }),
        ('Address Information', {
            'fields': ('home_address', 'office_address'),
            'classes': ('collapse',),  # Collapsible section
        }),
        ('Contact Information', {
            'fields': ('whatsapp_number', 'passport'),
        }),
        ('Additional Info', {
            'fields': ('client_id', 'date_added'),
            'classes': ('collapse',),  # Collapsible section
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing an existing object
            return self.readonly_fields + ('whatsapp_link',)
        return self.readonly_fields



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)



class StaffAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'employee_id', 'get_departments', 'get_roles', 
        'employment_status', 'salary_cycle', 'is_salary_fixed_verbose', 'salary',
        'national_id_number', 'bank_account_name', 'bank_name', 'date_added'
    )
    list_filter = ('employment_status', 'salary_cycle', 'is_salary_fixed', 'department', 'role')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id', 'national_id_number')
    readonly_fields = ('date_added',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'employee_id', 'department', 'role', 'employment_status', 'date_terminated')
        }),
        ('Salary Information', {
            'fields': ('salary_cycle', 'is_salary_fixed', 'salary')
        }),
        ('Bank Details', {
            'fields': ('national_id_number', 'bank_account_name', 'bank_name', 'bank_account_number')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Other', {
            'fields': ('contract_type', 'date_added')
        }),
    )
    
    def get_departments(self, obj):
        return ", ".join([d.name for d in obj.department.all()])
    get_departments.short_description = 'Departments'

    def get_roles(self, obj):
        return ", ".join([r.name for r in obj.role.all()])
    get_roles.short_description = 'Roles'

admin.site.register(Staff, StaffAdmin)

@admin.register(StaffSalaryLog)
class StaffSalaryLogAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date_due', 'date_paid', 'amount_due', 'amount_paid', 'is_paid')
    list_filter = ('is_paid', 'date_due')
    search_fields = ('staff__user__username', 'staff__employee_id')
    readonly_fields = ('date_due',)


@admin.register(StaffTransactionLog)
class StaffTransactionLogAdmin(admin.ModelAdmin):
    list_display = ('staff', 'transaction_type', 'date_initiated', 'amount', 'status')
    list_filter = ('transaction_type', 'status')
    search_fields = ('staff__user__username', 'staff__employee_id')
    readonly_fields = ('date_initiated',)


@admin.register(StaffLoan)
class StaffLoanAdmin(admin.ModelAdmin):
    list_display = ('staff', 'loan_amount', 'interest_rate', 'loan_date', 'repayment_start_date', 'repayment_end_date', 'status')
    list_filter = ('status', 'loan_date', 'repayment_start_date')
    search_fields = ('staff__user__username', 'staff__employee_id')
    readonly_fields = ('loan_date', 'total_repayment_amount')


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity_available', 'price_per_unit')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(FoodRequest)
class FoodRequestAdmin(admin.ModelAdmin):
    list_display = ('staff', 'food_item', 'quantity_requested', 'request_date', 'status')
    list_filter = ('status', 'request_date')
    search_fields = ('staff__user__username', 'food_item__name')
    readonly_fields = ('request_date',)
