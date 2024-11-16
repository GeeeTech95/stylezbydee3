
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fashion.models import BespokeOrderStatusLog, BespokeOrder, BespokeOrderStaffInfo
import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from users.permissions import ActivityPermissions


class UpdateStaffBespokeOrderStatusView(UserPassesTestMixin, LoginRequiredMixin, View):
    model = BespokeOrderStaffInfo

    def test_func(self):
        return self.request.user.is_company_staff

    def get_object(self):
        try:
            info = self.model.objects.get(pk=self.kwargs['pk'])
            return info

        except self.model.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):

        try:

            data = request.POST
            new_status = data.get("new_status", "").lower()

            if new_status == "approved":
                # check if this person can approve order
                perm = ActivityPermissions(request.user)
                if  not perm.can_approve_job_delegation():
                    return JsonResponse({'success': False, "error": "You are not authorized to perform this action"})

            # Check if the new status is valid
            if new_status not in [choice[0] for choice in BespokeOrderStaffInfo.StatusChoices]:
                return JsonResponse({'success': False, "error": f"{new_status} is invalid"})

            info = self.get_object()
            if not info:
                return JsonResponse({'success': False, 'error': 'Delegation not found'})
            
            if info.staff.user != request.user  and new_status != "approved":
                return JsonResponse({'success': False, 'error': 'You are not allowed to perform this action'})
            # Update staff status
            info.status = new_status
            info.save()

            order = info.order  
            
           
            if order.have_all_staff_accepted() :
                #then create a sewing commenced
                BespokeOrderStatusLog.objects.get_or_create(
                    outfit = order,
                    status = BespokeOrderStatusLog.SEWING_COMMENCED
                )   

            if order.have_all_staff_being_approved() :
                BespokeOrderStatusLog.objects.get_or_create(
                    outfit = order,
                    status = BespokeOrderStatusLog.READY_FOR_DELIVERY
                )   
            return JsonResponse({'success': True})

        except BespokeOrder.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found, order may have been deleted.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
