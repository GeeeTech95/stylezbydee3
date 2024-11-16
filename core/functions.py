from .models import Currency,CurrencyConvert
import decimal
def convert_currency(amount,from_currency,to_currency) :
    
    """
    from_currency and to_currency must be strings.
    e.g : USD
    """
    amount = decimal.Decimal(amount)
    if from_currency == to_currency : 
        return amount
    
    match = CurrencyConvert.objects.filter(_from__name = from_currency, _to__name = to_currency)
    
    if not match.exists() : 
        raise TypeError
    
    if amount < 0 : 
        raise ValueError
    
    match = match.first()
    return round(amount * match.multiply_by,2)
    
    



def get_default_currency() :
    """ returns the default currency used here"""
    default_currency = Currency.objects.first()
    return default_currency

