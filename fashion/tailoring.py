from django.views import generic


class CustomTailoring(generic.TemplateView) :
    template_name = "custom-tailoring.html"


class Catalogue(generic.TemplateView) :
    template_name = "catalogue.html"
  

class HowItWorks(generic.TemplateView) :
    template_name = "how-it-works.html"
  
