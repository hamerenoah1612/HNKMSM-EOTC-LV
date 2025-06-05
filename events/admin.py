# events/admin.py
from django.contrib import admin
from .models import Event, EventGallery, EventsCategory, PostEventImages,NewsAndAnnouncements,RemindMeUpcomingEvent,MarkedAsReadRemindMeNotification

admin.site.register(NewsAndAnnouncements)

admin.site.register(MarkedAsReadRemindMeNotification)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'start_time', 'end_time', 'status_tag','location', 
        'category', 'created_by', 'special_guests', 
        'max_number_guests', 'created', 'updated'
    )
    list_filter = ('category', 'start_time', 'end_time', 'created_by')
    search_fields = ('title', 'description', 'location', 'special_guests')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_time'
    ordering = ['-start_time', '-created']

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'start_time', 'end_time', 'location', 'image', 'media_url', 'category', 'special_guests', 'notices', 'max_number_guests', 'created_by', 'slug')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
        }),
    )
    readonly_fields = ('created', 'updated')

@admin.register(EventsCategory)
class EventsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class PostEventImagesInline(admin.TabularInline):
    model = PostEventImages
    extra = 1

@admin.register(EventGallery)
class EventGalleryAdmin(admin.ModelAdmin):
    list_display = ('post_events',
        'thumbnail_title', 'held_date', 'number_of_participants', 'thumbnail_image',
        'viewers_count', 'category', 'created', 'updated'
    )
    list_filter = ('held_date',)
    search_fields = ('thumbnail_title', 'short_review')
    prepopulated_fields = {'slug': ('thumbnail_title',)}
    date_hierarchy = 'held_date'
    ordering = ['-held_date', '-created']
    inlines = [PostEventImagesInline]

    fieldsets = (
        (None, {
            'fields': ('post_events','thumbnail_title', 'short_review', 'video_url', 'number_of_participants', 'category', 'held_date', 'thumbnail_image', 'slug')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
        }),
    )
    readonly_fields = ('created', 'updated')
    
@admin.register(PostEventImages)
class PostEventImagesAdmin(admin.ModelAdmin):
    list_display = ('event_gallery', 'image')
    search_fields = ('event_gallery__title',)
    list_filter = ('event_gallery',)
    
@admin.register(RemindMeUpcomingEvent)
class RemindMeUpcomingEventAdmin(admin.ModelAdmin):
    list_display = ('event', 'your_name', 'is_passed', 'is_viewed')