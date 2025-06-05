# events/views.py
# from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView,UpdateView
from django.views import View
from .models import (
    Event, EventGallery, 
    PostEventImages,NewsAndAnnouncements,
    RemindMeUpcomingEvent,MarkedAsReadRemindMeNotification )# Import your new model
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.db import transaction
from django.db.models import Exists, OuterRef, Q
from django.views.generic.list import ListView

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'past_events'
    paginate_by = 10

    def get_queryset(self):
        now = timezone.now()
        
        # Use a transaction to ensure data consistency
        with transaction.atomic():
            # Update statuses using bulk operations
            past_events = Event.objects.filter(
                Q(end_time__lt=now) & ~Q(status_tag='past')
            )
            past_events.update(status_tag='past')
            
            Event.objects.filter(
                Q(end_time__gte=now) & ~Q(status_tag='active')
            ).update(status_tag='active')
            
            # Create missing galleries in bulk only for events we just updated to past
            if past_events.exists():
                # Get IDs of events we just updated
                updated_event_ids = past_events.values_list('id', flat=True)
                
                # Find which of these need galleries
                events_needing_gallery = Event.objects.filter(
                    id__in=updated_event_ids
                ).annotate(
                    has_gallery=Exists(
                        EventGallery.objects.filter(
                            post_events=OuterRef('pk'),
                            held_date=OuterRef('end_time__date')
                        )
                    )
                ).filter(has_gallery=False)
                
                galleries = [
                    EventGallery(
                        post_events=event,
                        number_of_participants=event.max_number_guests,
                        held_date=event.end_time.date(),
                        category=event.category,
                        thumbnail_title=event.title
                    ) for event in events_needing_gallery
                ]
                
                if galleries:
                    EventGallery.objects.bulk_create(galleries)
        
        # Return only past events for the main list
        return Event.objects.filter(status_tag='past').order_by('-end_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_events"] = Event.objects.filter(
            status_tag='active'
        ).order_by('start_time')
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

class EventGalleryListView(ListView):
    model = EventGallery
    template_name = 'events/event_gallery_list.html'
    context_object_name = 'galleries'
    paginate_by = 10  # Optional: Add pagination

class EventGalleryDetailView(DetailView):
    model = EventGallery
    template_name = 'events/event_gallery_detail.html'
    context_object_name = 'gallery'
    
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Increment the viewer count
        if obj.short_review :
            obj.viewers_count += 1
            obj.save(update_fields=['viewers_count'])  # Save only the updated field for efficiency
            
        return obj
    def get_context_data(self, **kwargs):
        # Fetch the base context from the superclass
        context = super().get_context_data(**kwargs)
        
        # Get the current EventGallery instance
        event_gallery = self.get_object()
        
        # Filter PostEventImages based on the current EventGallery instance
        context["postEvent_Images"] = PostEventImages.objects.filter(event_gallery=event_gallery)
        
        return context

# ListView for News & Announcements
class NewsAndAnnouncementsListView(ListView):
    model = NewsAndAnnouncements
    template_name = 'events/news_and_announcements_list.html'
    context_object_name = 'news_list'
    paginate_by = 10  # Adjust pagination as needed
    ordering = ['-created']  # Orders by latest first

# DetailView for News & Announcements
class NewsAndAnnouncementsDetailView(DetailView):
    model = NewsAndAnnouncements
    template_name = 'events/news_and_announcements_detail.html'
    context_object_name = 'news'

    def get_object(self):
        return get_object_or_404(NewsAndAnnouncements, slug=self.kwargs['slug'])
    
class UserNotificationListView(LoginRequiredMixin, ListView):
    model = RemindMeUpcomingEvent
    template_name = 'events/remind_me_note.html'
    context_object_name = 'remind_me_note'
    
    def get_queryset(self):
        return RemindMeUpcomingEvent.objects.filter(your_name=self.request.user, is_passed = False, is_viewed=False)
    
class AddRemindMeNotificationCreateView(LoginRequiredMixin, CreateView):
   
    def post(self, request, slug):
        # Fetch the upcoming event
        upcoming_event = get_object_or_404(Event, slug=slug)

        # Check if the RemindMeUpcomingEvent already exists
        remind_me_event, created = RemindMeUpcomingEvent.objects.get_or_create(
            event=upcoming_event,
            your_name=request.user,
        )
        
        # Redirect to the event list view after processing
        return redirect('events:event_list')
    
class MarkedAsReadRemindMeNotificationView(LoginRequiredMixin, View):
    """
    Creates or updates a record in MarkedAsReadRemindMeNotification
    to indicate that the current user has viewed a specific RemindMeUpcomingEvent.
    """
    def post(self, request, slug):
        # Fetch the upcoming event
        upcoming_event = get_object_or_404(RemindMeUpcomingEvent, slug=slug)

        # Create or update the 'read' status for the current user and event
        # If a record exists, it does nothing as is_read is always True
        # If it doesn't exist, it creates a new record.
        marked_as_read_entry, created = MarkedAsReadRemindMeNotification.objects.update_or_create(
            user=request.user,
            event=upcoming_event,
            defaults={'is_read': True} # This ensures it's always True if created/updated
        )

        # Optional: Add a success message
        if created:
            messages.success(request, f"Notification for '{upcoming_event.event_name}' marked as read.")
        else:
            messages.info(request, f"Notification for '{upcoming_event.event_name}' was already marked as read.")


        # Redirect to the event list view after processing
        return redirect('events:event_list')