from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()

    def __str__(self):
        return self.course_name
    

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="questions")
    marks = models.PositiveIntegerField()
    question = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    class AnswerChoices(models.TextChoices):
        OPTION_1 = 'Option1', 'Option 1'
        OPTION_2 = 'Option2', 'Option 2'
        OPTION_3 = 'Option3', 'Option 3'
        OPTION_4 = 'Option4', 'Option 4'

    answer = models.CharField(
        max_length=200,
        choices=AnswerChoices.choices,
    )

    def __str__(self):
        return f"Question: {self.question} - {self.answer}"


class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.marks > self.exam.total_marks:
            raise ValidationError("Marks cannot exceed total marks of the exam.")
    
    def __str__(self):
        return f"{self.student.username} - {self.exam.course_name}"


def validate_phone_number(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError('Phone number must be exactly 10 digits.')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    
class Contact(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    message=models.TextField()
    phone = models.CharField(
        max_length=10, 
        validators=[validate_phone_number],
        help_text='Enter a 10-digit phone number')

    def __str__(self):  
        return self.name


