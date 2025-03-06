from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django_resized import ResizedImageField
from django.core.files.images import get_image_dimensions
from django.db import models
from django.urls import reverse


def validate_avatar(value):
    w, h = get_image_dimensions(value)
    if w > 200 or h > 200:
        raise ValidationError('Avatar must be no bigger than 200x200 pixels.')

# Create your models here.
class CustomUser(AbstractUser):
    
    dob = models.DateField(
        verbose_name= "Date of Birth", null=True , blank=True
    )
    # avatar = models.ImageField(
    #     upload_to='avatars/', 
    #     blank=True,
    #     help_text='Image must be 200px by 200px.',
    #     validators=[validate_avatar],
    # )
    avatar = ResizedImageField(
        size=[200, 200],  # Resize to 300x300 pixels
        crop=['middle', 'center'],  # Crop image
        quality=75,  # Image quality (1-100)
        upload_to='avatars/', 
        blank=True,
        help_text='Image must be 200px by 200px.',
        # validators=[validate_avatar],
    )
    def get_absolute_url(self):
        return reverse('my-account')

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'