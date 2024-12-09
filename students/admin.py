from django.contrib import admin
from .models import Class, Student

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'name')
    search_fields = ('class_id', 'name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'class_group', 'score')
    list_filter = ('class_group',)
    search_fields = ('first_name', 'last_name')