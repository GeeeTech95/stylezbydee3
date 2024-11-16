from fashion.models import Client
from django.utils import timezone
from fashion.models import BespokeOrderStatusLog

def core(request) :
    # Calculate the date one month ago
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    ctx = {}

    ctx['BO_STATUS_LOG_READY_FOR_DELIVERY'] = BespokeOrderStatusLog.READY_FOR_DELIVERY
    ctx['BO_STATUS_LOG_PAYMENT_COMPLETED'] = BespokeOrderStatusLog.PAYMENT_COMPLETED
    ctx['BO_STATUS_LOG_DELIVERED'] =  BespokeOrderStatusLog.DELIVERED
    ctx["currency_symbol"] = "₦"
    ctx['cliients_count'] = Client.objects.count()
    ctx['newly_acquired_clients_counts'] = Client.objects.filter(
        date_added__gte = one_month_ago
    ).count()#since last month
    return ctx