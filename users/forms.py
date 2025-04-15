from datetime import datetime
from django import forms
from django.forms import TextInput, EmailInput, Textarea, DateInput,FileInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.forms.widgets import DateInput
from allauth.account.forms import LoginForm

User = get_user_model()
BIRTH_YEAR_CHOICES = range(1915, datetime.now().year)

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        widgets = {
           
            'email': EmailInput(attrs={
                'class': 'w-100 form-control form-sm-control border-primary bg-light text-small',
                'placeholder': 'Email'
            }),
            'first_name': TextInput(attrs={
                'class': 'w-100 form-control form-sm-control border-primary bg-light text-small',
                'placeholder': 'First Name'
            }),
            'last_name': TextInput(attrs={
                'class': 'w-100 form-control form-sm-control border-primary bg-light text-small',
                'placeholder': 'Last Name'
            }),
        }

    def signup(self, request, user):
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()

# class SignupForm(forms.Form):
#     first_name = forms.CharField(max_length=50, required=False)
#     last_name = forms.CharField(max_length=50, required=False)
    
#     def signup(self, request, user):
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.save()
        
   
class CustomUserChangeForm(UserChangeForm):
    password = None
    
    # class Meta:
    #     model = get_user_model()
    #     fields = ('email', 'username', 'first_name', 'last_name', 'dob', 'avatar')
      
    #     widgets = {
    #         'dob': DateInput(attrs={'type': 'date','style': 'width: 100%; font-size:13px;'}), 
    #     }
       
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'dob', 'avatar')
        
        widgets = {
            'username': TextInput(attrs={'class': 'w-100 form-control p-3 mb-4 border-primary bg-light', 'placeholder': 'Your Name'}),
            'email': EmailInput(attrs={'class': 'w-100 form-control p-3 mb-4 border-primary bg-light', 'placeholder': 'Enter Your Email'}),
            'first_name': TextInput(attrs={'class': 'w-100 form-control p-3 mb-4 border-primary bg-light', 'placeholder': 'Enter Your First Name'}),
            'last_name': TextInput(attrs={'class': 'w-100 form-control p-3 mb-4 border-primary bg-light', 'placeholder': 'Enter Your Last Name'}),
            'dob': DateInput(attrs={'class': 'w-100 form-control p-3 mb-4 border-primary bg-light', 'type': 'date', 'style': 'width: 100%; font-size:13px;', 'placeholder': 'Select Your Date of Birth'}),
            'avatar': FileInput(attrs={'class': 'w-100 form-control p-3 mb-4 border-primary bg-light', 'placeholder': 'Your image'}),
        }
        
        


class CustomLoginForm(LoginForm):
    def clean(self):
        cleaned_data = super().clean() or {}  # fallback to empty dict if None

        email = cleaned_data.get('login')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                self.password_error = not user.check_password(password)
            except User.DoesNotExist:
                self.password_error = False
        else:
            self.password_error = False

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password_error = False

    def get_context(self):
        context = super().get_context()
        context['password_error'] = self.password_error
        return context
