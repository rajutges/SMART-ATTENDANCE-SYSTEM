"""this code in coded by Raju Ranjan
A pre final yer student at NATIONAL INSTITUTE OF TECHNOLOY PATNA"""
"""this is the code for attendance system which detects faces and mark attendance according to that"""



#inmporting libraries used in the code
import cv2  # importing opencv library
import numpy as np   
import face_recognition
import os
import time      
from datetime import datetime  #imported datetime library for detection of date and time
c=input("FOR NEW SESSION PRESS 'y' \n want to terminate?   ......press x \n   if no press other than x and y       ")

#ASK THE USER WEATHER USER WANTS A NEW SESSION SO THAT IT WILL CREATE A NEW EXCEL SHEET NAMED AS THE NEW DATE
if c=='y':
    today=datetime.today() 
    Attendance = today.strftime("%b-%d-%Y") 
    v=Attendance+'.'+'csv'
    f = open(v, 'w+')
    f.truncate(0)
else:
    
    if c=="x":
        sys.exit(0)
    else:
        today=datetime.today() 
        Attendance = today.strftime("%b-%d-%Y") 
        v=Attendance+'.'+'csv'
        f = open(v, 'w+')

 
    
path='dataset'  #DATASET
images=[]
classNames=[]
roLL=['EC501','EC502','EC503','EC504','EC505','EC506']

rollList={'ankit':'EC501','arya':'EC502','muskan':'EC503','raju':'EC504','anuu':'EC505',"nutan":'EC506'}  #ROLLSHEET (ADDED FOR BETTER FEATURE IN ATTENDANCE MARKING)


mylist=os.listdir(path) #read the file in the directory
print("the database contains : ")
print(mylist)

for cls in mylist:
    images.append(cv2.imread(str(path)+'/'+str(cls)))
    classNames.append(os.path.splitext(cls)[0])

print("the names of students")
print(classNames)

def get_key(val,rollList):   #get the name of student by their roll no.
    Flag=False
    for key, value in rollList.items():
         if val == value:
             flag=True
             return key.upper()
    if flag==False:
        return "not exist"
 
  
def findEncodings(images):  #encodings of images
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        try:
            encode=face_recognition.face_encodings(img)[0]
        except IndexError as e:
            continue
        encodeList.append(encode)
    return encodeList

def markAttendance(roll,ax):  
    today=datetime.today() 
    Attendance = today.strftime("%b-%d-%Y") 
    v=Attendance+'.'+'csv'
    with open(v,'r+') as f:
        myDataList=f.readlines()
       
        print(myDataList)
        nameList=[]

        for line in myDataList:
            entry=line.split(',')
            nameList.append(entry[0])
        if roll not in nameList:
            now=datetime.now()
            dtString=now.strftime('%I:%M:%S:%p')
            f.writelines('\n'+str(roll)+','+str(get_key(str(roll),rollList))+','+(str(dtString)))
            ax[str(roll)]=str(dtString)
            present.append(str(roll))
        



encodeListKnown=findEncodings(images)
print(len(encodeListKnown))
print("ENCODING COMPLETE")

cap=cv2.VideoCapture(0, cv2.CAP_DSHOW)
ax={}
present=[]
while(True):
    start = time.time()
    stop = time.time()
    while(stop-start<25):
        success,img=cap.read()
    
        
        imgS=cv2.resize(img,(0,0),None,0.25,0.25)
        imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
        try:
            encode=face_recognition.face_encodings(img)[0]
        except IndexError as e:
            print("FACE is  NOT VISIBLE.... PLEASE LOOK AT THE CAMERA PROPERLY")
            
        

            continue



        facesCurrFrame=face_recognition.face_locations(imgS)
        encodeCurrFrame=face_recognition.face_encodings(imgS,facesCurrFrame)

        for encdeFace,faceLoc in zip(encodeCurrFrame,facesCurrFrame):
            matches=face_recognition.compare_faces(encodeListKnown,encdeFace)
            faceDis=face_recognition.face_distance(encodeListKnown,encdeFace)
            print(faceDis)

            matchIndex=np.argmin(faceDis)

            if matches[matchIndex]:
                name=classNames[matchIndex].upper()
                print(name)
                markAttendance(str(rollList[name.lower()]),ax)
                
                y1,x2,y2,x1=faceLoc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),1)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        cv2.imshow('WEBCAM',img)
        cv2.waitKey(1)
        stop = time.time()+1
    c=input("whether want to continue if yes the press 'y' otherwise any other than 'y'   ")
    if c=="y":
       
        continue
    else:
        break


today=datetime.today() 
Attendance = today.strftime("%b-%d-%Y") 
v=Attendance+'.'+'csv'
with open(v,'r+') as f:
    
    f.truncate(0)

    print("ax",ax)
    print(present)
    myDataList=f.readlines()
    for i in roLL:
        if i not in present:
            myDataList.append('\n'+i+','+get_key(i,rollList)+','+"ABSENT"+","+"N/A")
        else:
            myDataList.append('\n'+i+','+get_key(i,rollList)+','+"PRESENT"+","+str(ax[i]))
    
    myDataList.insert(0,'TIME\n')
    myDataList.insert(0,'STATUS,')
    myDataList.insert(0,'NAME,')
    myDataList.insert(0,'ROLL NO.,')
    f.writelines(myDataList)



    













