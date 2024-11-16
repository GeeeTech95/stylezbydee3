from django.db import models








class Country(models.Model) :
    name = models.CharField(max_length = 30)
    code = models.CharField(max_length=10)

    def __str__(self) :
        return self.name


    
class Currency(models.Model) :
    CurrencyChoices = (
        ("NGN","NGN"),
        ("USD","USD"),
        ("GBP","GBP"),
        ("CAD","CAD"),

    )
    name = models.CharField(max_length=5,choices=CurrencyChoices)

    def __str__(self) :
        return self.name


class CurrencyConvert(models.Model) :
    
    _from = models.ForeignKey(Currency,on_delete=models.CASCADE,related_name="from_currency")
    _to = models.ForeignKey(Currency,on_delete=models.CASCADE,related_name = 'to_currency')
    multiply_by = models.DecimalField(decimal_places=5,max_digits=100)

    def __str__(self) :
        return "{}1 = {} X {} ".format(self._to,self._from,self.multiply_by)