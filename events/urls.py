# events/urls.py
from django.urls import path
from .views import (
    EventListView, EventDetailView, 
    EventGalleryListView, EventGalleryDetailView,
    NewsAndAnnouncementsListView, 
    NewsAndAnnouncementsDetailView,
    UserNotificationListView,
    AddRemindMeNotificationCreateView,
    MarkedAsReadRemindMeNotificationView,
    )

app_name = 'events' 

urlpatterns = [
    path('event_list', EventListView.as_view(), name='event_list'),
    path('event/<slug:slug>/', EventDetailView.as_view(), name='event_detail'),
    path('galleries/', EventGalleryListView.as_view(), name='event_gallery_list'),
    path('gallery/<slug:slug>/', EventGalleryDetailView.as_view(), name='event_gallery_detail'),
    path('NewsAndAnnouncements/', NewsAndAnnouncementsListView.as_view(), name='NewsAndAnnouncements_list'),
    path('NewsAndAnnouncements/<slug:slug>/', NewsAndAnnouncementsDetailView.as_view(), name='NewsAndAnnouncements_detail'),
    path('user/userNotification/', UserNotificationListView.as_view(), name='user-notification'),
    path('user/<slug:slug>/add-to-remind-me/', AddRemindMeNotificationCreateView.as_view(), name='add_remind_me'),
    path('event_mark-as-read/<slug:slug>/', MarkedAsReadRemindMeNotificationView.as_view(), name='mark_as_read'),
]
