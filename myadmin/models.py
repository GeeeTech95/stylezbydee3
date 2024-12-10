from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.apps import apps

class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ("tailoring", "Tailoring"),
        ("designing", "Designing"),
        ("finishing", "Finishing"),
        ("administration", "Administration"),
        ("sales", "sales"),
        ("security", "Security"),
        ("logistics", "Logistics"),
        ("customer service", "Customer Service"),
        ("beading", "Beading"),
        ("assistant", "Assistant"),
        ("cleaning", "Cleaning"),
        ("kitchen", "Kitchen"),
        ("others", "Others")
    ]
    name = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return self.name


class StaffRole(models.Model):
    ROLE_CHOICES = [

        ("ceo", "Ceo"),
        ("general manager", "General manager"),
        ("recruitment manager", "Recruitment manager"),
        ("safety manager", "Safety manager"),
        ("design", "Design"),
        ("social media manager", "Social media manager"),
        ("customer service", "Customer service"),
        ("technical manager", "Technical manager"),
        ("maintenance manager", "Maintenance manager"),
        ("quality control manager", "Quality control manager"),
        ("sales repesentative", "Sales repesentative"),
        ("personal assistant to ceo", "Personal assistant to ceo"),
        ("head tailor", "Head tailor"),
        ("head beeder", "Head beeder"),
        ("head stoner", "Head stoner"),
        ("no role", "No role"),



    ]
    name = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


class Staff(models.Model):
    
    EMPLOYMENT_STATUS_CHOICES = [
        ("active", "Active"),
        ("suspended", "Suspended"),
        ("terminated", "Terminated")
    ]

    SALARY_CYCLE_CHOICES = [
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    user = models.OneToOneField(
        get_user_model(),
        related_name='staff',
        on_delete=models.PROTECT
    )
    employee_id = models.CharField(max_length=5, db_index=True)
    department = models.ManyToManyField(Department)
    role = models.ManyToManyField(StaffRole)
    date_added = models.DateTimeField(auto_now_add=True)
    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_STATUS_CHOICES,
        default='active'
    )
    date_terminated = models.DateTimeField(
        blank=True, null=True, help_text="Leave Blank if staff's contract is not being terminated")

    salary_cycle = models.CharField(
        max_length=20,
        choices=SALARY_CYCLE_CHOICES,
        default="weekly",
        help_text="The frequency of salary payment for this staff"

    )
    is_salary_fixed = models.BooleanField(
        default=True,
        verbose_name="Is This Staff Salary fixed ?",
        help_text="uncheck if it does not apply to this staff"
    )

    salary = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        blank=True,
        null=True,
        help_text="Fixed salaries are for staffs whose salary is pre-dermined for their salary cycles. "
    )

    national_id_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        help_text="NIN, for identification"

    )
    bank_account_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    bank_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="e.g UBA"
    )
    bank_account_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,

    )

    contract_type = models.CharField(
        max_length=20,
        choices=[
            ('Full-Time', 'Full-Time'),
            ('Part-Time', 'Part-Time'),
            ('Intern', 'Intern')
        ],
        default='Full-Time'
    )
    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    emergency_contact_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

   

    def get_department_display(self):
        departments = self.department.all()  # Get all related departments
        if departments.exists():
            # Comma-separated string of department names
            return ', '.join([dept.name for dept in departments])
        return "Others"

    def get_role_display(self):
        roles = self.role.all()  # Get all related departments
        if roles.exists():
            # Comma-separated string of department names
            return ', '.join([role.name for role in roles])
        return "No Role"

    def get_salary_display(self):
        if self.is_salary_fixed:
            return f"{self.salary_cycle.capitalize()}, ₦{self.salary or 0.00:,.2f}"
        else:
            return f"{self.salary_cycle.capitalize()}, Not Fixed"

    @property
    def salary_verbose(self):
        return self.get_salary_display()

    @property
    def department_verbose(self):
        return self.get_department_display()

    @property
    def role_verbose(self):
        return self.get_role_display()

    @property
    def is_salary_fixed_verbose(self):
        return "YES" if self.is_salary_fixed else "NO"

    @property
    def is_active(self):
        return self.employment_status == "active"

    def __str__(self):
        return f"{self.user.full_name} - {self.get_department_display()}"

    def get_salary_due(self):
        salary = 0.00
        if self.is_salary_fixed:
            return self.salary or 0.00
        # else caluclate the amount of work he has domne and addup all the salary
        # staff.salary if self.is_salary_fixed else self.get_salary_due
        return salary

    # Inside your Staff model
    def all_bespoke_orders(self):
        from fashion.models import BespokeOrder as BO
        orders = BO.objects.filter(staff__in=[self])
        return orders


class StaffSalaryLog(models.Model):
    
    staff = models.ForeignKey(
        Staff, related_name="salary_log", on_delete=models.CASCADE)
    #bespoke orders tied to this salary, can bu null
    bespoke_orders = models.ManyToManyField('fashion.BespokeOrder',related_name='salary_log')
    date_due = models.DateField(auto_now_add=True)
    date_paid = models.DateTimeField(blank=True, null=True)
    amount_due = models.DecimalField(decimal_places=2, max_digits=20)
    amount_paid = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    

    def save(self, *args, **kwargs):
        # Call the parent save method first to create/update the log
        super().save(*args, **kwargs)

        BespokeOrderStaffInfo = apps.get_model('fashion', 'BespokeOrderStaffInfo')
        
        # If the log is marked as paid and there are associated bespoke orders
        if self.is_paid and self.bespoke_orders.exists():
            # Iterate through all associated bespoke orders
            for order in self.bespoke_orders.all():
                # Query BespokeOrderStaffInfo for the current staff and order
                staff_infos = BespokeOrderStaffInfo.objects.filter(
                    staff=self.staff, order=order
                )
                
                if staff_infos:
                    for staff_info in staff_infos : 
                        # Update the status of BespokeOrderStaffInfo to "paid"
                        staff_info.status = 'paid'
                        staff_info.save()

    def __str__(self):
        return f"Salary Log for {self.staff.user}"


class StaffTransactionLog(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('savings', 'Savings'),
        ('withdrawal', 'Withdrawal'),
        # Add more transaction types if needed
    )

    STATUS_CHOICES = (
        ('created', 'Created'),
        ('confirmed', 'Confirmed'),

    )

    staff = models.ForeignKey(
        'Staff',
        related_name='transaction_logs',
        on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES
    )
    date_initiated = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='created')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} by {self.staff.user.full_name} on {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-date_initiated']


class StaffLoan(models.Model):
    staff = models.ForeignKey(
        Staff, related_name='loans', on_delete=models.CASCADE)
    loan_amount = models.DecimalField(decimal_places=2, max_digits=20)
    interest_rate = models.DecimalField(
        decimal_places=2, max_digits=5, default=0.0)
    loan_date = models.DateField(auto_now_add=True)
    repayment_start_date = models.DateField()
    repayment_end_date = models.DateField()
    monthly_repayment_amount = models.DecimalField(
        decimal_places=2, max_digits=20)
    total_repayment_amount = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Repaid', 'Repaid'),
        ('Defaulted', 'Defaulted')
    ], default='Pending')
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.total_repayment_amount:
            # Calculate total repayment amount based on loan amount and interest rate
            self.total_repayment_amount = self.loan_amount * \
                (1 + (self.interest_rate / 100))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Loan of {self.loan_amount} to {self.staff.user.full_name}'

    class Meta:
        verbose_name = 'Staff Loan'
        verbose_name_plural = 'Staff Loans'


class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity_available = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.0)

    def __str__(self):
        return self.name


class FoodRequest(models.Model):
    staff = models.ForeignKey(
        Staff, related_name='food_requests', on_delete=models.CASCADE)
    food_item = models.ForeignKey(
        FoodItem, related_name='requests', on_delete=models.PROTECT)
    quantity_requested = models.PositiveIntegerField()
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Fulfilled', 'Fulfilled'),
        ('Rejected', 'Rejected')
    ], default='Pending')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.staff.user.full_name} - {self.food_item.name} ({self.quantity_requested})'

    class Meta:
        verbose_name = 'Food Request'
        verbose_name_plural = 'Food Requests'
