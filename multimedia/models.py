from django.db import models
from django.conf import settings
from common.utils.text import unique_slug
from django.utils import timezone

class BooksLibrary(models.Model):
    FORMAT_TYPE = [
        ('audio', 'audio'),
        ('text', 'text'),
    ]
    VISIBILITY_STATUES = [
        ('public', 'public'),
        ('private', 'private'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    published_date = models.DateField()
    published_by = models.CharField(max_length=100, blank=True, null=True)
    format_type = models.CharField(max_length=50, choices=FORMAT_TYPE)
    visibility =models.CharField(max_length=50, default="private", choices=VISIBILITY_STATUES)
    activeForVote =models.BooleanField(default=False)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    web_link = models.URLField(blank=True, null=True)
    summary = models.TextField(max_length=300, blank=True, null=True)
    cover_image = models.ImageField(upload_to='multimedia/book_covers/', blank=True, null=True)
    voteCount = models.PositiveIntegerField(default=0)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voted_books', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)  # Add this line
    
    class Meta:
        ordering = ['-published_date', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.title)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Gallery(models.Model):
  
    MEDIA_TYPE_CHOICES = [
        ('Photo', 'Photo'),
        ('Video', 'Video'),
    ]

    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=100, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='multimedia/gallery/', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)  # Add this line
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.title)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class UserManual(models.Model):
    title = models.CharField(max_length=200)
    version = models.CharField(max_length=20, default=1)
    usage_description = models.TextField(default=300, blank=True, null=True)
    file = models.FileField(upload_to='multimedia/userManuals/')
    published_by = models.CharField(max_length=200, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)  # Add this line
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.title)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class PraiseGlory(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(default=1000, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='multimedia/praiseGlory/', blank=True, null=True)
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

class TestimonyOfSalvation(models.Model):
    title = models.CharField(max_length=200)
    testimony = models.TextField(max_length=1000,null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    link = models.URLField(blank=True, null=True,help_text='A video that come from YouTube')
    testimony_image = models.ImageField(upload_to='testimony/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)  # Add this line
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.title)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title

class ArchiveLink(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='multimedia/ArchiveLink/', blank=True, null=True)
    url_link = models.URLField(blank=True, null=True)
    external_url = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)
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

class SpiritualPoemSong(models.Model):
    TYPE_CHOICES = [
        ('poem', 'Poem'),
        ('song', 'Song'),
    ]

    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Amharic', 'Amharic'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True, null=True)  # Optional author field
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    discretion = models.TextField(max_length=200, blank=True, null=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='en')
    published_date = models.DateField(blank=True, null=True)  # Optional publication date
    audio_file = models.FileField(upload_to='multimedia/spiritual_poems_songs/audio/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='multimedia/spiritual_poems_songs/pdf/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='multimedia/spiritual_poems_songs/covers/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)  # Link to external resource
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-published_date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.title)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
