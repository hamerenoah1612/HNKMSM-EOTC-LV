from django.db import models
from django.conf import settings
from common.utils.text import unique_slug
from django.utils import timezone

# Sermon services
class SermonSeries(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Add any other fields relevant to sermon series
    
    def __str__(self):
        return self.title
    
class SermonCategory(models.Model):
    category = models.CharField(max_length=200)
    subcategory = models.CharField(max_length=200)
    # Add any other fields relevant to sermon series
    
    def __str__(self):
        return self.category

class Sermon(models.Model):
    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=100)
    date_preached = models.DateField()
    series = models.ForeignKey(SermonSeries, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(SermonCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='sermonGallery/%Y/%m/%d', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)  # Add this line
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.title)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class SermonMedia(models.Model):
    SERMON_TYPES = (
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('transcript', 'Transcript'),
    )
    sermon = models.ForeignKey(Sermon, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=20, choices=SERMON_TYPES)
    media_url = models.URLField()
    # Add any other fields relevant to sermon media
    
class Comment(models.Model):
    sermon = models.ForeignKey(Sermon, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(default="God is great!!")
    respond = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    respond_at = models.DateTimeField(auto_now=True)
    # Add any other fields relevant to comments
    
    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.user)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.comment

class BaptizedCertification(models.Model):
    BAPTIZED_TYPES = (
        ('youth', 'youth'),
        ('children', 'children'),  
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    baptize_type = models.CharField(max_length=100, choices=BAPTIZED_TYPES)
    baptism_date = models.DateField()
    christina_name = models.CharField(max_length=100, blank=True, null=True)
    given_full_name = models.CharField(max_length=200)
    fathers_full_name = models.CharField(max_length=200)
    mothers_full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    child_country_of_birth = models.CharField(max_length=100)
    christian_fathers_or_mothers_name = models.CharField(max_length=100, blank=True, null=True)
    priest_who_baptized = models.CharField(max_length=100, blank=True, null=True)
    qualified = models.BooleanField(default=False)
    service_request_confirmation_number=models.CharField(max_length=100, blank=True, null=True)
    citification_request_confirmation_number=models.CharField(max_length=100, blank=True, null=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)  
    applied_data= models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
   
    
    def save(self, *args, **kwargs):
        
        if self.applied_data :
            applied_date_short = self.applied_data.strftime('%Y%m%d%H%M%S')
            self.service_request_confirmation_number = f"BTZ-{applied_date_short}-EOTC"
        if not self.slug:
            value = str(self.given_full_name)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.given_full_name

class FatherOfRepentanceLists(models.Model):
    COMMUNICATION_PREFERENCE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('other', 'Other'),
    ]
    AVAILABILITY_STATUS = (
        ('active', 'active'),
        ('deactivated', 'deactivated'),  
    )
    full_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='fathers_of_repentance/', help_text="Recommended size: 800px (width) by 450px (height).")
    location = models.CharField(max_length=255)
    availability_days = models.CharField(max_length=255, help_text="e.g. Monday to Friday")
    availability_hours = models.CharField(max_length=255, help_text="e.g. 9:00 AM to 5:00 PM")
    church_serving = models.CharField(max_length=255, help_text="Full-time serving church")
    title_serving = models.CharField(max_length=255, help_text="title position of serving in church", null=True, blank=True)
    experience_summary = models.TextField()
    communication_preference = models.CharField(max_length=10, choices=COMMUNICATION_PREFERENCE_CHOICES, default='phone')
    communication_information = models.CharField(max_length=255, help_text="Might be active phone, email, whatsappNumber, telegramNumber")
    availability_states = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='active')
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.full_name)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.full_name

class GroupMassageToSonOfRepentance(models.Model):
    father_of_repentance = models.ForeignKey(FatherOfRepentanceLists, on_delete=models.CASCADE)
    message = models.TextField(help_text="Message to Sons of Repentance")
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True) 
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.father_of_repentance.full_name)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Message from {self.father_of_repentance.full_name} at {self.sent_at}"

class FuneralServicesApplication(models.Model):
    # Applicant details
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default='1')
    full_name = models.CharField(max_length=255, help_text="Full name of the applicant")
    phone_number = models.CharField(max_length=15, help_text="Contact phone number")
    email = models.EmailField(blank=True, null=True, help_text="Optional email address")
    address = models.TextField(help_text="Address of the applicant")

    # Deceased details
    deceased_full_name = models.CharField(max_length=255, help_text="Full name of the deceased")
    age = models.PositiveIntegerField(help_text="Age of the deceased")
    date_of_passing = models.DateField(help_text="Date of passing")
    place_of_death = models.CharField(max_length=255, help_text="Place where the deceased passed away")

    # Service details
    preferred_date = models.DateField(help_text="Preferred date for the funeral service")
    church_name = models.CharField(max_length=255, help_text="Name of the church where the service will be held")
    additional_requests = models.TextField(blank=True, null=True, help_text="Any additional requests or details")
    location_preferred = models.CharField(max_length=255, blank=True, null=True, help_text="location preferred where the service will be held")
    
    # Administrative fields
    is_paid = models.BooleanField(default=False, help_text="Indicates whether the required payment has been made")
    slug = models.SlugField(unique=True, blank=True, help_text="Unique identifier for the application")
    created = models.DateTimeField(auto_now_add=True, help_text="Date and time the application was created")
    updated = models.DateTimeField(auto_now=True, help_text="Date and time the application was last updated")

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(f"{self.full_name}-{self.created}")
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Funeral Service Application for {self.deceased_full_name} by {self.full_name}"

#Memorial Service