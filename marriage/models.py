from django.db import models
from django.conf import settings
from common.utils.text import unique_slug
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor.fields import RichTextField



# User Registration for the School
class SignupForSchool(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    confirmation = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(str(self.user), type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.city}'

# Progress Control for Users
class SchoolProgressController(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_signup_user_account = models.BooleanField(default=True)
    is_membership = models.BooleanField(default=True)
    is_signup_for_school = models.BooleanField(default=False)
    is_complete_courses = models.BooleanField(default=False)
    is_pass_quiz = models.BooleanField(default=False)
    is_attended_webinar = models.BooleanField(default=False)
    is_attended_onsite = models.BooleanField(default=False)
    is_certified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - Progress'


# Course and Quiz Models
class Course(models.Model):
    CATEGORY=( 
         ('PreMarital', 'PreMarital'),
         ('PostMarital', 'PostMarital'),  
     )
    title = models.CharField(max_length=200)
    category =models.CharField(max_length=50, choices=CATEGORY)
    #description = models.TextField()
    description = RichTextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.title, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Course Progress Control for Users
class CourseChapterProgressController(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_complete_courses_Chapter_detail = models.BooleanField(default=False)
    is_courses_Chapter_quiz_pass = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.user, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - CourseChapterProgress {self.course.title}'


# Subtitle Model
class Subtitle(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subtitles')
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.subtitle, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subtitle
    
class Quiz(models.Model):
    quiz_title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.quiz_title, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.quiz_title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    question_text = models.TextField(max_length=3000)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(f"{self.quiz.quiz_title}-{self.number}", type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quiz} - Question {self.number}"

class Answer(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text

class Results(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    is_pass = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.is_pass = self.score >= 80   # Assuming a pass mark of 4
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}'s result for {self.quiz}"

class Certification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    results = models.ForeignKey(Results, on_delete=models.CASCADE)
    is_passed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.results.is_pass:
            self.is_passed = True
            self.completion_date = timezone.now()
        else:
            self.is_passed = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.course}"

# Event and Registration Models
class MeetEvents(models.Model):
    MEET_TYPE_CHOICES = [
        ('Webinar', 'Webinar'),
        ('Onsite', 'Onsite'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meet_type = models.CharField(max_length=50, choices=MEET_TYPE_CHOICES)
    date_and_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    webinar_link = models.URLField(null=True, blank=True)
    webinar_password = models.CharField(max_length=100, null=True, blank=True)
    held_by = models.CharField(max_length=100)
    speaker = models.CharField(max_length=100)
    special_guest = models.CharField(max_length=100, null=True, blank=True)
    status_is_active =  models.BooleanField(default=True)
    max_participant = models.IntegerField()
    min_participant = models.IntegerField()
    is_cancelled = models.BooleanField(default=False)
    cancelled_reason = models.CharField(max_length=100, null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancelled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cancelled_events'
    )
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(f"{self.meet_type}-{self.date_and_time}", type(self))
   
        now = timezone.now()
        
        if self.end_time < now:
            self.status_is_active = False
        else:
            self.status_is_active = True
            
        if self.is_cancelled and not self.cancelled_at:
            self.cancelled_at = now 
        else:
            self.cancelled_at = None      
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.meet_type} - {self.date_and_time}"

class SignupForMeetEvents(models.Model):
    meet_events = models.ForeignKey(MeetEvents, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    confirmation = models.CharField(max_length=255, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    is_attended = models.BooleanField(default=False)
    attended_confirmation_code=models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(f"{self.user}-{self.meet_events}", type(self))
            
        if not self.confirmation:
             # Format the date to get the year in 'yy' format.
            formatted_date = timezone.now().strftime("%d%m%Y%H%M%S")
            self.confirmation = f'ME{formatted_date}'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.meet_events}"

# Resources Model
class Resources(models.Model):
    CATEGORY=( 
         ('PreMarital', 'PreMarital'),
         ('PostMarital', 'PostMarital'),  
     )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category =models.CharField(max_length=50, choices=CATEGORY, default='PreMarital')
    audio = models.FileField(upload_to='resources/audio/', null=True, blank=True)
    video = models.FileField(upload_to='resources/video/', null=True, blank=True)
    pdf = models.FileField(upload_to='resources/pdf/', null=True, blank=True)
    image = models.ImageField(upload_to='resources/images/', null=True, blank=True)
    links = models.URLField(null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.title, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class marriageQuationsAndAnswer(models.Model):
    VIEWED_TYPES =(
        ('public', 'public'),
        ('private', 'private'),  
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Replace 'YourCourseModel' with your actual course model
    question = models.TextField(max_length=2000)
    answer = models.TextField(blank=True, null=True)
    is_answered= models.BooleanField(default=False)
    viewed_by = models.CharField(max_length=100, default='private', choices=VIEWED_TYPES)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
      
    def save(self, *args, **kwargs):    
        if self.answer:
            self.is_answered = True
        if not self.answer:
            self.is_answered = False
            
        if not self.slug:
            value = f"{self.user.username}-QA"
            self.slug = unique_slug(value, type(self))
       
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Question by {self.user.username} on {self.course.title}"