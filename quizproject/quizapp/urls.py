from django.urls import path
from .import views

app_name = 'quizapp'

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('studentregister/',views.studentregister,name='studentregister'),
    path('studentlogin/',views.studentlogin,name='studentlogin'),
    path('studentlogout/', views.studentlogout, name='studentlogout'), 
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('studentdashboard/', views.studentdashboard, name='studentdashboard'),
    path('complete_profile/', views.complete_profile, name='complete_profile'),
    path('start_exam/<int:course_id>/', views.start_exam, name='start_exam'),
    path('review-answer/<int:course_id>/',views.review_answer,name='review_answer'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('marks/<int:user_id>/', views.view_marks, name='view_mark'),
    path('delete_marks/<int:result_id>/', views.delete_marks, name='delete_marks'),
    path('add_course/', views.add_course, name='add_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('add_question/', views.add_question, name='add_question'),
    path('course-questions/<int:course_id>/', views.view_course_questions, name='view_course_questions'),
    path('delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('contact/', views.contact, name='contact'),
]


