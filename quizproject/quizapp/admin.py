from django.urls import path
from django.contrib import admin,messages
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Course, Question, Result, Contact, UserProfile

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'password_display')

    def password_display(self, obj):
        return '********'
    password_display.short_description = 'Password'  

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:user_id>/change-password/',
                self.admin_site.admin_view(self.change_password),
                name='custom_change_password',
            ),
        ]
        return custom_urls + urls

    def change_password(self, request, user_id):
        user = User.objects.get(pk=user_id)
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            if new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, f"The password for {user.username} has been successfully changed.")
                
    def get_readonly_fields(self, request, obj=None):
        if obj and not obj.is_superuser:
            return ['password']
        return super().get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        if change and 'password' in form.cleaned_data and not obj.is_superuser:
            original_user = User.objects.get(pk=obj.pk)
            obj.password = original_user.password
        super().save_model(request, obj, form, change)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'question_number', 'total_marks')
    search_fields = ('course_name',)
    list_filter = ('course_name',)
    ordering = ('course_name',)
admin.site.register(Course, CourseAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('course', 'question', 'marks', 'answer')
    search_fields = ('question', 'course__course_name')  
    list_filter = ('course',)
    ordering = ('course',)
admin.site.register(Question, QuestionAdmin)


class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks', 'date')
    search_fields = ('student__username', 'exam__course_name')
    list_filter = ('exam', 'date')
    ordering = ('-date',)
admin.site.register(Result, ResultAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('phone_number',)

    @staticmethod
    def first_name(obj):
        return obj.user.first_name
    @staticmethod
    def last_name(obj):
        return obj.user.last_name
    @staticmethod
    def email(obj):
        return obj.user.email
admin.site.register(UserProfile, UserProfileAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email', 'message')
admin.site.register(Contact,ContactAdmin)


