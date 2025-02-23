from random import sample
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from .models import FAQ, Course, Chapter, FAQReader, FaqRelatedResource, Quiz, Question, Answer, Resources, Result, Report,Progress,QuationsAndAnswer
from .forms import QuationsAndAnswerForm , FAQReaderForm
# Create your views here.
class SchoolsView(TemplateView):
    template_name = 'schools/schoolsView.html'
    

#SchoolsChildrenS
class SchoolsChildrenSchool(LoginRequiredMixin, View):
    template_name = 'schools/childrenSchool.html'

    def get(self, request):
        courses = Course.objects.all().order_by('created_at')
        chapters = Chapter.objects.all().order_by('created_at')
        reports = Report.objects.filter(user=self.request.user)
        progress = Progress.objects.filter(user=self.request.user)
        result = Result.objects.filter(user=self.request.user)
        quationsAndAnswer = QuationsAndAnswer.objects.filter(user=self.request.user)
        quationsAndAnswerAll = QuationsAndAnswer.objects.all().order_by('updated')
        quationsAnAnswerForm = QuationsAndAnswerForm()
        faqs = FAQ.objects.all()
        faqRelatedResource = FaqRelatedResource.objects.all()
        faq_reader_form = FAQReaderForm()
        fqaReader= FAQReader.objects.filter(user=self.request.user)
        chapters_with_resources = []
                   
        for chapter in chapters:
            resources = Resources.objects.filter(chapter=chapter)
            quizzes = Quiz.objects.filter(chapter=chapter)
           
            get_questions = Question.objects.filter(quiz__chapter=chapter)
            
            # Generate random questions
            if len(get_questions) > 5:
                # if have more than 5 questions we gen have random 5 questions 
                questions = sample(list(get_questions), min(5, len(get_questions)))  
                
            else : 
                questions = get_questions
            
            if chapter.course.school_type == 'sundaySchoolChildren':
                is_children = True
            else:
                is_children = False
            chapters_with_resources.append({
                 'chapter': chapter, 
                 'resources': resources, 
                 'quizzes': quizzes, 
                 'questions': questions, 
                 'reports': reports,
                 })
        # print(chapters_with_resources)               
        context = {
            'is_children':is_children,
            'chapters_with_resources': chapters_with_resources, 
            'courses': courses,
            'chapters': chapters,
            'progress' : progress,
            'results' : result,
            'reports' : reports,
            'quationsAndAnswer': quationsAndAnswer,
            'quationsAnAnswerForm':quationsAnAnswerForm,
            'quationsAndAnswerAll':quationsAndAnswerAll,
            'faqs': faqs,
            'faq_reader_form': faq_reader_form,
            'fqaReader' : fqaReader,
            'faqRelatedResource' : faqRelatedResource
            
        }
        return render(request, self.template_name, context)
    
    # def post(self, request):
    #     context={}
    #     return render(request, self.template_name, context)
        
    def post(self, request):
        
        if 'course_id' in request.POST:
            user = request.user
            course_id = request.POST.get('course_id')
            course = Course.objects.get(id=course_id)
            progress, created = Progress.objects.get_or_create(user=user, course=course)
            # progress = Progress.objects.create(user=user, course=course)
            progress.is_chapter_completed = True
            progress.save()
            return redirect('schools:childrenSchool')
        
        elif 'course_id_retake' in request.POST:
            user = request.user
            course_id = request.POST.get('course_id_retake')
            course = Course.objects.get(id=course_id)
            progress, created = Progress.objects.get_or_create(user=user, course=course)
            # progress = Progress.objects.create(user=user, course=course)
            progress.is_chapter_completed = False
            progress.is_quiz_completed = False
            progress.save()
            return redirect('schools:childrenSchool')
        
        elif 'quiz_id' in request.POST:
            user = request.user
            quiz_id = request.POST.get('quiz_id')
            score = self.calculate_score(request)
            quiz = Quiz.objects.get(id=quiz_id)
            # Check if the user has already taken this quiz
            is_result_exist = Result.objects.filter(user=user, quiz=quiz)
            if not is_result_exist :
                result, created = Result.objects.get_or_create(user=user, quiz=quiz, score=score)
            else: 
                result, created = Result.objects.get_or_create(user=user, quiz=quiz)
                if result.score < score :
                   result.score = score
            result.save()
            # Update or create progress
            progress, created = Progress.objects.get_or_create(user=user, course=quiz.chapter.course)
            progress.is_quiz_completed = True
            progress.is_chapter_completed= True
            progress.save()
            
            # Update or create report
            report, created = Report.objects.get_or_create(user=user, chapter=quiz.chapter,defaults={'completion_date': timezone.now()})
            report.save()
            return redirect('schools:childrenSchool')
        
        elif 'user_questions' in request.POST: 
            form = QuationsAndAnswerForm(request.POST)
            if form.is_valid():
                user = request.user
                course_id = request.POST.get('course')  # Assuming you have a hidden input with course_id in the form
                course = Course.objects.get(id=course_id)
                # Save the question to the database
                question = form.save(commit=False)
                question.user = user
                question.course = course
                question.save()
                return redirect('schools:childrenSchool')
            
        elif 'faq_id' in request.POST:
            form = FAQReaderForm(request.POST)
            if form.is_valid():
                user = request.user
                faq_id = request.POST.get('faq_id') 
                faq = FAQ.objects.get(id=faq_id)
                # Save the question to the database
                faq_reader, created = FAQReader.objects.get_or_create(user=user, faq_id=faq_id)
                faq_reader.satisfaction_rating = form.cleaned_data['satisfaction_rating']
                faq.is_satisfied = True
                faq_reader.save()
                # Save the changes
                faq.save()
                return redirect('schools:childrenSchool')
            
        else:
            context = {
                'quationsAnAnswerForm': QuationsAndAnswerForm()
                }
            return render(request, self.template_name, context)

    def calculate_score(self, request):
        score = 0
        for key, value in request.POST.items():
            if key.startswith('question') and value.isdigit():
                question_id = int(key.split('question')[1])
                selected_answer_id = int(value)
                question = Question.objects.get(id=question_id)
                correct_answer = question.answer_set.get(is_correct=True)
                if selected_answer_id == correct_answer.id:
                    score += 1
        return score
    
#SchoolsYouthSchool
class SchoolsYouthSchool(LoginRequiredMixin,View):
    template_name = 'schools/youthSchool.html'
    
    def get(self, request):
        courses = Course.objects.all().order_by('created_at')
        chapters = Chapter.objects.all().order_by('created_at')
        reports = Report.objects.filter(user=self.request.user)
        progress = Progress.objects.filter(user=self.request.user)
        result = Result.objects.filter(user=self.request.user)
        quationsAndAnswer = QuationsAndAnswer.objects.filter(user=self.request.user)
        quationsAndAnswerAll = QuationsAndAnswer.objects.all().order_by('updated')
        quationsAnAnswerForm = QuationsAndAnswerForm()
        faqs = FAQ.objects.all()
        faqRelatedResource = FaqRelatedResource.objects.all()
        faq_reader_form = FAQReaderForm()
        fqaReader= FAQReader.objects.filter(user=self.request.user)
        chapters_with_resources = []
                   
        for chapter in chapters:
            resources = Resources.objects.filter(chapter=chapter)
            quizzes = Quiz.objects.filter(chapter=chapter)
            get_questions = Question.objects.filter(quiz__chapter=chapter)
            
            # Generate random questions
            if len(get_questions) > 5:
                # if have more than 5 questions we gen have random 5 questions 
                questions = sample(list(get_questions), min(5, len(get_questions)))  
            else : 
                questions = get_questions
            
            if chapter.course.school_type == 'sundaySchoolYouth':
                is_youth = True
            else:
                is_youth = False
            chapters_with_resources.append({
                 'chapter': chapter, 
                 'resources': resources, 
                 'quizzes': quizzes, 
                 'questions': questions, 
                 'reports': reports,
                 })
                       
        context = {
            'is_youth' : is_youth,
            'chapters_with_resources': chapters_with_resources, 
            'courses': courses,
            'chapters': chapters,
            'progress' : progress,
            'results' : result,
            'reports' : reports,
            'quationsAndAnswer': quationsAndAnswer,
            'quationsAnAnswerForm':quationsAnAnswerForm,
            'quationsAndAnswerAll':quationsAndAnswerAll,
            'faqs': faqs,
            'faq_reader_form': faq_reader_form,
            'fqaReader' : fqaReader,
            'faqRelatedResource' : faqRelatedResource
            
        }
        return render(request, self.template_name, context)
    
    # def post(self, request):
    #     context={}
    #     return render(request, self.template_name, context)
        
    def post(self, request):
        
        if 'course_id' in request.POST:
            user = request.user
            course_id = request.POST.get('course_id')
            course = Course.objects.get(id=course_id)
            progress, created = Progress.objects.get_or_create(user=user, course=course)
            # progress = Progress.objects.create(user=user, course=course)
            progress.is_chapter_completed = True
            progress.save()
            return redirect('schools:youthSchool')
        
        elif 'course_id_retake' in request.POST:
            user = request.user
            course_id = request.POST.get('course_id_retake')
            course = Course.objects.get(id=course_id)
            progress, created = Progress.objects.get_or_create(user=user, course=course)
            # progress = Progress.objects.create(user=user, course=course)
            progress.is_chapter_completed = False
            progress.is_quiz_completed = False
            progress.save()
            return redirect('schools:youthSchool')
        
        elif 'quiz_id' in request.POST:
            user = request.user
            quiz_id = request.POST.get('quiz_id')
            score = self.calculate_score(request)
            quiz = Quiz.objects.get(id=quiz_id)
            # Check if the user has already taken this quiz
            is_result_exist = Result.objects.filter(user=user, quiz=quiz)
            if not is_result_exist :
                result, created = Result.objects.get_or_create(user=user, quiz=quiz, score=score)
            else: 
                result, created = Result.objects.get_or_create(user=user, quiz=quiz)
                if result.score < score :
                   result.score = score
            result.save()
            # Update or create progress
            progress, created = Progress.objects.get_or_create(user=user, course=quiz.chapter.course)
            progress.is_quiz_completed = True
            progress.is_chapter_completed= True
            progress.save()
            
            # Update or create report
            report, created = Report.objects.get_or_create(user=user, chapter=quiz.chapter,defaults={'completion_date': timezone.now()})
            report.save()
            return redirect('schools:youthSchool')
        
        elif 'user_questions' in request.POST: 
            form = QuationsAndAnswerForm(request.POST)
            if form.is_valid():
                user = request.user
                course_id = request.POST.get('course')  # Assuming you have a hidden input with course_id in the form
                course = Course.objects.get(id=course_id)
                # Save the question to the database
                question = form.save(commit=False)
                question.user = user
                question.course = course
                question.save()
                return redirect('schools:youthSchool')
            
        elif 'faq_id' in request.POST:
            form = FAQReaderForm(request.POST)
            if form.is_valid():
                user = request.user
                faq_id = request.POST.get('faq_id') 
                faq = FAQ.objects.get(id=faq_id)
                # Save the question to the database
                faq_reader, created = FAQReader.objects.get_or_create(user=user, faq_id=faq_id)
                faq_reader.satisfaction_rating = form.cleaned_data['satisfaction_rating']
                faq.is_satisfied = True
                faq_reader.save()
                # Save the changes
                faq.save()
                return redirect('schools:youthSchool')
            
        else:
            context = {
                'quationsAnAnswerForm': QuationsAndAnswerForm()
                }
            return render(request, self.template_name, context)

    def calculate_score(self, request):
        score = 0
        for key, value in request.POST.items():
            if key.startswith('question') and value.isdigit():
                question_id = int(key.split('question')[1])
                selected_answer_id = int(value)
                question = Question.objects.get(id=question_id)
                correct_answer = question.answer_set.get(is_correct=True)
                if selected_answer_id == correct_answer.id:
                    score += 1
        return score
    
      
      

 