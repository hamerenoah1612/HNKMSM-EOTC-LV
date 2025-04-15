from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from allauth.account.views import PasswordChangeView
from .forms import CustomUserChangeForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import FieldError
from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('my-account')

class MyAccountPageView(SuccessMessageMixin,LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = 'account/my_account.html'
    success_message = 'Update Successful'

    def get_object(self):
        return self.request.user
    


# def custom_confirm_email(request, key):
#     try:
#         email_address = EmailAddress.objects.get(key=key)
#         if email_address.user.emailaddress_set.filter(verified=True, email=email_address.email).exists():
#             messages.error(request, "This email address has already been verified and is associated with another account.")
#             return redirect(reverse('account_login'))
#         email_address.verified = True
#         email_address.save()
#         email_confirmed.send(sender=email_address, request=request)
#         messages.success(request, "Your email address has been successfully verified.")
#         return redirect('account_login')
#     except EmailAddress.DoesNotExist:
#         messages.error(request, "This email confirmation link is invalid or has expired.")
#         return redirect(reverse('account_signup'))
#     except IntegrityError:
#         messages.error(request, "An unexpected error occurred: This email address is already associated with a verified account.")
#         return redirect(reverse('account_login'))
#     except FieldError as e:  # Catch the specific FieldError
#         messages.error(request, f"An internal error occurred: {e}")
#         return redirect(reverse('account_signup'))
#     except Exception as e:
#         messages.error(request, f"An unexpected error occurred: {e}")
#         return redirect(reverse('account_signup'))

