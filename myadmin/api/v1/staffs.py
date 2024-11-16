from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from myadmin.models import Staff, StaffSalaryLog
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from myadmin.models import StaffTransactionLog




class CreateSalaryLogView(APIView):
    """
    API View to create salary logs for staff based on their salary cycle (weekly or monthly).
    """
    
    def post(self, request, *args, **kwargs):
        try:
            # Get the current date
            current_date = timezone.now()
            
            # Filter staff members whose salary cycle is weekly or monthly
            weekly_staff = Staff.objects.filter(salary_cycle="weekly")
            monthly_staff = Staff.objects.filter(salary_cycle="monthly")
            
            # Create logs for weekly staff
            for staff in weekly_staff:
                StaffSalaryLog.objects.create(
                    staff=staff,
                    date_due=current_date,
                    amount_due=staff.salary or 0.0,
                    is_paid=False
                )
            
            # Create logs for monthly staff
            for staff in monthly_staff:
                # Check if the log already exists for the current month
                salary_log_exists = StaffSalaryLog.objects.filter(
                    staff=staff,
                    date_due__year=current_date.year,
                    date_due__month=current_date.month
                ).exists()
                
                if not salary_log_exists:
                    StaffSalaryLog.objects.create(
                        staff=staff,
                        date_due=current_date,
                        amount_due=staff.salary or 0.0,
                        is_paid=False
                    )
            
            # Return a success response
            return Response({"message": "Salary logs created successfully!"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            # Handle any unexpected errors
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class StaffTransactionLogDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        savings_log = get_object_or_404(StaffTransactionLog, pk=pk)
        savings_log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
