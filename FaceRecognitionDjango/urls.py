"""FaceRecognitionDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.views.static import serve
from django.conf.urls import url
from . import student
from . import teacher
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.dashboard),
    path('dashboard/',views.dashboard),  
    path('student_register/',student.Actionstudentregister),
    path('studentsubmit',student.Actionsubmitstudent),
    path('student_login/',student.Actionstudentlogin),
    path('checkstudentlogin',student.checkstudentlogin),    
    path('student_homepage/',student.Actionstudenthomepage),
    path('teacher_register/',teacher.Actionteacherregister),
    path('teachersubmit',teacher.Actionsubmitteacher),
    path('teacher_login/',teacher.Actionteacherlogin),
    path('checkteacherlogin',teacher.checkteacherlogin),
    path('sforgotpassword',student.Actionsforgotpassword),
    path('supdatepassword/',student.supdatepassword),
    path('tforgotpassword',teacher.Actiontforgotpassword),
    path('tupdatepassword/',teacher.tupdatepassword),
    path('displayteacherid/',teacher.Actiondisplayteacherid),
    path('checkupload',teacher.Actionteacherhomepage),
    path('teacher_dropdown/',teacher.teacherdropdown),
    path('displaymarkedattendance',teacher.displaymarkedattendance), 
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
urlpatterns+=staticfiles_urlpatterns()
