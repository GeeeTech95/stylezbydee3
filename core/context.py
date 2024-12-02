from .models import Currency, Country
from shop.models import Product


def core(request):
    ctx = {}
    ctx['site_name'] = "StylezByDee"
    ctx['CURRENCIES'] = Currency.objects.all()
    ctx['COUNTRIES'] = Country.objects.all()
    ctx['site_address'] = "Box 55 plaza, old airport road, Emene Enugu Nigeria"
    ctx['site_phone'] = "+2349028736553"
    ctx['site_phone2'] = "+2349026890331"
    ctx['site_email'] = "info@stylezbydee.com"
    ctx['x_link'] = "#0"
    ctx['instagram_link'] = "https://www.instagram.com/p/C9e7_gdorpg/?igsh=MXBmYWhreDRud3ltNA=="
    ctx['instagram_link_men'] = "https://www.instagram.com/p/C9C07XJNQV-/?igsh=MXA1NmRvNHRiNXlwYQ=="
    ctx['instagram_link_fashion_school'] = "https://www.instagram.com/stylezbydeefashionschool?igsh=bzdpMWt4NWVnaHNh"
    ctx['instagram_link_rtw'] = "https://www.instagram.com/p/C9KUGSFsVlk/?igsh=czZxOWNyZGRkZnFw"
    ctx['tiktok_link'] = "https://www.tiktok.com/@stylezbydee?_t=8ocBJMaCJQD&_r=1"
    ctx['facebook_link'] = "https://www.facebook.com/profile.php?id=100092686010057&mibextid=LQQJ4d"
    ctx['linkedin_link'] = "#0"
    ctx['youtube_link'] = "#0"
    ctx['whatsapp_item_enquiry_link}}'] = "https://wa.me/+2349026890331"
    return ctx


