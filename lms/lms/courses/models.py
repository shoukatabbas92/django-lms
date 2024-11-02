from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
# Create your models here.

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('instructor','Instructor'),
        ('student','Student'),
    ]
    role = models.CharField(max_length=10,choices=ROLE_CHOICES)
    bio = models.TextField(blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True,null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role':'instructor'})
    start_date = models.DateField()
    end_date = models.DateField()
    enrollment_limt = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
class Enrollment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role':'student'})
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    enrollment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} Enroll in {self.course.title}'
    
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='assignment')

    def __str__(self):
        return f'{self.title} for {self.course.title}'
    
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    student = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role':'student'})
    file_upload = models.FileField(upload_to='submission/',blank=True,null=True)
    submission_date = models.DateField(default=timezone.now)
    feedback = models.TextField(blank=True,null=True)

    def __str__(self):
        return f'Submission By {self.student.assignment} {self.assignment.title}'
    

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='quizzes')

    def __str__(self):
        return f'{self.title} For  {self.course.title}'
    

class Question(models.Model):
    quiz = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'questions')
    questions = models.TextField()
    answer_choice = models.JSONField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f'Questions For {self.quiz.title}'
    
class Grade(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment,on_delete=models.SET_NULL,blank=True,null=True)
    quiz = models.ForeignKey(Quiz,on_delete=models.SET_NULL,blank=True,null=True)
    score = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return f'{self.user.username} in {self.course.title}'
    

