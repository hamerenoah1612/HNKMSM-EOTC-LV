from django.contrib import admin
from .models import *


admin.site.register(SignupForSchool)
admin.site.register(SchoolProgressController)
admin.site.register(Course)
admin.site.register(CourseChapterProgressController)
admin.site.register(Subtitle)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Results)
admin.site.register(Certification)
admin.site.register(MeetEvents)
admin.site.register(SignupForMeetEvents)
admin.site.register(Resources)
class marriageQuationsAndAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'viewed_by', 'is_answered' ,'question', 'answer')  # Add 'is_answered' to the list display

    def is_answered(self, obj):
        return obj.answer is not None
    is_answered.boolean = True  # Displays a nice True/False icon instead of "True"/"False"
    is_answered.short_description = 'Answered'  # Custom column header name
admin.site.register(marriageQuationsAndAnswer,marriageQuationsAndAnswerAdmin)
