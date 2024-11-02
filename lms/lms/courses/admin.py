from django.contrib import admin
from .models import Course, User,Assignment,Submission,Question,Quiz,Grade,Enrollment
# Register your models here.

admin.site.register(User)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Grade)
admin.site.register(Course)
admin.site.register(Enrollment)