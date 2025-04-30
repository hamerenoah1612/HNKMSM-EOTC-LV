from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView,TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import (Course, Quiz, Question, 
                     Answer, Results, Resources, 
                     SchoolProgressController,
                     Certification,MeetEvents,
                     marriageQuationsAndAnswer,
                     SignupForSchool,
                     CourseChapterProgressController,
                     SignupForMeetEvents
                )
from .forms import SignupForSchoolForm,marriageSchoolQuationsAndAnswerForm

class marriageSchoolWelcome(LoginRequiredMixin,TemplateView):
    template_name = 'marriage/marriageView.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Handle objects that may not exist for the user
        try:
            schoolProgressController = SchoolProgressController.objects.get(user=user)
            course = Course.objects.all().count()
            results = Results.objects.filter(user=user).count()
            #update the schoolProgressController
            if course == results:
               schoolProgressController.is_complete_courses = True
               schoolProgressController.is_pass_quiz = True
               schoolProgressController.save()
               
        except SchoolProgressController.DoesNotExist:
           context['schoolProgressController'] = None  # or some default value
        
        try:
            school_progress = SchoolProgressController.objects.get(user=user)
        except SchoolProgressController.DoesNotExist:
            school_progress = None

        if school_progress:
            total_steps = 6  # Total number of steps represented by the boolean fields
            completed_steps = sum([
                school_progress.is_signup_for_school,
                school_progress.is_complete_courses,
                school_progress.is_pass_quiz,
                school_progress.is_attended_webinar,
                school_progress.is_attended_onsite,
                school_progress.is_certified,
            ])
            progress_percentage = (completed_steps / total_steps) * 100
        else:
            progress_percentage = 0

        context['progress_percentage'] = progress_percentage
        context['schoolProgressController'] = school_progress

        try:
            context['results'] = Results.objects.filter(user=user).first()
        except Results.DoesNotExist:
            context['results'] = None  # or some default value

        try:
            context['certification'] = Certification.objects.get(user=user)
        except Certification.DoesNotExist:
            context['certification'] = None  # or some default value

        # MeetEvents is a queryset, so no need for get_object_or_404
        context['meetEvents'] = MeetEvents.objects.filter(user=user)

        # Instantiate the signup form
        context['signupForSchoolForm'] = SignupForSchoolForm()

        return context
    
    def post(self, request, *args, **kwargs):
        form = SignupForSchoolForm(request.POST)
        SchoolProgress, created = SchoolProgressController.objects.get_or_create(user=self.request.user)
        
        if form.is_valid():
            signup = form.save(commit=False)
            signup.user = request.user
            signup.save()
            
            # Update SchoolProgressController
            SchoolProgress.is_signup_for_school = True
            SchoolProgress.save()
            
            return redirect('marriage:marriageSchool_welcome')

        context = self.get_context_data(**kwargs)
        context['signupForSchoolForm'] = form
        return self.render_to_response(context)
    
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'marriage/course_list.html'
    context_object_name = 'courses'
    # paginate_by = 6  # Number of courses per page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
       
        # Create a dictionary of course: result pairs
        context['results'] = {course: Results.objects.filter(user=user, course=course).first() for course in context['courses']} 
        context['resources_pre'] = Resources.objects.filter(category = 'PreMarital')
        context['resources_post'] = Resources.objects.filter(category = 'PostMarital')
        context['progress'] = CourseChapterProgressController.objects.filter(user=user)
        return context
    
class CourseDetailView(LoginRequiredMixin, DetailView): 
    model = Course
    template_name = 'marriage/course_detail.html'  # Specify your detail view template
    context_object_name = 'course_detail'
    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        course = self.get_object()  # Get the current course object
        if course.is_completed == True:
            context['quizzes'] = Quiz.objects.filter(course=course)
            context['questions'] = Question.objects.filter(course=course)
            context['answers'] = Answer.objects.filter(question__course=course)
            context['resources'] = Resources.objects.all()
            context['result'] = Results.objects.filter(user=self.request.user, course=course).order_by('-updated_at')
            context['is_quizzes_taken'] = Results.objects.filter(user=self.request.user, course=course).exists()
            # Filter quationsAndAnswer by the current course
            context['quationsAnswerData'] = marriageQuationsAndAnswer.objects.filter(course=course).order_by('created')
            context['progress'] = UpdateCourseChapterDetailClicked(course,user=self.request.user, is_Chapter =True, is_quiz = False)
        else: 
            context['course_content'] = course
        return context
    
def UpdateCourseChapterDetailClicked(course, user, is_Chapter , is_quiz ):
    # Get or create the progress record for this user and course
    if is_Chapter == True:
        progress, created = CourseChapterProgressController.objects.get_or_create(
            user=user,
            course=course,
            defaults={
                'is_complete_courses_Chapter_detail': True,
                'slug': None  # The save() method will handle the slug
            }
        )
        
        # If the record already existed, update it
        if not created:
            progress.is_complete_courses_Chapter_detail = True
            progress.save()
            
    if is_quiz :
        progress, created = CourseChapterProgressController.objects.get_or_create(
            user=user,
            course=course,
            defaults={
                'is_courses_Chapter_quiz_pass': True,
                'slug': None  # The save() method will handle the slug
            }
        )
        
        # If the record already existed, update it
        if not created:
            progress.is_courses_Chapter_quiz_pass = True
            progress.save()
            
    return progress
       
class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resources
    template_name = 'marriage/resources_detail.html'  # Specify your detail view template
    context_object_name = 'resources_detail'
     
class ResultsListView(LoginRequiredMixin, ListView):
    model = Results
    template_name = 'marriage/results_list.html'
    context_object_name = 'results_list'
     
    def get_queryset(self):
        return Results.objects.filter(user=self.request.user)

class marriageSchoolQA(LoginRequiredMixin, View):
    
    def post(self, request):
        
        if 'questions_and_answers' in request.POST: 
            form = marriageSchoolQuationsAndAnswerForm(request.POST)
            if form.is_valid():
                user = request.user
                course_id = request.POST.get('course')  # Assuming you have a hidden input with course_id in the form
                course = Course.objects.get(id=course_id)
                # Save the question to the database
                question = form.save(commit=False)
                question.user = user
                question.course = course
                question.save()
                return redirect('marriage:quationsAndAnswer_confirmation')
        else:
            context = {
                'quationsAnAnswerForm': marriageSchoolQuationsAndAnswerForm()
                }
            return render(request, self.template_name, context)
         
class QuationsAndAnswer_confirmation(TemplateView, LoginRequiredMixin):
    template_name = 'marriage/quationsAndAnswer_confirmation.html'
    
class MeetEventListView(ListView):
    model = MeetEvents
    template_name = 'marriage/meet_event_list.html'  # Specify the template to use
    context_object_name = 'meet_events'
    paginate_by = 10  # Add pagination if you have many events

    def get_queryset(self):
        # Filter to show only active events
        return MeetEvents.objects.filter(status='active').order_by('-date_and_time')

class MeetEventDetailView(DetailView):
    model = MeetEvents
    template_name = 'marriage/meet_event_detail.html'  # Specify the template to use
    context_object_name = 'meet_event'

# @login_required
# def signup_for_event(request, event_slug):
#     meet_event = get_object_or_404(MeetEvents, slug=event_slug)
    
#     # Check if the user has already signed up for the event
#     if SignupForMeetEvents.objects.filter(meet_events=meet_event, user=request.user).exists():
#         messages.warning(request, "You have already signed up for this event.")
#     else:
#         signup = SignupForMeetEvents(meet_events=meet_event, user=request.user)
#         signup.save()
#         messages.success(request, "You have successfully signed up for the event.")
    
#     return redirect('marriage:meet_event_detail', event_slug=event_slug)

@login_required
def signup_for_event(request, slug):
    # Fetch the event using the slug
    event = get_object_or_404(MeetEvents, slug=slug)

    # Check if the user has already signed up
    if SignupForMeetEvents.objects.filter(user=request.user, meet_events=event).exists():
        
        messages.info(request, "You have already signed up for this event.")
        # Optionally, handle the case where the user is already signed up
        return redirect('marriage:meet_event_detail', slug=slug)

    # Create a new signup instance
    signup = SignupForMeetEvents(user=request.user, meet_events=event)
    signup.save()
    messages.success(request, "You have successfully signed up for the event.")
    # Redirect to a confirmation page or the event detail page
    return redirect('marriage:meet_event_detail', slug=slug)


@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    course = quiz.course
    total_questions = Question.objects.filter(quiz=quiz).count()
    correct_answers = 0

    if request.method == 'POST':
        for question in quiz.question_set.all():
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                selected_answer = get_object_or_404(Answer, id=selected_answer_id)
                if selected_answer.is_correct:
                    correct_answers += 1

        score = (correct_answers * 100 ) / total_questions   # Scale to a score out of 5
        result, created = Results.objects.get_or_create(user=request.user, quiz=quiz, course=course)
        result.score = score
        result.save()
        if created:
            UpdateCourseChapterDetailClicked(course,user=request.user, is_Chapter=False, is_quiz=True)
        return redirect('marriage:course_detail', slug=course.slug)
    return render(request, 'marriage/course_detail.html', {'course_detail': course})
