# events/models.py
from django.db import models
from django.conf import settings
from common.utils.text import unique_slug
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status_tag = models.CharField(max_length=200, default='active')
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/%Y/%m/%d', blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey('EventsCategory', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    special_guests = models.CharField(max_length=200, blank=True, null=True)
    notices = models.TextField(blank=True, null=True)
    max_number_guests = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-start_time', '-created']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.title, Event)
        now = timezone.now()
        
        if self.end_time < now:
            self.status_tag = 'past'
        else:
            self.status_tag = 'active'
       
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class EventsCategory(models.Model):
    name = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class EventGallery(models.Model):
    post_events = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True)
    thumbnail_title = models.CharField(max_length=200, blank=True, null=True)
    short_review = models.TextField(max_length=1000,blank=True, null=True )
    video_url = models.URLField(blank=True, null=True)
    number_of_participants = models.PositiveIntegerField(default=100)
    held_date = models.DateField()
    thumbnail_image = models.ImageField(upload_to='event_gallery/thumbnails/%Y/%m/%d', blank=True, null=True)
    viewers_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('EventsCategory', on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-held_date', '-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.thumbnail_title, EventGallery)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.thumbnail_title

class PostEventImages(models.Model):
    event_gallery = models.ForeignKey(EventGallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_gallery/images/%Y/%m/%d')

    def __str__(self):
        return f"Image for {self.event_gallery.thumbnail_title}"
    
class NewsAndAnnouncements(models.Model):
    ERGENCE_TYPE_CHOICES = [
        ('urgent', 'Urgent'),
        ('on_time', 'On-Time'),
        ('as_quick_as', 'As Quick As'),
    ]

    CATEGORY_CHOICES = [
        ('news', 'News'),
        ('announcement', 'Announcement'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='newsAnnouncement_images/', blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    announce_to = models.TextField(max_length=100,blank=True, null=True)
    announcer = models.CharField(max_length=100,blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='news')
    emergence_type = models.CharField(max_length=20, choices=ERGENCE_TYPE_CHOICES, default='on_time')
    reference_source = models.CharField(max_length=100,blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news_announcements')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.title[:50])
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.category.capitalize()} - {self.emergence_type.capitalize()}"
    
    
class RemindMeUpcomingEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='event')
    your_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='remainder')
    massage = models.TextField(default="Upcoming Event Tomorrow:This is a polite reminder that the scheduled event will take place tomorrow. Please ensure you are prepared & ready to participate.")
    is_passed = models.BooleanField(default=False)
    is_viewed = models.BooleanField(default=False )
    slug = models.SlugField(unique=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.your_name)
            self.slug = unique_slug(value, type(self))
        now = timezone.now()
        
        if self.event.end_time < now:
            self.is_passed = True
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Remainder:{self.event.title} coming tomorrow start_time {self.event.start_time}"
    
    
class MarkedAsReadRemindMeNotification(models.Model):
        """
        Tracks when a specific user has marked a RemindMeUpcomingEvent as read.
        """
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='read_reminders')
        event = models.ForeignKey(RemindMeUpcomingEvent, on_delete=models.CASCADE, related_name='read_by_users')
        timestamp = models.DateTimeField(auto_now_add=True)
        is_read = models.BooleanField(default=True) # Always True when created via this view

        class Meta:
            unique_together = ('user', 'event') # A user can only mark an event as read once

        def __str__(self):
            return f"{self.user.username} read {self.event.event.title}"