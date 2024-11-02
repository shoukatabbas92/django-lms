from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Assignment,Submission,Question,Quiz,Grade,Enrollment,Course 

#for User registration 
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username','email','password1','password2','role','bio','profile_picture']

#course creation form
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        feilds = ['title','description','instructor','start_data','end_date','enrollment_limit']

#Enrollment Form
class EnrollmentForm(forms.Form):
    course =forms.ModelChoiceField(queryset=Course.objects.all())


#Assignment Form
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields =['title','description','due_date','course']


#Submission Form
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields =['assignment','file_upload','student','submission_date','feedback']


#Quiz Form
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title','description','course']

#Question Form
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz','questions','answer_choice','correct_answer']

#grade Form
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['user','course','assignment','quiz','score']