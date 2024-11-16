from django.views import generic



class ExploreCollection(generic.TemplateView) : 
    template_name = "explore-collection.html"
    title_dict = {"men" : "Men","women" : "Women","unisex" : "Unisex" }
    
    
    def get_context_data(self,**kwargs) :
        ctx = super(ExploreCollection,self).get_context_data(**kwargs)
        gender = self.request.GET.get('g')
        q = self.request.GET.get("q")
       
        if gender :
            gender = gender.lower()
            if gender  and gender in self.title_dict :
                ctx['title'] = self.title_dict.get(gender)
        elif q  and len(q) > 0 :
            ctx['title'] = q
        return ctx


class ExploreShop(generic.TemplateView) : 
    template_name = "explore-shop.html"
    title_dict = {"men" : "Men","women" : "Women","unisex" : "Unisex" }
    
    
    def get_context_data(self,**kwargs) :
        ctx = super(ExploreShop,self).get_context_data(**kwargs)
        gender = self.request.GET.get('g')
        q = self.request.GET.get("q")
       
        if gender :
            gender = gender.lower()
            if gender  and gender in self.title_dict :
                ctx['title'] = self.title_dict.get(gender)
        elif q  and len(q) > 0 :
            ctx['title'] = q
        return ctx


