from email.mime import application
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView,UpdateView,CreateView
from .models import (
    BaptizedCertification, Sermon, 
    SermonCategory, SermonMedia,
    FatherOfRepentanceLists, 
    GroupMassageToSonOfRepentance,
    FuneralServicesApplication
    )
from members.models import MembersUpdateInformation
from .forms import ( BaptizedApplicationForm, 
                    BaptizedApplicationUpdatingForm,
                    FuneralServicesApplicationForm,
                    FuneralServicesApplicationUpdatingForm
                    )
class ServicesView(TemplateView):
    template_name = 'services/servicesView.html'

class SermonServicesView(TemplateView):
    template_name = 'services/sermon.html'
    
class SermonMediaListView(ListView):
    model = SermonMedia
    template_name = 'services/sermon_media_list.html'  # Template name to be created
    context_object_name = 'sermon_media_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sermon_media = SermonMedia.objects.all() 
        context['sermon_categories'] = {}

        for media in sermon_media:
            category = media.sermon.category.category
            if category not in context['sermon_categories']:
                context['sermon_categories'][category] = SermonCategory.objects.filter(category=category)

        return context
              
class SermonMediaDetailView(DetailView):
    model = SermonMedia
    template_name = 'services/sermon_media_detail.html'  # Template name to be created
    context_object_name = 'sermon_media'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sermon_media = self.get_object()  # Get the current SermonMedia object
        related_sermons = Sermon.objects.filter(category=sermon_media.sermon.category)  # Filter related sermons by category

        context['related_sermons'] = related_sermons
        return context

class BaptismServiceView(LoginRequiredMixin,View):
    #model = BaptizedCertification
    template_name = 'services/baptism_service.html'  # Template name to be created
          
    def get(self, request):
        #Forms
        baptizedForm = BaptizedApplicationForm()
        baptizedApplicationConfirmation = BaptizedCertification.objects.filter(user=self.request.user).first()
        context = {
            'baptizedForm': baptizedForm,
            'baptizedApplicationConfirmation':baptizedApplicationConfirmation,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        baptizedForm = BaptizedApplicationForm(request.POST)
        user = request.user
        member = MembersUpdateInformation.objects.filter(user=user).first()
        
        if baptizedForm.is_valid():
            # user = request.user
            baptized_application = baptizedForm.save(commit=False)
            baptized_application.user = user
            if member:
                baptized_application.qualified = True
            baptized_application.save()
            
                
            # Add a success message
            messages.success(request, 'Your baptism application has been successfully submitted!')
            return redirect('services:baptism_service')
                       
        context = {
            'baptizedForm': baptizedForm, 
        }
        return render(request, self.template_name, context)

class BaptizedApplicationUpdatingView(LoginRequiredMixin, UpdateView):
    model = BaptizedCertification
    template_name = 'services/baptism_service_ApplicationUpdating.html'
    form_class = BaptizedApplicationUpdatingForm
    success_url = reverse_lazy('services:baptism_service')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return BaptizedCertification.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Your baptism application information has been updated successfully!')
        return super().form_valid(form)

# HolyCommunion
class HolyCommunionServicesView(TemplateView):
    template_name = 'services/holyCommunion.html'
    
class CreateFuneralServicesView(LoginRequiredMixin, CreateView):
    model = FuneralServicesApplication
    template_name = 'services/funeralServicesView.html'
    form_class = FuneralServicesApplicationForm
    success_url = reverse_lazy('services:createFuneralServices')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assuming 'user' is a field in the model

        # Check if an application already exists for the user
        if FuneralServicesApplication.objects.filter(user=form.instance.user).exists():
            form.add_error(None, "A Funeral Services Application already exists.")
            return self.form_invalid(form)

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the existing application for the user
        funeralServices = FuneralServicesApplication.objects.filter(user=self.request.user).first()
        if funeralServices:
            context['funeralServices'] = funeralServices
        else :
            context['funeralServices'] = 'None'
        return context
  
#Funeral Services UpdateFuneralServicesApplication
class UpdateFuneralServicesApplication(LoginRequiredMixin, UpdateView):
    model = FuneralServicesApplication
    template_name = 'services/UpdateFuneralServicesApplication.html'
    form_class = FuneralServicesApplicationUpdatingForm
    success_url = reverse_lazy('services:createFuneralServices')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return FuneralServicesApplication.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Your Funeral application information has been updated successfully!')
        return super().form_valid(form)
         
#WeddingServicesView
class WeddingServicesView(TemplateView):
    template_name ='services/weddingServices.html'
 
# ListView for displaying all Fathers of Repentance
class FatherOfRepentanceListView(ListView):
    model = FatherOfRepentanceLists
    template_name = 'services/fatherOfRepentance.html'
    context_object_name = 'fathers'
    paginate_by = 9  # Paginate after every 9 item
    
class FatherOfRepentanceDetailView(DetailView):
    model = FatherOfRepentanceLists
    template_name = 'services/fatherOfRepentanceDetail.html'
    context_object_name = 'father'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch related messages for the specific Father of Repentance
        context['messages'] = GroupMassageToSonOfRepentance.objects.filter(father_of_repentance=self.object)
        return context
