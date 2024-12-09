from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('students.urls')),
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
]

handler404 = 'students.views.custom_404'