from django.urls import path
from .views import (marriageSchoolWelcome,CourseListView,
                    CourseDetailView,ResultsListView, 
                    ResourceDetailView , submit_quiz, 
                    marriageSchoolQA,QuationsAndAnswer_confirmation,
                    MeetEventListView,MeetEventDetailView,
                    signup_for_event,
                    canceled_for_event
                    )

app_name = 'marriage' 

urlpatterns = [
    # path('marriageSchoolWelcome', marriageSchoolWelcome.as_view(), name='marriageSchool_welcome'),
    path('marriageSchoolWelcome/', marriageSchoolWelcome.as_view(), name='marriageSchool_welcome'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/results/', ResultsListView.as_view(), name='results_list'),
    path('courses/resource/<slug:slug>/', ResourceDetailView.as_view(), name='resource_detail'),
    path('marriage_quations_answers_create/', marriageSchoolQA.as_view(), name='quations_answers_create'),
    path('confirmation/',QuationsAndAnswer_confirmation.as_view(), name='quationsAndAnswer_confirmation'),
    path('quiz/submit/<int:quiz_id>/', submit_quiz, name='submit_quiz'),
    path('meet_events/', MeetEventListView.as_view(), name='meet_event_list'),
    path('meet_events/<slug:slug>/', MeetEventDetailView.as_view(), name='meet_event_detail'),
    path('meet_events/<slug:slug>/signup/', signup_for_event, name='signup_for_event'),
    path('meet_events/<slug:slug>/canceled/', canceled_for_event, name='canceled_for_event')
]