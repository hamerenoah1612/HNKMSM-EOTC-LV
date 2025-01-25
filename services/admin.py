from django.contrib import admin
from .models import (SermonCategory, SermonSeries, 
Sermon, SermonMedia, 
Comment, BaptizedCertification,
FatherOfRepentanceLists,
GroupMassageToSonOfRepentance,
FuneralServicesApplication
)

@admin.register(SermonSeries)
class SermonSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    
@admin.register(SermonCategory)
class SermonCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'subcategory')
    search_fields = ('category',)

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date_preached', 'series')
    list_filter = ('date_preached', 'series', 'category')
    search_fields = ('title', 'preacher')
    date_hierarchy = 'date_preached'
    # prepopulated_fields = {'slug': ('title',)}  # Remove this line
    readonly_fields = ('created_at', 'updated',)
    # Additional customization as needed


@admin.register(SermonMedia)
class SermonMediaAdmin(admin.ModelAdmin):
    list_display = ('sermon', 'media_type', 'media_url')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('sermon', 'user', 'created_at')
    search_fields = ('sermon__title', 'user__username')
    readonly_fields = ('created_at', 'respond_at',)

class BaptizedCertificationAdmin(admin.ModelAdmin):
    list_display = ('user','given_full_name', 'baptism_date', 'qualified', 'applied_data', 'updated')
    list_filter = ('qualified', 'baptism_date', 'applied_data', 'updated')
    search_fields = ('given_full_name', 'fathers_full_name', 'mothers_full_name', 'phone_number')
    prepopulated_fields = {'slug': ('given_full_name',)}
    readonly_fields = ('service_request_confirmation_number', 'citification_request_confirmation_number')

admin.site.register(BaptizedCertification, BaptizedCertificationAdmin)


@admin.register(FatherOfRepentanceLists)
class FatherOfRepentanceListsAdmin(admin.ModelAdmin):
    list_display = (
    'full_name',
    'image',
    'location',
    'availability_days',
    'availability_hours',
    'church_serving',
    'title_serving',
    'experience_summary',
    'communication_preference',
    'communication_information', 
    'availability_states' , )

@admin.register(GroupMassageToSonOfRepentance)
class GroupMassageToSonOfRepentanceAdmin(admin.ModelAdmin):
    list_display = ('father_of_repentance', 'message', 'sent_at')
  
@admin.register(FuneralServicesApplication)
class FuneralServicesApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 
        'deceased_full_name', 
        'date_of_passing', 
        'church_name', 
        'preferred_date', 
        'is_paid', 
        'created', 
        'updated'
    )
    list_filter = ('is_paid', 'preferred_date', 'created')
    search_fields = ('full_name', 'deceased_full_name', 'phone_number', 'church_name')
    prepopulated_fields = {'slug': ('full_name',)}
    readonly_fields = ('created', 'updated')
    ordering = ('-created',)
