from django.shortcuts import render
from django.http import HttpResponse
import pymysql as mysql
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from datetime import date
import os 


def Actionteacherregister(request):
    return render(request,"teacher_register.html",{'msg':''})

def Actionsubmitteacher(request):
    tname=request.POST['tname']
    temail=request.POST['temail']
    tpwd=request.POST['tpwd']
    try:
        dbe = mysql.connect(host="localhost", port=3306,
                           user="root", password='123', db="face_recognition")
        cmd = dbe.cursor()
        q="insert into teacher(teacher_name,teacher_email,teacher_password) values('{0}','{1}','{2}')".format(tname,temail,tpwd)
        r="select *  from teacher where teacher_email='{}'".format(request.POST['temail'])
        cmd.execute(q)
        cmd.execute(r)
        rows=cmd.fetchall()
        dbe.commit()
        dbe.close()
        return render(request,"displayteacherid.html",{'rows':rows})
    except Exception as e:
        print(e)
        return render(request, "teacher_register.html", {'msg': 'Fail to Submit Record'})

def Actiondisplayteacherid(request):
       try:
              dbe = mysql.connect(host="localhost", port=3306,
                                  user="root", password='123', db="face_recognition")
              cmd = dbe.cursor()
              q="select *  from teacher where teacher_email='{}'".format(request.POST['temail'])
              cmd.execute(q)
              rows=cmd.fetchall()
              dbe.close()
              return render(request, "displayteacherid.html",{'rows':rows})
       except Exception as e:
              print(e)
              return render(request, "displayteacherid.html",{'rows':[]})
def  Actionteacherlogin(request):
    return render(request,"teacher_login.html",{'msg':''})

def  checkteacherlogin(request):
        dbe = mysql.connect(host="localhost", port=3306,
                        user="root", password='123', db="face_recognition")
        cmd = dbe.cursor()
        
        q="select * from teacher where teacher_id='{}' and teacher_password='{}'"\
            .format(request.POST['tid'],request.POST['tpwd'])
        cmd.execute(q)
        row=cmd.fetchone()
        if(row==None):
            return render(request,'teacher_login.html',{'msg':'Invalid Credential'})
        else:
            tid=request.POST['tid']
            q="select teacher_name from teacher where teacher_id='{}' ".format(request.POST['tid'])
            cmd.execute(q)
            tname=cmd.fetchone()            
            return render(request,'teacher_homepage.html',{'tid':tid,'tname':tname})
        db.close()

def tupdatepassword(request):
    return render(request,'tupdatepassword.html')

def Actiontforgotpassword(request):
    tid = request.POST['tid']
    #temail = request.POST['temail']
    tpwd = request.POST['tpwd']
    try:
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='123', db="face_recognition")
        cmd = dbe.cursor()
        q = "update teacher set teacher_password='{}' where teacher_id='{}' "\
            .format(request.POST['tpwd'],request.POST['tid'])
        cmd.execute(q)
        dbe.commit()
        dbe.close()
        return render(request,"teacher_login.html",{'msg':'Record Updated'})
    except Exception as e:
        print(e)
        return render(request, "tupdatepassword.html", {'msg': 'Fail to reset Password'})


def Actionteacherhomepage(request):
    file = request.FILES['pic']
    try:
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='123', db="face_recognition")
        cmd = dbe.cursor()
        q = "insert into pic values('{0}')".format(file.name)
        cmd.execute(q)
        dbe.commit()
        dbe.close()

        f=open("F:/FaceRecognition/FaceRecognitionDjango/UploadedPhoto/"+file.name,"wb")
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        return render(request,"teacher_homepage.html",{'msg':'Record Submitted'})
    except Exception as e:
        print(e)
        return render(request,"teacher_homepage.html",{'msg':'Fail to submit Record'})

def teacherdropdown(request):
    return render(request,"teacher_dropdown.html")   

def displaymarkedattendance(request):
    path = 'F:/FaceRecognition/FaceRecognitionDjango/UploadedPhoto/'
    images = []
    classNames = []
    myList = os.listdir(path)
    #print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    #print(classNames)
 
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList
 
    def markAttendance(name):
        try:       
            scode =request.POST['scode']
            tname =request.POST['tname']
            dbe = mysql.connect(host='localhost', port=3306, user='root',
                        password='123',db='face_recognition')
            cmd = dbe.cursor()
            now = datetime.now()
            dt = now.strftime("%a|%d-%m-%y")
            time = now.strftime('%H:%M:%S')
            q = "insert into mark_attendance(enrollment_no,subject_code,teacher_name,date,time)" \
                " values('{0}','{1}','{2}','{3}','{4}')"\
                .format(name,scode,tname,dt,time)
            cmd.execute(q)
            dbe.commit()
            dbe.close()
        except Exception as e:
            print("Error:",e)

 
    encodeListKnown = findEncodings(images)
    #print('Encoding Complete')
 
    cap = cv2.VideoCapture(0)
 
    while True:
        success, img = cap.read()
        #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
     
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame) 
 
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)
 
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()

                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
 
        cv2.imshow('Video',img)
    
        if cv2.waitKey(0) & 0xFF==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    try:
        dbe = mysql.connect(host="localhost", port=3306,
                            user="root", password='123', db="face_recognition")
        cmd = dbe.cursor()
        q="select *  from mark_attendance" 
        cmd.execute(q)
        rows=cmd.fetchall()
        dbe.close()
        return render(request, "displaymarkedattendance.html",{'rows':rows})
    except Exception as e:
        print(e)
        return render(request, "displaymarkedattendance.html",{'rows':[]})
    #return render(request, "displaymarkedattendance.html")
        
   
    





    



    