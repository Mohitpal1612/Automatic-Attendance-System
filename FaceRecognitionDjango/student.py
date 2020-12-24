from django.shortcuts import render
from django.http import HttpResponse
import pymysql as mysql

def Actionstudentregister(request):
    return render(request,"student_register.html",{'msg':''})

def Actionsubmitstudent(request):
    roll=request.POST['roll']
    sname=request.POST['sname']
    spwd=request.POST['spwd']
    try:
        dbe = mysql.connect(host="localhost", port=3306,
                           user="root", password='123', db="face_recognition")
        cmd = dbe.cursor()
        q="insert into student (enrollment_no,student_name,student_password) values('{0}','{1}','{2}')".format(roll,sname,spwd)
        cmd.execute(q)
        dbe.commit()
        dbe.close()
        return render(request,"student_register.html",{'msg':'Record Submitted'})
    except Exception as e:
        print(e)
        return render(request, "student_register.html", {'msg': 'Fail to Submit Record'})

def  Actionstudentlogin(request):
    return render(request,"student_login.html",{'msg':''})

def  checkstudentlogin(request):
        dbe = mysql.connect(host="localhost", port=3306,
                        user="root", password='123', db="face_recognition")
        cmd = dbe.cursor()        
        q="select * from student where enrollment_no='{}' and student_password='{}'".format(request.POST['roll'],request.POST['spwd'])
        cmd.execute(q)
        row=cmd.fetchone()
        if(row==None):
            return render(request,'student_login.html',{'msg':'Invalid Credential'})
        else:
            roll=request.POST['roll']
            q="select student_name from student where enrollment_no='{}' ".format(request.POST['roll'])
            r = "select * from mark_attendance where enrollment_no='{}' ".format(request.POST['roll'])
            cmd.execute(r)
            rows = cmd.fetchall()
            dbe.commit()
            cmd.execute(q)
            sname=cmd.fetchone()            
            return render(request,'student_homepage.html',{'roll':roll,'sname':sname,'rows':rows})
            dbe.close()


def supdatepassword(request):
    return render(request, 'supdatepassword.html')


def Actionsforgotpassword(request):
    roll = request.POST['roll']
    # temail = request.POST['temail']
    spwd = request.POST['spwd']
    try:
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='123', db="face_recognition")
        cmd = dbe.cursor()
        q = "update student set student_password='{}' where enrollment_no='{}' " \
            .format(request.POST['spwd'], request.POST['roll'])
        cmd.execute(q)
        dbe.commit()
        dbe.close()
        return render(request, "student_login.html", {'msg': 'Record Updated'})
    except Exception as e:
        print(e)
        return render(request, "supdatepassword.html", {'msg': 'Fail to reset Password'})


def  Actionstudenthomepage(request):
    return render(request,"student_homepage.html")

