from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import Course,Question,Result,Contact,UserProfile

# Create your views here.

def index(request):
    return render(request,"index.html")


def about(request):
    return render(request,"about.html")


def studentregister(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect("quizapp:studentregister") 
        if len(password) < 8:
            messages.add_message(request,messages.ERROR, "Password must be at least 8 characters long.", extra_tags="password-length-error")
            return redirect("quizapp:studentregister")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("quizapp:studentregister")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("quizapp:studentregister")

        user = User.objects.create(username=username,email=email,password=make_password(password))
        user.save()
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect("quizapp:studentlogin")  
    return render(request,"studentregister.html") 


def studentlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Both email and password fields are required.")
            return redirect("quizapp:studentlogin")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect("quizapp:studentlogin")

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_staff: 
                return redirect('quizapp:admindashboard')
            else:
                return redirect('quizapp:studentdashboard')
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect("quizapp:studentlogin")
    return render(request, "studentlogin.html")


def studentlogout(request):
    logout(request)  
    messages.success(request, "You have been logged out successfully.")
    return redirect("quizapp:studentlogin")


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if len(new_password) < 8:
            messages.error(request, "Your password must be at least 8 characters long.")
            return redirect('quizapp:forgot_password')
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect('quizapp:forgot_password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No user found with that email address.")
            return redirect('quizapp:forgot_password')

        user.set_password(new_password)
        user.save()
        # Update session auth hash to avoid the user getting logged out
        update_session_auth_hash(request, user)
        messages.success(request, "Your password has been successfully updated!")
        return redirect('quizapp:studentlogin')  
    return render(request,'forgot_password.html')  


@login_required
def studentdashboard(request):
    user = request.user
    courses = Course.objects.all()
    results = Result.objects.filter(student=user)
    total_questions = sum(course.question_number for course in courses)
    
    context = {'user': user,'courses': courses,'results': results, 'total_questions': total_questions,}
    return render(request, 'studentdashboard.html', context)


@login_required
def complete_profile(request):
    user = request.user
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")

        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        UserProfile.objects.update_or_create(user=user, defaults={"phone_number": phone_number},)
        return redirect("quizapp:studentdashboard")

    # Handle GET request to prefill form fields
    try:
        profile = user.profile  
        phone_number = profile.phone_number
    except UserProfile.DoesNotExist:
        phone_number = ""

    context = {"user": user, "phone_number": phone_number,}
    return render(request, "complete_profile.html", context)


@login_required
def start_exam(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(course=course)
    is_submitted = False
    total_marks = 0

    if request.method == "POST":
        for question in questions:
            selected_option = request.POST.get(f"question_{question.id}")
            if selected_option == question.answer:
                total_marks += question.marks
        
        Result.objects.create(student=request.user, exam=course, marks=total_marks)
        is_submitted = True
    
    if is_submitted:
        if total_marks == course.total_marks:
            performance = "Excellent work! You aced it! 🎉"
        elif total_marks >= course.total_marks / 2:
            performance = "Great job! You passed with flying colors! 😊"
        else:
            performance = "Keep practicing! You'll do better next time! 💪"
    else:
        performance = None

    context = {'course': course, 'questions': questions, 'is_submitted': is_submitted,
                'total_marks': total_marks, 'performance': performance,}
    return render(request, 'start_exam.html', context)


def review_answer(request,course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(course=course)

    context = { 'course': course, 'questions': questions, }
    return render(request, 'user_reviewanswers.html', context)


@user_passes_test(lambda user: user.is_staff)
@login_required
def admindashboard(request):
    users = User.objects.all() 
    total_user=User.objects.all().count()-1
    courses = Course.objects.all()
    total_questions = sum(course.question_number for course in courses)

    context= {'users':users, 'total_user':total_user,'courses':courses,'total_questions':total_questions}
    return render(request, "admindashboard.html",context)


def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
    return redirect(f"{reverse('quizapp:admindashboard')}?show=user-table")


def view_marks(request, user_id):
    user = get_object_or_404(User, id=user_id)
    results = Result.objects.filter(student=user)
    return render(request, 'admin_viewmark.html', {'user': user,'results':results})


def delete_marks(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    user_id = result.student.id  
    if request.method == 'POST':
        result.delete()
    return redirect('quizapp:view_mark', user_id=user_id)


def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        question_number = request.POST.get('question_number')
        total_marks = request.POST.get('total_marks')
        
        Course.objects.create(course_name=course_name, question_number=question_number, total_marks=total_marks)
    return redirect(f"{reverse('quizapp:admindashboard')}?show=course-section")


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect(f"{reverse('quizapp:admindashboard')}?show=course-section")


def add_question(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, id=course_id)
        question_text = request.POST.get('question')
        marks = request.POST.get('marks')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        answer = request.POST.get('answer')

        Question.objects.create(
            course=course,
            marks=marks,
            question=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            answer=answer
        )
        context={courses:courses}
    return redirect(f"{reverse('quizapp:admindashboard')}?show=Question-section",context)


def view_course_questions(request,course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(course=course)

    context = { 'course': course, 'questions': questions, }
    return render(request, 'admin_viewquestions.html', context)


def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    course_id = question.course.id
    question.delete()
    return redirect('quizapp:view_course_questions', course_id=course_id)


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']

        if len(phone) != 10:
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect('quizapp:contact')
        cont = Contact(name=name, phone=phone, email=email, message=message)
        cont.save()
        messages.success(request, 'Message sent successfully.')
    return render(request, "contact.html")

 
       