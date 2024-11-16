from .models import ProductCategory, ProductClass
from .models import Product


def product(request):
    ctx = {}
    ctx['ChildProductCategories'] = ProductCategory.objects.filter(numchild=0)
    ctx['ProductClasses'] = ProductClass.objects.all()
    ctx['ParentProductCategories'] = ProductCategory.objects.filter(depth=1)

    ctx['womenParentProductCategories'] = ProductCategory.objects.filter(
        depth=1, gender__in=['Women', 'Unisex'])

    ctx['menParentProductCategories'] = ProductCategory.objects.filter(
        depth=1, gender__in=['Men', 'Unisex'])
    ctx['womenTopTrending'] = Product.products.filter(gender="Women").first()
  

    return ctx
