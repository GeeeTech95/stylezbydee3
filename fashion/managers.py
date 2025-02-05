from django.db import models
from django.apps import apps




class BespokeOrderManager(models.Manager):
   

    def pending_orders(self):
        # Get the status log model dynamically
        status_log_model = apps.get_model('fashion', 'BespokeOrderStatusLog')

        # Subquery to get the latest status log for each order
        latest_status_log = status_log_model.objects.filter(
            outfit=models.OuterRef('pk')  # Match logs to the order
        ).order_by('-date').values('status')[:1]  # Get the most recent status

        # Filter orders where the latest status is either ORDER_CREATED or MEASUREMENT_ACQUIRED
        return self.annotate(
            latest_status=models.Subquery(latest_status_log)
        ).filter(
            latest_status__in=[
                status_log_model.ORDER_CREATED,
                status_log_model.MEASUREMENT_ACQUIRED
            ]
        )
    

    def in_progress_orders(self):
        # Get the status log model dynamically
        status_log_model = apps.get_model('fashion', 'BespokeOrderStatusLog')

        # Subquery to get the latest status log for each order
        latest_status_log = status_log_model.objects.filter(
            outfit=models.OuterRef('pk')  # Match logs to the order
        ).order_by('-date').values('status')[:1]  # Get the most recent status

        # Filter orders where the latest status is either ORDER_CREATED or MEASUREMENT_ACQUIRED
        return self.annotate(
            latest_status=models.Subquery(latest_status_log)
        ).filter(
            latest_status__in=[
                status_log_model.SEWING_COMMENCED,
                status_log_model.ADVANCE_PAYMENT_MADE,
            ]
        )
    

    def ready_for_delivery_orders(self):
        # Get the status log model dynamically
        status_log_model = apps.get_model('fashion', 'BespokeOrderStatusLog')

        # Subquery to get the latest status log for each order
        latest_status_log = status_log_model.objects.filter(
            outfit=models.OuterRef('pk')  # Match logs to the order
        ).order_by('-date').values('status')[:1]  # Get the most recent status

        # Filter orders where the latest status is either ORDER_CREATED or MEASUREMENT_ACQUIRED
        return self.annotate(
            latest_status=models.Subquery(latest_status_log)
        ).filter(
            latest_status__in=[
                status_log_model.READY_FOR_DELIVERY,
             
            ]
        )


    def delivered_orders(self):
        # Returns orders that have "delivered" status
        status_log_model = apps.get_model('fashion.BespokeOrderStatusLog')
        return self.filter(
            status_log__status=status_log_model.DELIVERED
        ).distinct()
    
    
    def cancelled_orders(self):
        # Returns orders that have "cancelled" status
        status_log_model = apps.get_model('fashion.BespokeOrderStatusLog')
        return self.filter(
            status_log__status=status_log_model.CANCELLED
        ).distinct()


class ClientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)  # Excludes inactive clients
