from django import forms
from .models import BaptizedCertification,FuneralServicesApplication

class BaptizedApplicationForm(forms.ModelForm):
    class Meta:
        model = BaptizedCertification
        fields = [
            'baptize_type',
            'baptism_date',
            'given_full_name', 
            'fathers_full_name', 
            'mothers_full_name', 
            'phone_number' ,
            'child_country_of_birth', 
            'christian_fathers_or_mothers_name', 
            ]
        widgets = {
            'baptism_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
class BaptizedApplicationUpdatingForm(forms.ModelForm):
    class Meta:
        model = BaptizedCertification
        fields = [
            'baptize_type',
            'baptism_date',
            'christina_name',
            'given_full_name',
            'fathers_full_name',
            'mothers_full_name',
            'phone_number',
            'child_country_of_birth',
            'christian_fathers_or_mothers_name',
            'priest_who_baptized',
        ]
        widgets = {
            'baptism_date': forms.DateInput(attrs={'type': 'date'}),
        }


class FuneralServicesApplicationForm(forms.ModelForm):
    class Meta:
        model = FuneralServicesApplication
        fields = [
            'full_name',
            'phone_number',
            'email',
            'address',
            'deceased_full_name',
            'age',
            'date_of_passing',
            'place_of_death',
            'preferred_date',
            'church_name',
            'additional_requests',
        ]
        widgets = {
            'date_of_passing': forms.DateInput(attrs={'type': 'date'}),
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'additional_requests': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'full_name': 'Applicant Full Name',
            'phone_number': 'Contact Phone Number',
            'email': 'Email Address (Optional)',
            'address': 'Applicant Address',
            'deceased_full_name': 'Deceased Full Name',
            'age': 'Age of the Deceased',
            'date_of_passing': 'Date of Passing',
            'place_of_death': 'Place of Death',
            'preferred_date': 'Preferred Funeral Service Date',
            'church_name': 'Church Name',
            'additional_requests': 'Additional Requests or Details',
        }
        help_texts = {
            'email': 'Provide an email address if available.',
            'additional_requests': 'Include any specific requests for the funeral service.',
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age <= 0:
            raise forms.ValidationError("Age must be a positive number.")
        return age
