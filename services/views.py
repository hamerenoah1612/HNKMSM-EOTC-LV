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
    BaptizedCertification, Sermon, SermonCategory, SermonMedia,
    FatherOfRepentanceLists, GroupMassageToSonOfRepentance,FuneralServicesApplication)
from members.models import MembersUpdateInformation
from django.contrib.auth.models import User
from .forms import BaptizedApplicationForm, BaptizedApplicationUpdatingForm,FuneralServicesApplication
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
    

#Funeral Services 
class FuneralServicesView(TemplateView):
    template_name = 'services/funeralServicesView.html'
    
class CreateFuneralServicesView(CreateView, LoginRequiredMixin):
    model = FuneralServicesApplication
    template_name = 'services/funeralServicesView.html'
    form_class = FuneralServicesApplication
    success_url = reverse_lazy('services:funeralServices')

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     title = form.cleaned_data.get('title')
    #     author = form.cleaned_data.get('author')
    #     published_date = form.cleaned_data.get('published_date')
        
    #     # Check if a book with the same title, author, and published date already exists
    #     if BooksLibrary.objects.filter(title=title, author=author, published_date=published_date).exists():
    #         form.add_error(None, "A book with the same title, author, and published date already exists.")
    #         return self.form_invalid(form)
        
    #     return super().form_valid(form)
    
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
