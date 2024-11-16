
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.views.generic.edit import CreateView,View, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages  # Import the messaging framework


from fashion.forms import ClientForm, MeasurementForm
from fashion.models import ClientBodyMeasurement ,Client


class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('myadmin:client-list')

    def get_context_data(self, **kwargs):
        context = super(ClientCreateView,self).get_context_data(**kwargs)
        context['form_client'] = ClientForm()
            
        return context





class ClientUpdateView(View):
    
    def get(self, request, *args, **kwargs):
        client = Client.objects.get(pk=self.kwargs['pk'])
        target_form = kwargs.get("target_form")  # Capture the target form from the URL
        #incase no exist
        ClientBodyMeasurement.objects.get_or_create( client = client)

        # Initialize empty form variables
        form = None
    

        # Determine which form to display based on 'target_form'
        if target_form == "info":
            form = ClientForm(instance=client)
            form_title = "Client Details"
        elif target_form == "measurement":
            form = MeasurementForm(instance=client.measurement, client_gender=client.gender)
            form_title = "Measurement Details"
        else:
            return HttpResponse("Invalid form target", status=400)  # Return error if the target is invalid

        return render(request, 'clients/client_form.html', {
            'form': form,
            'target_form': target_form , # Pass target_form to the template
             'form_title' : form_title
        })


    def post(self, request, *args, **kwargs):
        client = Client.objects.get(pk=self.kwargs['pk'])
        target_form = kwargs.get("target_form")  # Capture the target form from the URL

        # Initialize empty form variables
        form= None
  

        # Determine which form to process based on 'target_form'
        if target_form == "info":
            form = ClientForm(request.POST,request.FILES, instance=client)
            form_title = "Client Details"
            if form.is_valid():
                form.save()
                messages.success(request, 'Client details has  been updated successfully.')  # Add success message
                return HttpResponseRedirect(reverse_lazy('myadmin:client-detail',args=[client.pk]))
            else:
                messages.error(request, 'Please correct the errors below.')
                return render(request, 'clients/client_form.html', {
                    'form': form,
                    'target_form': target_form,
                    "form_title" : form_title

                })


        elif target_form == "measurement":
            form = MeasurementForm(request.POST, instance=client.measurement, client_gender=client.gender)
            form_title = "Measurement Details"
            if form.is_valid():
                form.save(commit = False)
                form.instance.client = client
                form.save()
                messages.success(request, 'Measurement details has been updated successfully.')  # Add success message
                return HttpResponseRedirect(reverse_lazy('myadmin:client-detail',args=[client.pk]))
            else:
                print(form.errors)
                messages.error(request, 'Please correct the errors below.')
                return render(request, 'clients/client_form.html', {
                    'form': form,
                    'target_form': target_form,
                    "form_title" : form_title
                })
            

        else:
            return HttpResponse("Invalid form target", status=400)  # Return error if the target is invalid
