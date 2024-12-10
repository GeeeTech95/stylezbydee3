from .models import StaffSalaryLog, Staff
from django.utils import timezone

from datetime import datetime, timedelta
from django.utils import timezone

from fashion.models import BespokeOrder, BespokeOrderStaffInfo, BespokeOrderStatusLog

from django.db.models import Count, Max, Sum
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from collections import defaultdict


class Salary:

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
            print(
                f"Created weekly salary log for {staff.user.get_full_name()}")

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
                print(
                    f"Created monthly salary log for {staff.user.get_full_name()}")


    def create_salary_logs():
        """
        Generate salary logs for all staff members based on their salary cycle.
        - Monthly: Create logs due on the 25th of the month or the next unpaid cycle.
        - Weekly: Summarize weekly pay from completed BespokeOrders and create logs.

        Handles duplicate logs by ensuring no redundant unpaid logs exist.
        """
        # Get the current time in local timezone
        today = timezone.localtime(timezone.now()).date()

        # Ensure the function runs only on the 25th of the month for monthly salary cycle
        monthly_salary_due_day = 25  # The day salaries for monthly earners should be due
        weekday = today.weekday()  # Monday = 0, Sunday = 6
        is_saturday = weekday == 5  # Check if today is Saturday for weekly logs
        
        # Retrieve all staff members
        staffs = Staff.objects.all()

        # Process each staff member
        for staff in staffs:
            # Handle monthly salary cycle
            if staff.salary_cycle == 'monthly':
                if today.day != monthly_salary_due_day:
                    continue  # Skip if today is not the 25th (for monthly earners)

                # Retrieve the last paid salary log for the staff
                last_paid_salary_log = StaffSalaryLog.objects.filter(staff=staff, is_paid=True).last()

                if last_paid_salary_log:
                    # Determine the next salary due date (25th of the next month)
                    last_log_date = last_paid_salary_log.date_due
                    next_month = 1 if last_log_date.month == 12 else last_log_date.month + 1
                    year = last_log_date.year + 1 if last_log_date.month == 12 else last_log_date.year
                    date_due = timezone.make_aware(datetime(year, next_month, monthly_salary_due_day, 0, 0))  # Normalize time to midnight

                else:
                    # If no previous logs, set the due date as the 25th of the current month
                    date_due = timezone.make_aware(datetime(today.year, today.month, monthly_salary_due_day, 0, 0))  # Normalize time to midnight

                # Ensure the date_due is only compared by date (no time comparison)
                date_due = date_due.date()

                # Check if an unpaid log for the same date already exists
                unpaid_logs = StaffSalaryLog.objects.filter(staff=staff, is_paid=False, date_due=date_due)

                if unpaid_logs.exists():
                    # Skip creation if an unpaid log already exists
                    # Remove any outdated unpaid logs
                    #unpaid_logs.delete()
                    continue
                else:
                    print('Creating monthly salary log for:', date_due)
                    # Create a new salary log for the monthly salary
                    StaffSalaryLog.objects.create(
                        staff=staff,
                        amount_due=staff.salary,  # Use the staff's monthly salary
                        date_due=date_due,  # Store date only
                        is_paid=False  # Mark as unpaid initially
                    )

            # Handle weekly salary cycle
            elif staff.salary_cycle == 'weekly':
                # Get the current date in local timezone
                today = timezone.localtime(timezone.now()).date()
                weekday = today.weekday()

                # Calculate the start and end of the week (Monday to Saturday)
                start_of_week = today - timedelta(days=weekday)  # Start of the week (Monday)
                end_of_week = start_of_week + timedelta(days=5)  # End of the week (Saturday)

                # Make start_of_week and end_of_week timezone-aware
                start_of_week = timezone.make_aware(datetime.combine(start_of_week, datetime.min.time()))
                end_of_week = timezone.make_aware(datetime.combine(end_of_week, datetime.max.time()))

                # Retrieve approved BespokeOrderStaffInfo entries for the current week
                approved_orders_staff_infos = BespokeOrderStaffInfo.objects.filter(
                    staff=staff,
                    status='approved',
                    date_staff_is_paid__isnull=True,
                    date_approved__range=[start_of_week, end_of_week]
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
                        log.bespoke_orders.add(
                            *approved_orders_staff_infos.values_list('order', flat=True)
                        )





class Charts:

    def bespoke_order_chart_view():
        # Get the past calendar year's date range
        today = datetime.today()
        last_year = today - timedelta(days=365)

        # Get the latest status log entry for each order within the last year
        latest_logs = (
            BespokeOrderStatusLog.objects.filter(date__gte=last_year)
            # Ensure we consider the latest log for each order
            .annotate(latest_log_date=Max('date'))
            .values('outfit', 'status', 'latest_log_date')
        )

        # Extract orders grouped by month and status
        orders = (
            latest_logs.annotate(month=TruncMonth('latest_log_date'))
            .values('month', 'status')
            .annotate(count=Count('outfit'))
            .order_by('month')
            # .distinct('outfit')
        )

        # Prepare data for chart
        data = defaultdict(lambda: defaultdict(int))
        for order in orders:
            # Format month as 'Jan', 'Feb', etc.
            month = order['month'].strftime('%b')
            status = order['status']
            count = order['count']
            data[month][status] = count

        # Get all months for the past year
        months = [(last_year + timedelta(days=i)).strftime('%b')
                  for i in range(0, 366, 30)]

        # Build series data for ApexCharts
        status_labels = {
            "Delivered": BespokeOrderStatusLog.DELIVERED,
            "Ready to be Delivered": BespokeOrderStatusLog.READY_FOR_DELIVERY,
            "In Progress": BespokeOrderStatusLog.SEWING_COMMENCED
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
