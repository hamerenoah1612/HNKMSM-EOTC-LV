from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import MembersUpdateInformation, Child, Relative
from payments.models import PaymentCases
from .forms import MembersUpdateInformationForm, ChildFormSet, RelativeFormSet
from .forms import ChildForm, RelativeForm
from django.views.generic.edit import UpdateView
from django.shortcuts import render



class MemberCreateView(LoginRequiredMixin, CreateView):
    model = MembersUpdateInformation
    form_class = MembersUpdateInformationForm
    template_name = 'members/member_create_form.html'
    success_url = reverse_lazy('members:member_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['children'] = ChildFormSet(self.request.POST)
            data['relatives'] = RelativeFormSet(self.request.POST)
        else:
            data['children'] = ChildFormSet()
            data['relatives'] = RelativeFormSet()
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        children = context['children']
        relatives = context['relatives']
        self.object = form.save()
        if children.is_valid() and relatives.is_valid():
            children.instance = self.object
            children.save()
            relatives.instance = self.object
            relatives.save()
        return super().form_valid(form)

class MemberListView(LoginRequiredMixin, ListView):
    model = MembersUpdateInformation
    template_name = 'members/member_list.html'
    context_object_name = 'members'
    
    def get_queryset(self):
        return MembersUpdateInformation.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['child_form'] = ChildForm()
        context['relative_form'] = RelativeForm()
        context['payment_cases_membership'] = PaymentCases.objects.filter(title='membership')
        return context

class ChildCreateView(LoginRequiredMixin, CreateView):
    model = Child
    form_class = ChildForm
    success_url = reverse_lazy('members:member_list')
    
    def form_valid(self, form):
        form.instance.member = MembersUpdateInformation.objects.get(user=self.request.user)
        return super().form_valid(form)

class RelativeCreateView(LoginRequiredMixin, CreateView):
    model = Relative
    form_class = RelativeForm
    success_url = reverse_lazy('members:member_list')
    
    def form_valid(self, form):
        form.instance.member = MembersUpdateInformation.objects.get(user=self.request.user)
        return super().form_valid(form)

class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = MembersUpdateInformation
    form_class = MembersUpdateInformationForm
    template_name = 'members/member_update_form.html'
    success_url = reverse_lazy('members:member_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['children'] = ChildFormSet(self.request.POST, instance=self.object)
            data['relatives'] = RelativeFormSet(self.request.POST, instance=self.object)
        else:
            data['children'] = ChildFormSet(instance=self.object)
            data['relatives'] = RelativeFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        children = context['children']
        relatives = context['relatives']
        self.object = form.save()
        if children.is_valid() and relatives.is_valid():
            children.instance = self.object
            relatives.instance = self.object
            children.save()
            relatives.save()
            return super().form_valid(form)
        else:
            print("Children Formset Errors: ", children.errors)
            print("Relatives Formset Errors: ", relatives.errors)
            return self.form_invalid(form)