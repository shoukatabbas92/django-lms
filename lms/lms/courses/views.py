from django.shortcuts import render,redirect,get_object_or_404
from .models import Assignment,Submission,Course,Question,Quiz,Enrollment,Grade
from .forms import UserRegistrationForm, AssignmentForm,SubmissionForm,CourseForm,QuestionForm,QuizForm,EnrollmentForm,GradeForm
from django.views import View
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class RegisterView(View):
    def get(self,request):
        form = UserRegistrationForm()
        return render(request,'registration/register.html',{'form':form})

    
    def post(self,request):
        form = UserRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1']) 
            user.save()
            return redirect('course_list')
        return render(request,'registration/register.html')
    
# Course list View  
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_view.html'
    context_object_name = 'courses'


# Course detail View 
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'


#Course Creation veiw for instructor
@method_decorator(login_required,name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)
    

#Enrollment 
@login_required
def enrol_in_course(request,course_id):
    course = get_object_or_404(Course,pk=course_id)
    if request.method == 'POST':
        Enrollment.objects.create(user = request.user,course_id=course_id)
        return redirect('course_detail', pk=course_id)
    return render(request,'courses/enroll.html',{'course':course})


#assignment creation view
@method_decorator(login_required,name='dispatch')
class AssignmentCreateView(CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/assigement_form.html'

    def form_valid(self, form):
        form.instance.course = get_object_or_404(Course,id=self.kwargs['course_id'])
        return super().form_valid(form)
    
#submission creation
@login_required 
def sub_assignment(request,assignment_id):
    assignment =get_object_or_404(Assignment,id=assignment_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            submission =form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.save()
            return redirect('assignment_detail',pk =assignment_id)
        else:
            form = SubmissionForm()
        return render(request,'assignments/submission_form.html',{'form':form , 'assignment':assignment})

#Quiz Creation View
@method_decorator(login_required,name='dispatch')
class QuizCreationView(CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quizzes/quiz_form.html'

    def form_valid(self, form):
        form.instance.course = get_object_or_404(Course,id=self.kwargs['course_id'])
        return super().form_valid(form)


# Question Creation View
@method_decorator(login_required,name='dispatch')
class QuestionCreationView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'qaizzes/question_form.html'

    def form_valid(self, form):
        form.instance.quiz = get_object_or_404(Quiz,id=self.kwargs['quiz_if'])
        return super().form_valid(form)

#Grade Assignment
@login_required
def grade_submission(request,submission_id):
    submission =get_object_or_404(Submission,id= submission_id)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.user = submission.student
            grade.assignment = submission.student
            grade.sava()
            return redirect('submission_detail',submission_id)
        else:
            form = GradeForm()
        return render(request,'grades/grade_form.html',{'form':form,'submission':submission})

#Profile 
@login_required
def Profile_view(request):
    user_courses = Enrollment.objects.filter(user=request.user)
    user_grade = Grade.objects.filter(user = request.user)
    return render(request,'profile.html',{'user_courses':user_courses,'user_grade':user_grade})


