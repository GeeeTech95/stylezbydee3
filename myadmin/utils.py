from .models import StaffSalaryLog,Staff
from django.utils import timezone

from datetime import datetime, timedelta
from django.utils import timezone

from fashion.models import  BespokeOrder, BespokeOrderStaffInfo,BespokeOrderStatusLog

from django.db.models import Count,Max,Sum
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from collections import defaultdict




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
        """
        Generate salary logs for all staff members based on their salary cycle.
        - Monthly: Create logs due on the 25th of the month or the next unpaid cycle.
        - Weekly: Summarize weekly pay from completed BespokeOrders and create logs.

        Handles duplicate logs by ensuring no redundant unpaid logs exist.
        """
        # Get today's date and the current day of the week
        today = timezone.now().date()
        weekday = today.weekday()  # Monday = 0, Sunday = 6
        is_saturday = weekday == 5  # Check if today is Saturday for weekly logs

        # Retrieve all staff members
        staffs = Staff.objects.all()

        # Process each staff member
        for staff in staffs:
            # Handle monthly salary cycle
            if staff.salary_cycle == 'monthly':
                # Retrieve the last paid salary log for the staff
                last_paid_salary_log = StaffSalaryLog.objects.filter(staff=staff, is_paid=True).last()

                if last_paid_salary_log:
                    # Determine the next salary due date (25th of the next month)
                    last_log_date = last_paid_salary_log.date_due
                    next_month = 1 if last_log_date.month == 12 else last_log_date.month + 1
                    next_year = last_log_date.year + 1 if last_log_date.month == 12 else last_log_date.year
                    date_due = datetime(next_year, next_month, 25).date()
                else:
                    # If no previous logs, set the due date as the 25th of the current month
                    date_due = datetime(today.year, today.month, 25).date()

                # Check if an unpaid log for the same date already exists
                existing_log = StaffSalaryLog.objects.filter(staff=staff, is_paid=False, date_due=date_due).exists()
                if existing_log:
                    # Skip creation if an unpaid log already exists
                    continue

                # Remove any outdated unpaid logs
                StaffSalaryLog.objects.filter(staff=staff, is_paid=False, date_due__lt=date_due).delete()

                # Create a new salary log for the monthly salary
                StaffSalaryLog.objects.create(
                    staff=staff,
                    amount_due=staff.salary,  # Use the staff's monthly salary
                    date_due=date_due,
                    is_paid=False  # Mark as unpaid initially
                )

            # Handle weekly salary cycle
            elif staff.salary_cycle == 'weekly':
                # Determine the start and end dates of the current week (Monday to Sunday)
                start_of_week = today - timedelta(days=weekday)
                end_of_week = start_of_week + timedelta(days=6)

                # Retrieve approved BespokeOrders for the current week
                approved_orders_staff_infos = BespokeOrderStaffInfo.objects.filter(
                    staff=staff,
                    status='approved',
                    date_staff_is_paid__isnull=True,  # Ensure the orders are unpaid
                    date_approved__range=[start_of_week, end_of_week]  # Approved this week
                ).distinct()

                # Calculate the total weekly salary due from approved orders
                weekly_salary_due = approved_orders_staff_infos.aggregate(total_pay=Sum('pay'))['total_pay'] or 0

                # Only proceed if there's a valid weekly salary due
                if weekly_salary_due > 0:
                    # Check for existing unpaid logs for the current week
                    existing_weekly_log = StaffSalaryLog.objects.filter(
                        staff=staff,
                        is_paid=False,
                        date_due__range=[start_of_week, end_of_week]
                    ).exists()

                    if not existing_weekly_log:
                        # Create a new salary log for the weekly earnings
                        log = StaffSalaryLog.objects.create(
                            staff=staff,
                            amount_due=weekly_salary_due,
                            date_due=today,  # Set today's date as the due date
                            is_paid=False  # Mark as unpaid initially
                        )
                        # Link the related BespokeOrders to the salary log
                        log.bespoke_orders.add(*approved_orders_staff_infos.values_list('order', flat=True))





class Charts :

    def bespoke_order_chart_view():
        # Get the past calendar year's date range
        today = datetime.today()
        last_year = today - timedelta(days=365)

        # Get the latest status log entry for each order within the last year
        latest_logs = (
            BespokeOrderStatusLog.objects.filter(date__gte=last_year)
            .annotate(latest_log_date=Max('date'))  # Ensure we consider the latest log for each order
            .values('outfit', 'status', 'latest_log_date')
        )

        # Extract orders grouped by month and status
        orders = (
            latest_logs.annotate(month=TruncMonth('latest_log_date'))
            .values('month', 'status')
            .annotate(count=Count('outfit'))
            .order_by('month')
            #.distinct('outfit') 
        )

        # Prepare data for chart
        data = defaultdict(lambda: defaultdict(int))
        for order in orders:
            month = order['month'].strftime('%b')  # Format month as 'Jan', 'Feb', etc.
            status = order['status']
            count = order['count']
            data[month][status] = count

        # Get all months for the past year
        months = [(last_year + timedelta(days=i)).strftime('%b') for i in range(0, 366, 30)]

        # Build series data for ApexCharts
        status_labels = {
            "Delivered" : BespokeOrderStatusLog.DELIVERED,
            "Ready to be Delivered" : BespokeOrderStatusLog.READY_FOR_DELIVERY,
            "In Progress" : BespokeOrderStatusLog.SEWING_COMMENCED
            }
        
        series = [
            {
                "name": status_label,
                "data": [data[month].get(status_label.lower(), 0) for month in months],
            }
            for status_label in status_labels
        ]

        # Pass series and categories to the template
        context = {
            "bespoke_chart_series": series,
            "bespoke_chart_categories": months,
        }
        print(context)

        return context
        
