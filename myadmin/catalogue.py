
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.views.generic.edit import CreateView, View, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages  # Import the messaging framework


from fashion.models import Catalogue, CatalogueImage
from fashion.forms import CatalogueForm, CatalogueImageFormSet


from django.urls import reverse
from django.views.generic import DeleteView


class CatalogueDeleteView(DeleteView):
    model = Catalogue
    success_url = reverse_lazy('catalogue_list')  # Redirect to the list view after deletion
    template_name = 'catalogue-confirm-delete.html'


class CatalogueEditView(UpdateView):
    model = Catalogue
    fields = ['title', 'description_text', 'cost', 'discount_price', 'image']
    template_name = 'catalogue-edit.html'
    
    def get_success_url(self):
        return reverse('catalogue_detail', kwargs={'pk': self.object.pk})



class CatalogueDetailView(DetailView):
    model = Catalogue
    template_name = 'catalogue/catalogue-detail.html'
    context_object_name = 'catalogue_item'
  



class CatalogueListView(ListView):
    model = Catalogue
    template_name = 'catalogue/catalogue-list.html'  # Template for rendering the list
    # Context name for accessing items in the template
    context_object_name = 'catalogue_items'
    paginate_by = 10  # Number of items per page (optional)



class CatalogueCreateView(CreateView):
    model = Catalogue
    form_class = CatalogueForm
    template_name = 'catalogue/catalogue-form.html'
    success_url = reverse_lazy('myadmin:catalogue-list')  # Replace with your desired URL

    def get_context_data(self, **kwargs):
        """Provide context for the form and formset."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = CatalogueImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = CatalogueImageFormSet()
        return context

    def form_valid(self, form):
        """Save the Catalogue and its associated images."""
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        # Debug: Print out POST data
        print("POST Data:", self.request.POST)

        if form.is_valid() and image_formset.is_valid():
            # Save the catalogue form
            self.object = form.save()

            # Associate the formset with the saved catalogue object
            image_formset.instance = self.object

            # Debugging: Ensure the catalogue object is saved
            print(f"Catalogue saved with ID: {self.object.id}")

            # Save the image formset
            image_formset.save()

            return HttpResponseRedirect(self.success_url)
        else:
            # Debugging: Print form errors
            print("Form errors:", form.errors)

            # Debugging: Print image formset errors
            print("Image formset errors:", image_formset.errors)

            return self.form_invalid(form)
