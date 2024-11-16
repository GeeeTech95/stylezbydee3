from .models import SupportingBank,PaymentMethod



def user(request) :
    ctx = {}
    ctx['withdrawal_supporting_banks'] = SupportingBank.objects.all()
    ctx['payment_method_types'] = PaymentMethod.METHOD_TYPES
    return ctx