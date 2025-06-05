from django import forms
from .models import MembersUpdateInformation, Child, Relative
from django.forms.models import inlineformset_factory


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'age', 'gender']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'age': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'gender': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

class RelativeForm(forms.ModelForm):
    class Meta:
        model = Relative
        fields = ['name', 'relationship']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }
  
class MembersUpdateInformationForm(forms.ModelForm):
    
    marital_status = forms.ChoiceField(
        choices=MembersUpdateInformation.MARITAL_STATUS, 
        widget=forms.RadioSelect
    )
    class Meta:
        model = MembersUpdateInformation
        fields = [
            'full_name', 'baptismal_name', 'godfather', 'address', 'city', 'state',
            'zip_code', 'apartment', 'telephone_number', 'email', 'marital_status',
            'spouse_name', 'spouse_baptismal_name'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'baptismal_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'godfather': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'state': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'apartment': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'telephone_number': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'marital_status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'spouse_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'spouse_baptismal_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

ChildFormSet = inlineformset_factory(MembersUpdateInformation, Child, form=forms.ModelForm, fields=['name', 'age', 'gender'],widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'age': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'gender': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        } ,extra=1)
RelativeFormSet = inlineformset_factory(MembersUpdateInformation, Relative, form=forms.ModelForm, fields=['name', 'relationship'], widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        },extra=1)