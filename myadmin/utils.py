from .models import StaffSalaryLog,Staff
from django.utils import timezone

from datetime import datetime, timedelta
from django.utils import timezone

from fashion.models import  BespokeOrder, BespokeOrderStaffInfo



class Salary :
    
    def create_salary_logsx(self):
        # Get the current date
        current_date = timezone.now()
        
        # Filter staff members whose salary cycle is weekly or monthly
        weekly_staff = Staff.objects.filter(salary_cycle="weekly")
        monthly_staff = Staff.objects.filter(salary_cycle="monthly")
        
        # Process weekly salary logs
        for staff in weekly_staff:
            # Create a salary log marked as unpaid for weekly staff
            StaffSalaryLog.objects.create(
                staff=staff,
                date_due=current_date,
                amount_due=self.get_salary_due(),
                is_paid=False
            )
            print(f"Created weekly salary log for {staff.user.get_full_name()}")
        
        # Process monthly salary logs
        for staff in monthly_staff:
            # Check if a salary log already exists for the current month to avoid duplicates
            salary_log_exists = StaffSalaryLog.objects.filter(
                staff=staff,
                date_due__year=current_date.year,
                date_due__month=current_date.month
            ).exists()
            
            if not salary_log_exists:
                # Create a salary log marked as unpaid for monthly staff
                StaffSalaryLog.objects.create(
                    staff=staff,
                    date_due=current_date,
                    amount_due=staff.salary or 0.0,
                    is_paid=False
                )
                print(f"Created monthly salary log for {staff.user.get_full_name()}")



    def create_salary_logs():
        # Get current date and the current day of the week
        today = timezone.now().date()
        weekday = today.weekday()  # Monday = 0, Sunday = 6

        # Check if today is Saturday (for weekly earners)
        is_saturday = weekday == 5

        # Get all staff members
        staffs = Staff.objects.all()

        for staff in staffs:
            # Check if the staff is a monthly salary earner
            if staff.salary_cycle == 'monthly':
                # Get the last salary log of the staff
                last_salary_log = StaffSalaryLog.objects.filter(staff=staff,is_paid = True).last()

                if last_salary_log:
                    # If there's a previous log, set the next date_due to the 25th of the next month
                    last_log_date = last_salary_log.date_due
                    if last_log_date.month == 12:
                        next_month = 1
                        next_year = last_log_date.year + 1
                    else:
                        next_month = last_log_date.month + 1
                        next_year = last_log_date.year

                    # Set the date_due to 25th of next month
                    date_due = datetime(next_year, next_month, 25).date()

                    # Delete the old unpaid salary log
                    last_unpaid_salary_logs = StaffSalaryLog.objects.filter(
                        staff=staff, is_paid=False
                        )
                    
                    last_unpaid_salary_logs.delete()

                else:
                    # If no previous log, set the first salary log to the 25th of the current month
                    date_due = datetime(today.year, today.month, 25).date()

                # Create the new salary log for the staff
                StaffSalaryLog.objects.create(
                    staff=staff,
                    amount_due=staff.salary,  # Assuming the `salary` attribute in Staff is the monthly salary
                    date_due=date_due,
                    is_paid=False  # Set to False initially
                )

            # Check if the staff is a weekly salary earner (only if it's Saturday)
            elif staff.salary_cycle == 'weekly' : #and is_saturday:
                # Get all BespokeOrders that were marked as completed in the current week
                start_of_week = today - timedelta(days=weekday)  # Starting from Monday of the current week
                end_of_week = start_of_week + timedelta(days=6)  # Ending on Sunday

                # Get the related BespokeOrderStaffInfo for the approved orders within the current week
                approved_orders_staff_infos = BespokeOrderStaffInfo.objects.filter(
                    staff=staff,
                    status='approved',
                    date_staff_is_paid__isnull=True,  # Ensure it's unpaid
                    date_approved__range=[start_of_week, end_of_week]
                ).distinct()  # Ensure no duplicates

                # Sum up the weekly earnings from the approved orders based on the `pay` field in BespokeOrderStaffInfo
                weekly_salary_due = 0
                bespoke_orders = []
                for staff_info in approved_orders_staff_infos:
                    # Add the pay from each staff_info record
                    weekly_salary_due += staff_info.pay
                    if staff_info.order not in bespoke_orders  : 
                        bespoke_orders.append(staff_info.order) 

                # Only create a log if there's a valid weekly salary due
                if weekly_salary_due > 0:
                    # Check if an unpaid salary log already exists for this staff within the current week
                    existing_salary_log = StaffSalaryLog.objects.filter(
                        staff=staff,
                        is_paid=False,
                        date_due__range=[start_of_week, end_of_week]
                    )

                    if existing_salary_log:
                        # If an existing unpaid log is found, delete the old log
                        existing_salary_log.delete()

                    # Create a new salary log with the calculated weekly salary
                    log = StaffSalaryLog.objects.create(
                        staff=staff,
                        
                        amount_due=weekly_salary_due,
                        date_due=today,  # Set date_due as today (Saturday)
                        is_paid=False  # Set to False initially
                    )
                    #add associuated bespoke orders
                    if bespoke_orders : 
                        log.bespoke_orders.add(*bespoke_orders)