import tkinter.messagebox
from tkinter import *
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image,ImageTk
import numpy as np
import mysql.connector
from time import strftime
from datetime import datetime
from tkinter import filedialog
import webbrowser
import csv
import cv2
import os
import sys

###  https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#=======HOME PAGE=========

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

def main():
    win=ctk.CTk()
    app=Login_window(win)
    win.mainloop()

class Login_window:
    def __init__(self,log):
        self.log=log
        self.log.minsize(500,400)
        self.log.geometry('800x600')
        self.log.title('Face Recognition Attendence System ')

        self.img = ctk.CTkImage(Image.open(resource_path('images\\pattern.png')), size=(1550,850))
        self.imglbl = ctk.CTkLabel(self.log, image=self.img)
        self.imglbl.pack(fill=BOTH, expand=TRUE)

        self.mainfr = ctk.CTkFrame(self.imglbl, width=350, height=380, corner_radius=15)
        self.mainfr.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        ctk.CTkLabel(master=self.mainfr, text="Log into your Account",font=('Century Gothic',24)).place(x=50, y=45)
        
        ctk.CTkLabel(self.mainfr, text='Username', font=('Century Gothic',12)).place(x=65, y=115)

        self.entrybox1 = tk.StringVar()
        ctk.CTkEntry(self.mainfr, textvariable=self.entrybox1, width=240, placeholder_text='Username').place(x=60, y=140)

        ctk.CTkLabel(self.mainfr, text='Password', font=('Century Gothic',12)).place(x=65, y=185)

        self.entrybox2 = tk.StringVar()
        ctk.CTkEntry(self.mainfr, textvariable=self.entrybox2, width=240, placeholder_text='Password', show='*').place(x=60, y=210)

        ctk.CTkButton(self.mainfr, text='Forgot Password?',command=self.forgot_pass, fg_color='transparent', font=('Century Gothic',12), hover_color='#2B2B2B').place(x=170, y=240)
       
        ctk.CTkButton(self.mainfr,width=240, text="Login", corner_radius=6, command=self.login).place(x=60, y=280)
        
        self.btn3=ctk.CTkButton(self.mainfr, text='New User Register', bg_color='transparent',fg_color='transparent', font=('Century Gothic',12), command=self.register_win, hover_color='#2B2B2B').place(x=110, y=320)

    
    def register_win(self):
        self.main=Register(self)
        

    def login(self):
        if self.entrybox1.get()=='' or self.entrybox2.get()=='':
            messagebox.showerror('Error','All fields required!',parent=self.log)
        elif self.entrybox1.get()=='Arun' and self.entrybox2.get()=='1234':
            messagebox.showinfo('Success','Login Successfully',parent=self.log)
        else:
            conn = mysql.connector.connect(host='Localhost', user='root', password='Kr1sh@n', database='mydata1')
            my_cursor = conn.cursor()
            my_cursor.execute('select * from register where email=%s and password=%s',(

                self.entrybox1.get(),
                self.entrybox2.get()
            ))

            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror('Error','Invalid Username & Password',parent=self.log)
            else:
                open_main=messagebox.askyesno('YesNO','Access only admin')
                if open_main>0:
                    self.main=Face_Recognition_System(self)

                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()
            


###############################--RESET PASSWORD--###############################
    def reset_pass(self):
        if self.question_combo.get()=='Select':
            messagebox.showerror('Error','Select Security Question',parent=self.root2)
        elif self.answer.get()=='':
            messagebox.showerror('Error','Please enter the answer',parent=self.root2)
        elif self.resetpass.get()=="":
            messagebox.showerror('Error','Please enter the new password',parent=self.root2)
        else:
            conn = mysql.connector.connect(host='Localhost', username='root', password='Kr1sh@n', database='mydata1')
            my_cursor = conn.cursor()
            query=('select * from register where email=%s and securityQ=%s and SecurityA=%s')
            value=(self.entrybox1.get(),self.question_combo.get(),self.answer.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror('Error','Please enter the correct answer',parent=self.root2)
            else:
                query=('update register set password=%s where email=%s')
                value=(self.resetpass.get(),self.entrybox1.get())
                my_cursor.execute(query,value)

                conn.commit()
                conn.close()
                messagebox.showinfo('INFORMATION','Your password has been reset\n Please Login new Password',parent=self.root2)
                self.root2.destroy()


##########################--FORGOT PASSWORD__####################################

    def forgot_pass(self):
        if self.entrybox1.get()=='':
            messagebox.showerror('Error','Please Enter the Email address to Forgot the password',parent=self.log)
        else:
            conn = mysql.connector.connect(host='Localhost', user='root', password='Kr1sh@n', database='mydata1')
            my_cursor = conn.cursor()
            query=('select * from register where email=%s')
            value=(self.entrybox1.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()

            if row==None:
                messagebox.showerror('Error','Please enter the valid user name',parent=self.log)
            else:
                conn.close()
            
                self.root2=ctk.CTkToplevel()
                self.root2.title('Forgot Password')
                self.root2.minsize(500,400)
                self.root2.geometry('800x600')
                self.root2.after(100, self.root2.lift)

                self.img = ctk.CTkImage(Image.open(resource_path('images\\pattern.png')), size=(1550,850))
                self.imglbl = ctk.CTkLabel(self.root2, image=self.img)
                self.imglbl.pack(fill=BOTH, expand=TRUE)

                self.mainfr = ctk.CTkFrame(self.imglbl, width=350, height=380, corner_radius=15)
                self.mainfr.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                l=ctk.CTkLabel(self.mainfr,text='Forgot Password',font=('arial', 20, 'bold',)).place(x=0,y=10,relwidth=1)

                # question
                question = ctk.CTkLabel(self.mainfr, text='==> Select Security Question:-', font=('times new roman', 13, 'bold',))
                question.place(x=105,y=80)
                
                self.question_combo = ctk.CTkComboBox(self.mainfr, width=150, values=['Select', 'Your Birth Place', 'Your Girlfriend Name', 'Your pet Name'],font=('times new roman', 11, 'bold',), state='readonly')
                self.question_combo.place(x=120,y=110)

                # answer
                answer = ctk.CTkLabel(self.mainfr, text='==> Security Answer:-', font=('times new roman', 13, 'bold',))
                answer.place(x=105,y=165)
                self.answer = ctk.CTkEntry(self.mainfr, width=150,font=('times new roman', 13, 'bold',))
                self.answer.place(x=120,y=195)


                # RESET PASSWORD

                resetpass = ctk.CTkLabel(self.mainfr, text='==> New Password:-', font=('times new roman', 13, 'bold',))
                resetpass.place(x=105, y=240)
                self.resetpass = ctk.CTkEntry(self.mainfr, width=150, font=('times new roman', 13, 'bold',))
                self.resetpass.place(x=120, y=270)

                # REST--BUTTON

                btn=ctk.CTkButton(self.mainfr,text='Reset',font=('times new roman', 13, 'bold',), command=self.reset_pass)
                btn.place(x=120,y=320)

    def fExit(self):
        self.fExit=tkinter.messagebox.askyesno('Face Recognition','Are you sure exit this software',parent=self.root)
        if self.fExit>0:
            self.root.destroy()
        else:
            return



##########################-REGISTER CLASS-############################################################################################################


class Register:
    def __init__(self,reg):
        self.reg=ctk.CTkToplevel()
        self.reg.minsize(500,400)
        self.reg.geometry('800x600')
        self.reg.title('Face Recognition Attendence System ')
        self.reg.after(100, self.reg.lift)

        self.img = ctk.CTkImage(Image.open(resource_path('images\\pattern.png')), size=(1550,850))
        self.imglbl = ctk.CTkLabel(self.reg, image=self.img)
        self.imglbl.pack(fill=BOTH, expand=TRUE)

        heading = ctk.CTkLabel(self.imglbl, text='New User Registration', font=('Times New Roman',38,'bold')).place(relx=0.5, rely=0.1, anchor='n')

        # ====================Variable================

        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_securityQ = StringVar(value='Select')
        self.var_securityA = StringVar()
        self.var_pass = StringVar()
        self.var_confpass = StringVar()

        # InsideTable---------------------------------------------
        intable = ctk.CTkFrame(self.imglbl, width=600, height=500)
        intable.place(relx=0.5, rely=0.5,  anchor=tkinter.CENTER)


        # First Name
        Firstname = ctk.CTkLabel(intable, text='First Name:', font=('times new roman', 14, 'bold'))
        Firstname.grid(row=0, column=0, padx=10, pady=15)
        Firstname1 = ctk.CTkEntry(intable, width=150, textvariable=self.var_fname, font=('times new roman', 13, 'bold',))
        Firstname1.grid(row=0, column=1, padx=10, pady=15, sticky=W)

        # Lastname
        Lastname = ctk.CTkLabel(intable, text='Last Name', font=('times new roman', 14, 'bold',))
        Lastname.grid(row=0, column=2, padx=10, pady=15)
        Lastname = ctk.CTkEntry(intable, width=150, textvariable=self.var_lname, font=('times new roman', 13, 'bold',))
        Lastname.grid(row=0, column=3, padx=10, pady=15, sticky=W)

        # contact
        contact = ctk.CTkLabel(intable, text='Contact No.', font=('times new roman', 14, 'bold',))
        contact.grid(row=1, column=0, padx=10, pady=15)
        contact = ctk.CTkEntry(intable, width=150, textvariable=self.var_contact, font=('times new roman', 13, 'bold',))
        contact.grid(row=1, column=1, padx=10, pady=15, sticky=W)


        # email
        email = ctk.CTkLabel(intable, text='Email', font=('times new roman', 14, 'bold',))
        email.grid(row=1, column=2, padx=10, pady=15)
        email = ctk.CTkEntry(intable, width=150, textvariable=self.var_email, font=('times new roman', 13, 'bold',))
        email.grid(row=1, column=3, padx=10, pady=15, sticky=W)

        # question
        question = ctk.CTkLabel(intable, text='Select Security Question', font=('times new roman', 14, 'bold',))
        question.grid(row=2, column=0, padx=10, pady=15)
        question_combo = ctk.CTkComboBox(intable, width=150, variable=self.var_securityQ, values=['Select', 'Your Birth Place', 'Your Girlfriend Name', 'Your pet Name'], font=('times new roman', 11, 'bold',),state='readonly')
        question_combo.grid(row=2, column=1, pady=10, padx=11, sticky=W)

        # answer
        answer = ctk.CTkLabel(intable, text='Security Answer', font=('times new roman', 14, 'bold',))
        answer.grid(row=2, column=2, padx=10, pady=15)
        answer = ctk.CTkEntry(intable, width=150, textvariable=self.var_securityA, font=('times new roman', 13, 'bold',))
        answer.grid(row=2, column=3, padx=10, pady=15, sticky=W)

        # password
        password = ctk.CTkLabel(intable, text='Password', font=('times new roman', 14, 'bold',))
        password.grid(row=3, column=0, padx=10, pady=15)
        password = ctk.CTkEntry(intable, width=150, textvariable=self.var_pass, font=('times new roman', 13, 'bold',))
        password.grid(row=3, column=1, padx=10, pady=15, sticky=W)

        # confpass
        confpass = ctk.CTkLabel(intable, text='Confirm Password', font=('times new roman', 14, 'bold',))
        confpass.grid(row=3, column=2, padx=10, pady=15)
        confpass = ctk.CTkEntry(intable, width=150, textvariable=self.var_confpass, font=('times new roman', 13, 'bold',))
        confpass.grid(row=3, column=3, padx=10, pady=15, sticky=W)

        # Check Button---------------------------
        self.var_check=IntVar()
        checkbtn=ctk.CTkCheckBox(intable,variable=self.var_check,text='I agree the Terms & Conditions',font=('times new roman', 13, 'bold',),onvalue=1,offvalue=0)
        checkbtn.grid(row=4,column=0,padx=20,pady=15)

        # Button----------------------------------
        # login btn-----
        b2 = ctk.CTkButton(intable, text='LogIn', cursor='hand2', command=self.rtn_login)
        b2.place(x=550, y=250)

        # register btn-------
        b3 = ctk.CTkButton(intable, text='Register', cursor='hand2',command=self.register_data)
        b3.place(x=400, y=250)

        # ---------------------------Functionalty---------------

    def register_data(self):
        if self.var_fname.get()=='' or self.var_email.get()=='' or self.var_securityQ.get()=='Select':
            messagebox.showerror('Error','All fields required!',parent=self.reg)
        elif self.var_pass.get()!=self.var_confpass.get():
            messagebox.showerror('Error','Password & Confirm password must be same',parent=self.reg)
        elif self.var_check.get()==0:
            messagebox.showerror('Error','Please agree our Terms & Conditions',parent=self.reg)
        else:
            conn = mysql.connector.connect(host='Localhost', user='root', password='Kr1sh@n',database='mydata1')
            my_cursor = conn.cursor()
            query=('select * from register where email=%s')
            value=(self.var_email.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror('Error','User already exist, Please try another email',parent=self.reg)
            else:
                my_cursor.execute('insert into register values(%s,%s,%s,%s,%s,%s,%s)',(
                                                                                        self.var_fname.get(),
                                                                                        self.var_lname.get(),
                                                                                        self.var_contact.get(),
                                                                                        self.var_email.get(),
                                                                                        self.var_securityQ.get(),
                                                                                        self.var_securityA.get(),
                                                                                        self.var_pass.get()

                                                                                        ))
                messagebox.showinfo('Success', 'Register Successful', parent=self.reg)

            conn.commit()
            conn.close()

    def rtn_login(self):
        self.reg.destroy()


#####################################--MAIN WINDOW--###########################################################################################

class Face_Recognition_System:
    def __init__(self,root):
        self.root=ctk.CTkToplevel()
        self.root.minsize(500,400)
        self.root.geometry('1500x800')
        self.root.title('Face Recognition Attendence System ')
        self.root.after(100, self.root.lift)

        self.img = ctk.CTkImage(Image.open(resource_path('images\\pattern.png')), size=(1550,850))
        self.imglbl = ctk.CTkLabel(self.root, image=self.img)
        self.imglbl.pack(fill=BOTH, expand=TRUE)

        mainframe = ctk.CTkFrame(self.imglbl,width=1300,height=700)
        mainframe.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.mnimg = ctk.CTkImage(Image.open(resource_path('images\\main_pic.png')), size=(680,520))
        self.mnimg = ctk.CTkLabel(mainframe, image=self.mnimg, text='')
        self.mnimg.place(relx=0.46, rely=0.13)

        
#####################--MAIN_FRAME--###################################################################################
        text = ctk.CTkLabel(mainframe, justify='left', text='Face\nRecognition ', font=('Arial', 72, 'bold')).place(relx=0.08, rely=0.3)
        text = ctk.CTkLabel(mainframe, justify='left', text="Facial recognition is a category of biometric software that maps\nan individual's facial features mathematically and stores the data\nas a faceprint. The software uses deep learning algorithms to\ncompare a live capture or digital image to the stored faceprint\nin order to verify an individual's identity.", font=('Arial', 16, 'bold',)).place(relx=0.08, rely=0.56)
    
        # LINK  
        self.url = 'https://github.com/arun0ku/Report-On-Face-Recognition-System.git'
        link = ctk.CTkButton(mainframe, text='Learn More', font=('Arial',34,'underline'), corner_radius=100, fg_color='#2B2B2B', hover_color='#262626', cursor='hand2', command=self.callback)
        link.place(relx=0.08, rely=0.74)
                

        # Student detail
       
        btn_text1 = ctk.CTkButton(mainframe, text='Student Detail', font=('Arial',18), fg_color='#2B2B2B', hover_color='#262626', command=self.student_details, cursor='hand2')
        btn_text1.place(relx=0.67, rely=0.1, anchor='ne')

        # Attendence Detail
        
        btn_text2 = ctk.CTkButton(mainframe, text='Attendence Detail', font=('Arial',18), fg_color='#2B2B2B', hover_color='#262626', cursor='hand2',command=self.attendance_data)
        btn_text2.place(relx=0.79, rely=0.1, anchor='ne')

        # Detected Photos
       
        btn_text3 = ctk.CTkButton(mainframe, text='Detected Photos', font=('Arial',18), fg_color='#2B2B2B', hover_color='#262626', cursor='hand2',command=self.open_photo)
        btn_text3.place(relx=0.91, rely=0.1, anchor='ne')

        # Detect face
        
        btn_text4 = ctk.CTkButton(mainframe, text='Face Detector', font=('Arial',18), cursor='hand2',command=self.face_recoge)
        btn_text4.place(relx=0.75, rely=0.9, anchor='ne')


        # Training Data

        btn_text5 = ctk.CTkButton(mainframe, text='Training Data', font=('Arial',18), cursor='hand2',command=self.train_data)
        btn_text5.place(relx=0.88, rely=0.9, anchor='ne')


        # Exit
        
        # btn_text = ctk.CTkButton(mainframe, text='Exit', cursor='hand2',command=self.iExit)
        # btn_text.place(relx=0.4, rely=0.1, anchor='ne')

    def callback(self):
        webbrowser.open_new(self.url)

    def student_details(self):
        self.app=Student(self)

    def attendance_data(self):
        self.app=Attendanced(self)
    
    def open_photo(self):
        os.startfile('data')

    def iExit(self):
        self.iExit=tkinter.messagebox.askyesno('Face Recognition','Are you sure exit this software',parent=self.root)
        if self.iExit>0:
            self.root.destroy()
        else:
            return

    def train_data(self):
        data_dir = ('data')
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L')
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)
            cv2.imshow('Training Data',imageNp)
            cv2.waitKey(1)==13
        ids = np.array(ids)

        # ===========================Train the classifier===========

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write(resource_path('face_data\\classifier.xml'))
        cv2.destroyAllWindows()
        messagebox.showinfo('Result', 'Training datasets completed!!',parent=self.root)


        # ==================================Face-Detector============

    def mark_attendance(self,i,r,n,d):
        with open('attendance_data/Attendance.csv','r+',newline='\n') as f:
            myDataList=f.readlines()
            name_list=[]
            for line in myDataList:
                entry=line.split((','))
                name_list.append(entry[0])
            if((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list)):
                now=datetime.now()
                d1=now.strftime('%d/%m/%Y')
                dtString=now.strftime('%H:%M:%S')
                f.writelines(f'\n{i},{r},{n},{d},{dtString},{d1},Present')

        #===========face recognition=========

    def face_recoge(self):
        def draw_boundray(img,classifier,scaleFactore,minNeighbors,color,text,clf):
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features=classifier.detectMultiScale(gray_image,scaleFactore,minNeighbors)

            coord=[]

            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict=clf.predict(gray_image[y:y+h,x:x+w])
                confidence=int((100*(1-predict/300)))

                conn = mysql.connector.connect(host='Localhost', username='root', password='Kr1sh@n',database='face_recognition')
                my_cursor=conn.cursor()

                my_cursor.execute('select Name from student where Student_Id='+str(id))
                n= my_cursor.fetchone()
                n="+".join(n)

                my_cursor.execute('select Roll from student where Student_Id='+str(id))
                r= my_cursor.fetchone()
                r="+".join(r)

                my_cursor.execute('select Dep from student where Student_Id='+str(id))
                d= my_cursor.fetchone()
                d="+".join(d)

                my_cursor.execute('select Student_Id from student where Student_Id='+str(id))
                i= my_cursor.fetchone()
                i="+".join(i)

                if confidence>77:
                    cv2.putText(img,f'Id:{i}',(x,y-80),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,0,0),3)
                    cv2.putText(img,f'Name:{n}',(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,0,0),3)
                    cv2.putText(img,f'Roll:{r}',(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,0,0),3)
                    cv2.putText(img,f'Dep:{d}',(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,0,0),3)
                    self.mark_attendance(i,r,n,d)

                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,'Unknown Face',(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)


                coord=[x,y,w,y]

            return coord

        def recognize(img,clf,faceCascade):
            coord=draw_boundray(img,faceCascade,1.1,10,(255,25,255),'Face',clf)
            return img

        faceCascade=cv2.CascadeClassifier(resource_path('face_data\\haarcascade_frontalface_default.xml'))
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read(resource_path('face_data\\classifier.xml'))

        video_cap=cv2.VideoCapture(0)

        while True:
            ret,img=video_cap.read()
            img=recognize(img,clf,faceCascade)
            cv2.imshow('Welcome To Face Recognition',img)

            if cv2.waitKey(1)==13:
                break

        video_cap.release()
        cv2.destroyAllWindows()


##########################################STUDENT-DETAIL###################################################################################################

myresult = []

class Student:
    def __init__(self,std):
        self.std=ctk.CTkToplevel()
        self.std.minsize(1100,800)
        self.std.geometry('1500x800')
        self.std.title('Face Recognition Attendence System ')
        self.std.after(100, self.std.lift)

        self.img = ctk.CTkImage(Image.open(resource_path('images\\pattern.png')), size=(1550,850))
        self.imglbl = ctk.CTkLabel(self.std, image=self.img, text='')
        self.imglbl.pack(fill=BOTH, expand=TRUE)

        # ====================Variable================

        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_semester=StringVar()
        self.va_std_id=StringVar()
        self.var_std_name = StringVar()
        self.var_roll=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
        self.var_teacher=StringVar()


        text = ctk.CTkLabel(self.imglbl, text='STUDENT DETAIL', font=('times new roman', 34, 'bold',)).place(relx=0.5, rely=0.1, anchor=CENTER)


        # LEFT FRAME
        l_f1 = ctk.CTkFrame(self.imglbl, border_width=2, width=700, height=560)
        l_f1.place(relx=0.26, rely=0.5, anchor=CENTER)

        #LABEL CURRENT COURSE INFORMATION
        CC_Label = ctk.CTkLabel(l_f1, text='Current Course information', font=('times new roman', 28, 'bold',)).place(relx=0.5, rely=0.12, anchor=CENTER)

        CC_frame = ctk.CTkFrame(l_f1, border_width=2)
        CC_frame.place(relx=0.5, rely=0.25, anchor=CENTER)

        # Department
        dep_l = ctk.CTkLabel(CC_frame, text='Department:', font=('times new roman', 16, 'bold',)).grid(row=0, column=0, padx=10, pady=10)
        self.var_dep = ctk.StringVar(value='Select department')
        dep_combo = ctk.CTkOptionMenu(CC_frame, variable=self.var_dep,  values=['Select department', 'Computer Scince', 'Machenical', 'IT', 'Civil'], font=('times new roman',16,'bold',), state='readonly')
        dep_combo.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Course
        Corse_l = ctk.CTkLabel(CC_frame, text='Course      :', font=('times new roman', 16, 'bold',)).grid(row=0, column=2, padx=10, pady=10)
        self.var_course = ctk.StringVar(value='Select Course    ')
        Corse_combo = ctk.CTkOptionMenu(CC_frame, variable=self.var_course, values=['Select Course    ', 'B.tech', 'BBA', 'BCA', 'B.COM'], font=('times new roman',16,'bold',), state='readonly')
        Corse_combo.grid(row=0, column=3, padx=10, pady=10, sticky=W)

        # Year
        year_l = ctk.CTkLabel(CC_frame, text='Year            :', font=('times new roman', 16, 'bold',)).grid(row=1, column=0, padx=10, pady=10)
        self.var_year = ctk.StringVar(value='Select Year           ')
        year_combo = ctk.CTkOptionMenu(CC_frame,variable=self.var_year, values=['Select Year           ', '2023', '2022', '2021', '2020'], font=('times new roman',16,'bold',), state='readonly')
        year_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Semester
        sem_l = ctk.CTkLabel(CC_frame, text='Semester  :', font=('times new roman', 16, 'bold',)).grid(row=1, column=2, pady=10, padx=10)
        self.var_semester = ctk.StringVar(value='Select Semester')
        sem_combo = ctk.CTkOptionMenu(CC_frame,variable=self.var_semester,values=['Select Semester', 'VIIIth', 'VIIth', 'VIth', 'Vth', 'IVth', 'IIIrd', 'IInd', 'Ist'], font=('times new roman',16,'bold',), state='readonly')
        sem_combo.grid(row=1, column=3, padx=10, pady=10, sticky=W)

        # Class Student Information

        CS_Label = ctk.CTkLabel(l_f1, text='Class Student information', font=('times new roman', 28, 'bold',)).place(relx=0.5, rely=0.45, anchor=CENTER)

        CS_frame = ctk.CTkFrame(l_f1, border_width=2)
        CS_frame.place(relx=0.5, rely=0.68, anchor=CENTER)

        # StudentId
        std_id = ctk.CTkLabel(CS_frame, text='Student-ID:', font=('times new roman', 16, 'bold',))
        std_id.grid(row=0, column=0, padx=10, pady=5)
        std = ctk.CTkEntry(CS_frame,textvariable=self.va_std_id, font=('times new roman', 16, 'bold',))
        std.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Student Name
        Std_name = ctk.CTkLabel(CS_frame, text='Student Name:', font=('times new roman', 16, 'bold'))
        Std_name.grid(row=0, column=2, padx=10, pady=5)
        Stdname = ctk.CTkEntry(CS_frame,textvariable=self.var_std_name, font=('times new roman', 16, 'bold',))
        Stdname.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Roll No.
        Roll_no = ctk.CTkLabel(CS_frame, text='Roll no.      :', font=('times new roman', 16, 'bold',))
        Roll_no.grid(row=1, column=0, padx=10, pady=5)
        Roll_no = ctk.CTkEntry(CS_frame,textvariable=self.var_roll, font=('times new roman', 16, 'bold',))
        Roll_no.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Gender
        Gender = ctk.CTkLabel(CS_frame, text='Gender            :', font=('times new roman', 16, 'bold',))
        Gender.grid(row=1, column=2, padx=10, pady=5)
        self.var_gender = ctk.StringVar(value='Select gender')
        gender_combo = ctk.CTkOptionMenu(CS_frame, variable=self.var_gender, values=['Select gender', 'Male', 'Female', 'Other'], font=('times new roman',16,'bold',),state='readonly')
        gender_combo.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # Dob
        Dob = ctk.CTkLabel(CS_frame, text='DoB            :', font=('times new roman', 16, 'bold',))
        Dob.grid(row=2, column=0, padx=10, pady=5)
        Dob = ctk.CTkEntry(CS_frame,textvariable=self.var_dob, font=('times new roman', 16, 'bold',))
        Dob.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # Email
        Emal = ctk.CTkLabel(CS_frame, text='Email               :', font=('times new roman', 16, 'bold',))
        Emal.grid(row=2, column=2, padx=10, pady=5)
        Emal = ctk.CTkEntry(CS_frame,textvariable=self.var_email, font=('times new roman', 16, 'bold',))
        Emal.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # Phone
        Phone = ctk.CTkLabel(CS_frame, text='Phone         :', font=('times new roman', 16, 'bold',))
        Phone.grid(row=3, column=0, padx=10, pady=5)
        Phone = ctk.CTkEntry(CS_frame,textvariable=self.var_phone, font=('times new roman', 16, 'bold',))
        Phone.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # Teacher
        Teacher = ctk.CTkLabel(CS_frame, text='Teacher           :', font=('times new roman', 16, 'bold',))
        Teacher.grid(row=3, column=2, padx=10, pady=5)
        Teacher = ctk.CTkEntry(CS_frame,textvariable=self.var_teacher, font=('times new roman', 16, 'bold',))
        Teacher.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # radio button
        self.var_radio1=StringVar()
        radiobtn = ctk.CTkRadioButton(CS_frame,variable=self.var_radio1, text='Take photo Sample', value='yes')
        radiobtn.grid(row=6, column=0, padx=10, pady=10)

        radiobtn0 = ctk.CTkRadioButton(CS_frame,variable=self.var_radio1, text='No photo Sample', value='No')
        radiobtn0.grid(row=6, column=1, padx=10, pady=10)

        # Button Frame
        btnFrame = ctk.CTkFrame(l_f1, fg_color='transparent')
        btnFrame.place(relx=0.5, rely=0.9, anchor=CENTER)

        savebtn = ctk.CTkButton(btnFrame, text='Save', font=('times new roman', 20, 'bold',), command=self.add_data)
        savebtn.grid(row=0, column=0, padx=4)

        updatebtn = ctk.CTkButton(btnFrame, text='Update', font=('times new roman', 20, 'bold',), command=self.update_data)
        updatebtn.grid(row=0, column=1, padx=4)

        deletebtn = ctk.CTkButton(btnFrame, text='Delete', font=('times new roman', 20, 'bold',), command=self.delete_data)
        deletebtn.grid(row=0, column=2, padx=4)

        Resetbtn = ctk.CTkButton(btnFrame, text='Reset', font=('times new roman', 20, 'bold',), command=self.reset_data)
        Resetbtn.grid(row=0, column=3, padx=4)

        btnFrame0 = ctk.CTkFrame(l_f1, fg_color='transparent')
        btnFrame0.place(relx=0.5, rely=0.96, anchor=CENTER )

        Takephotobtn = ctk.CTkButton(btnFrame0, text='Take Photo Sample', font=('times new roman', 20, 'bold',), command=self.face_data)
        Takephotobtn.grid(row=1, column=0, padx=5)

        Uppicbtn = ctk.CTkButton(btnFrame0, text='Update Photo Sample', font=('times new roman', 20, 'bold',), command=self.update_face_data)
        Uppicbtn.grid(row=1, column=1, padx=5)

        # RIGHT FRAME
        f1 = ctk.CTkFrame(self.imglbl, border_width=2, width=700, height=560)
        f1.place(relx=0.74, rely=0.5, anchor=CENTER)

        # ======Search=====

        search_lb = ctk.CTkFrame(f1, border_width=2)
        search_lb.place(x=5, y=10)

        sort = ctk.CTkLabel(search_lb, text='Sort By:', font=('times new roman', 16, 'bold',))
        sort.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        search_combo = ctk.CTkOptionMenu(search_lb, font=('times new roman', 13, 'bold',), values=['Select', 'Student Name', 'Student-ID', 'Roll no.', 'Email', 'Phone'], state='readonly')
        search_combo.grid(row=0, column=1, pady=10, sticky=W)

        search_entry = ctk.CTkEntry(search_lb, font=('times new roman', 13, 'bold',))
        search_entry.grid(row=0, column=2, pady=5, padx=5, sticky=W)

        search_btn = ctk.CTkButton(search_lb, text='Search', font=('times new roman', 11, 'bold',))
        search_btn.grid(row=0, column=3, padx=5, pady=5)

        search_btn0 = ctk.CTkButton(search_lb, text='Show All', font=('times new roman', 11, 'bold',))
        search_btn0.grid(row=0, column=4, padx=5, pady=5)

        # ===============Table Frame===========

        table = Frame(f1, bd=0, bg='#2E2E2E', relief=RIDGE)
        table.place(x=10, y=90, width=860, height=600)

        scroll_x = ctk.CTkScrollbar(table, orientation=HORIZONTAL, fg_color='transparent', bg_color='transparent')
        scroll_y = ctk.CTkScrollbar(table, orientation=VERTICAL, fg_color='transparent', bg_color='transparent')

        style = ttk.Style(std)
        # set ttk theme to "clam" which support the fieldbackground option
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#2E2E2E", foreground="white", font=('Arial', 13, 'bold'))
        style.configure("Treeview", background="#2E2E2E", fieldbackground="#2E2E2E", foreground="white", font=('Arial', 12, 'bold'))
        
        self.student_table = ttk.Treeview(table, columns=('dep', 'course', 'year', 'sem', 'id', 'name', 'roll', 'gender', 'dob' , 'email', 'phone', 'teacher','photo'))

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.configure(command=self.student_table.xview)
        scroll_y.configure(command=self.student_table.yview)

        self.student_table.configure(yscrollcommand=scroll_y.set)
        self.student_table.configure(xscrollcommand=scroll_x.set)

        self.student_table.heading('dep', text='Department')
        self.student_table.heading('course', text='Course')
        self.student_table.heading('year', text='year')
        self.student_table.heading('sem', text='Semester')
        self.student_table.heading('roll', text='Roll_no')
        self.student_table.heading('id', text='StudentId')
        self.student_table.heading('name', text='Name')
        self.student_table.heading('dob', text='DOB')
        self.student_table.heading('email', text='Email')
        self.student_table.heading('phone', text='Phone')
        self.student_table.heading('teacher', text='Teacher')
        self.student_table.heading('gender', text='Gender')
        self.student_table.heading('photo', text='PhotoSampleStatus')
        self.student_table['show'] = 'headings'

        self.student_table.column('dep', width=150)
        self.student_table.column('course', width=100)
        self.student_table.column('year', width=100)
        self.student_table.column('sem', width=100)
        self.student_table.column('roll', width=100)
        self.student_table.column('id', width=100)
        self.student_table.column('name', width=100)
        self.student_table.column('dob', width=100)
        self.student_table.column('email', width=100)
        self.student_table.column('phone', width=150)
        self.student_table.column('teacher', width=100)
        self.student_table.column('gender', width=100)
        self.student_table.column('photo', width=100)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()

        #=======================function declaration=================

    def add_data(self):
        if self.var_dep.get()=='Select Department' or self.var_std_name.get()==''or self.va_std_id.get()=='':
            messagebox.showerror('Error','All Fields are required',parent=self.std)
        else:
            try:
                conn=mysql.connector.connect(host='Localhost',user='root',password='Kr1sh@n',database='face_recognition')
                my_cursor=conn.cursor()
                my_cursor.execute('insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(
                                                                                                            self.var_dep.get(),
                                                                                                            self.var_course.get(),
                                                                                                            self.var_year.get(),
                                                                                                            self.var_semester.get(),
                                                                                                            self.va_std_id.get(),
                                                                                                            self.var_std_name.get(),
                                                                                                            self.var_roll.get(),
                                                                                                            self.var_gender.get(),
                                                                                                            self.var_dob.get(),
                                                                                                            self.var_email.get(),
                                                                                                            self.var_phone.get(),
                                                                                                            self.var_teacher.get(),
                                                                                                            self.var_radio1.get()
                                                                                                        ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo('Success','Student detail has been added Successfully',parent=self.std)
            except Exception as es:
                messagebox.showerror('Error',f'Due To :{str(es)}',parent=self.std)

    # =================fetch data=================

    def fetch_data(self):
        conn=mysql.connector.connect(host='Localhost', user='root', password='Kr1sh@n',database='face_recognition')
        my_cursor=conn.cursor()
        my_cursor.execute('select * from student')
        data=my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert('',END,values=i)
            conn.commit()
        conn.close()

    # =========================get cursor============

    def get_cursor(self,event=''):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content['values']

        self.var_dep.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_semester.set(data[3]),
        self.va_std_id.set(data[4]),
        self.var_std_name.set(data[5]),
        self.var_roll.set(data[6]),
        self.var_gender.set(data[7]),
        self.var_dob.set(data[8]),
        self.var_email.set(data[9]),
        self.var_phone.set(data[10]),
        self.var_teacher.set(data[11]),
        self.var_radio1.set(data[12])

    # update data

    def update_data(self):
        if self.var_dep.get()=='Select Department' or self.var_std_name.get()=='' or self.va_std_id.get() == '':
            messagebox.showerror('Error', 'All Fields are required', parent=self.std)
        else:
            try:
                Update = messagebox.askyesno('Update','Do you want to update this student details',parent=self.std)
                if Update > 0:
                    conn=mysql.connector.connect(host='Localhost', user='root', password='Kr1sh@n',database='face_recognition')
                    my_cursor=conn.cursor()
                    my_cursor.execute('update student set Dep=%s,course=%s,Year=%s,Semester=%s,Name=%s,Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Teacher=%s,PhotoSmaple=%s where Student_Id=%s',(
                                                                                                                                                                                            self.var_dep.get(),
                                                                                                                                                                                            self.var_course.get(),
                                                                                                                                                                                            self.var_year.get(),
                                                                                                                                                                                            self.var_semester.get(),
                                                                                                                                                                                            self.var_std_name.get(),
                                                                                                                                                                                            self.var_roll.get(),
                                                                                                                                                                                            self.var_gender.get(),
                                                                                                                                                                                            self.var_dob.get(),
                                                                                                                                                                                            self.var_email.get(),
                                                                                                                                                                                            self.var_phone.get(),
                                                                                                                                                                                            self.var_teacher.get(),
                                                                                                                                                                                            self.var_radio1.get(),
                                                                                                                                                                                            self.va_std_id.get()
                                                                                                                                                                                        ))

                else:
                    if not Update:
                        return
                messagebox.showinfo('Success','Student details successfully updated',parent=self.std)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror('Error',f'Due to:{str(es)}',parent=self.std)


    # Deletion Data

    def delete_data(self):
        if self.va_std_id.get()=='':
            messagebox.showerror('Error','Student id must be required',parent=self.std)
        else:
            try:
                delete=messagebox.askyesno('Student Delete Page','Do you want to delete this student',parent=self.std)
                if delete>0:
                    conn = mysql.connector.connect(host='Localhost', user='root', password='Kr1sh@n',database='face_recognition')
                    my_cursor = conn.cursor()
                    sql='delete from student where Student_Id=%s'
                    val=(self.va_std_id.get(),)
                    my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo('Delete','Successfully deleted student details',parent=self.std)
            except Exception as es:
                messagebox.showerror('Error',f'Due to:{str(es)}',parent=self.std)


    # Reset Button

    def reset_data(self):
        self.var_dep.set('Select Department'),
        self.var_course.set('Select Course'),
        self.var_year.set('Select Year'),
        self.var_semester.set('Select Semester'),
        self.va_std_id.set(''),
        self.var_std_name.set(''),
        self.var_roll.set(''),
        self.var_gender.set('Select Gender'),
        self.var_dob.set(''),
        self.var_email.set(''),
        self.var_phone.set(''),
        self.var_teacher.set(''),
        self.var_radio1.set('')


    # ==================Face Data===============

    def face_data(self):
        if self.var_dep.get() == 'Select Department' or self.var_std_name.get() == '' or self.va_std_id.get() == '':
            messagebox.showerror('Error', 'All Fields are required', parent=self.std)
        else:
            try:
                conn = mysql.connector.connect(host='Localhost', user='root', password='Kr1sh@n',database='face_recognition')
                my_cursor = conn.cursor()
                my_cursor.execute('select * from student')
                myresult=my_cursor.fetchall()
                id=0
                for x in myresult:
                    id+=1
                my_cursor.execute('update student set Dep=%s,course=%s,Year=%s,Semester=%s,Name=%s,Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Teacher=%s,PhotoSmaple=%s where Student_Id=%s',(
                                                                                                                                                                                        self.var_dep.get(),
                                                                                                                                                                                        self.var_course.get(),
                                                                                                                                                                                        self.var_year.get(),
                                                                                                                                                                                        self.var_semester.get(),
                                                                                                                                                                                        self.var_std_name.get(),
                                                                                                                                                                                        self.var_roll.get(),
                                                                                                                                                                                        self.var_gender.get(),
                                                                                                                                                                                        self.var_dob.get(),
                                                                                                                                                                                        self.var_email.get(),
                                                                                                                                                                                        self.var_phone.get(),
                                                                                                                                                                                        self.var_teacher.get(),
                                                                                                                                                                                        self.var_radio1.get(),
                                                                                                                                                                                        self.va_std_id.get()==id+1
                                                                                                                                                                                    ))

                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()

                #========================load predefined data on face frontals from opencv=========

                face_classifier=cv2.CascadeClassifier(resource_path('face_data\\haarcascade_frontalface_default.xml'))

                def face_cropped(img):
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray,1.3,5)

                    # scaling factor=1.3
                    # Minimum neighbor=5
                    for (x,y,w,h) in faces:
                        face_cropped=img[y:y+h,x:x+w]
                        return face_cropped

                cap=cv2.VideoCapture(0)
                img_id=0
                while True:
                    ret, my_frame=cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id+=1
                        face=cv2.resize(face_cropped(my_frame),(450,450))
                        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        file_name_path='data/user.'+str(id)+'.'+str(img_id)+'.jpg'
                        cv2.imwrite(file_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                        cv2.imshow('Croped Face',face)

                    if cv2.waitKey(1)==13 or int(img_id)==100:
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo('Result','Generating  data sets completed!!!',parent=self.std)
            except Exception as es:
                messagebox.showerror('Error',f'Due To:{str(es)}',parent=self.std)



    def update_face_data(self):
        global myresult
        if self.var_dep.get() == 'Select Department' or self.var_std_name.get() == '' or self.va_std_id.get() == '':
            messagebox.showerror('Error', 'All Fields are required', parent=self.std)
        else:
            try:
                myresult.clear()
                conn = mysql.connector.connect(host='Localhost', user='root', password='Kr1sh@n',database='face_recognition')
                my_cursor = conn.cursor()
                my_cursor.execute('select * from student')
                myresult=my_cursor.fetchall()
                id=0
                for x in myresult:
                    id+=1
                my_cursor.execute('update student set Dep=%s,course=%s,Year=%s,Semester=%s,Name=%s,Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Teacher=%s,PhotoSmaple=%s where Student_Id=%s',(
                                                                                                                                                                                        self.var_dep.get(),
                                                                                                                                                                                        self.var_course.get(),
                                                                                                                                                                                        self.var_year.get(),
                                                                                                                                                                                        self.var_semester.get(),
                                                                                                                                                                                        self.var_std_name.get(),
                                                                                                                                                                                        self.var_roll.get(),
                                                                                                                                                                                        self.var_gender.get(),
                                                                                                                                                                                        self.var_dob.get(),
                                                                                                                                                                                        self.var_email.get(),
                                                                                                                                                                                        self.var_phone.get(),
                                                                                                                                                                                        self.var_teacher.get(),
                                                                                                                                                                                        self.var_radio1.get(),
                                                                                                                                                                                        self.va_std_id.get()==id+1
                                                                                                                                                                                    ))

                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()

                #========================load predefined data on face frontals from opencv=========

                face_classifier=cv2.CascadeClassifier(resource_path('face_data\\haarcascade_frontalface_default.xml'))

                def face_cropped(img):
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray,1.3,5)

                    # scaling factor=1.3
                    # Minimum neighbor=5
                    for (x,y,w,h) in faces:
                        face_cropped=img[y:y+h,x:x+w]
                        return face_cropped

                cap=cv2.VideoCapture(0)
                img_id=0
                while True:
                    ret, my_frame=cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id+=1
                        face=cv2.resize(face_cropped(my_frame),(450,450))
                        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        file_name_path='data/user.'+str(id)+'.'+str(img_id)+'.jpg'
                        cv2.imwrite(file_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                        cv2.imshow('Croped Face',face)

                    if cv2.waitKey(1)==13 or int(img_id)==100:
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo('Result','Generating  data sets completed!!!',parent=self.std)
            except Exception as es:
                messagebox.showerror('Error',f'Due To:{str(es)}',parent=self.std)

##################################################--ATTENDANCE-DETAILS--#############################################################################

mydata=[]

class Attendanced:
    def __init__(self,atd):
        self.atd=ctk.CTkToplevel()
        self.atd.geometry('1500x800')
        self.atd.title('Face Recognition Attendence System ')
        self.atd.after(100, self.atd.lift)


        self.img = ctk.CTkImage(Image.open(resource_path('images\\pattern.png')), size=(1550,850))
        self.imglbl = ctk.CTkLabel(self.atd, image=self.img, text='')
        self.imglbl.pack(fill=BOTH, expand=TRUE)
    

        # =============================== Variable==================

        self.var_atten_id=StringVar()
        self.var_atten_roll=StringVar()
        self.var_atten_name=StringVar()
        self.var_atten_dep=StringVar()
        self.var_atten_time=StringVar()
        self.var_atten_date=StringVar()
        self.var_atten_attendance=StringVar()

        text = ctk.CTkLabel(self.imglbl, text='ATTENDANCE DETAIL', font=('Arial', 42, 'bold',))
        text.place(relx=0.5, rely=0.1, anchor=CENTER)

        # LEFT FRAME
        
        lblf1 = ctk.CTkFrame(self.imglbl, border_width=2, width=700, height=500)
        lblf1.place(relx=0.25, rely=0.55, anchor=CENTER)

        lbltext = ctk.CTkLabel(lblf1, text='Student Detail', font=('Arial', 34, 'bold',)).place(relx=0.5, rely=0.1, anchor=CENTER)

        # left iside frame
        l_in_f1=ctk.CTkFrame(lblf1, border_width=0, fg_color='transparent')
        l_in_f1.place(relx=0.5, rely=0.4, anchor=CENTER)


        # Attendence id
        attdance_id = ctk.CTkLabel(l_in_f1, text='Attendance ID :', font=('Arial', 16, 'bold',))
        attdance_id.grid(row=1, column=0, padx=10, pady=20)
        attdance = ctk.CTkEntry(l_in_f1, textvariable=self.var_atten_id, font=('Arial', 16, 'bold',))
        attdance.grid(row=1, column=1, padx=10, pady=20, sticky=W)

        # Roll No.
        Roll_no = ctk.CTkLabel(l_in_f1, text='Roll no.           :', font=('Arial', 16, 'bold',))
        Roll_no.grid(row=2, column=0, padx=10, pady=10)
        Roll_no = ctk.CTkEntry(l_in_f1, textvariable=self.var_atten_roll, font=('Arial', 16, 'bold',))
        Roll_no.grid(row=2, column=1, padx=10,pady=10, sticky=W)

        #   Time
        Time = ctk.CTkLabel(l_in_f1, text= 'Time               :', font=('Arial', 16, 'bold',))
        Time.grid(row=3, column=0, padx=10, pady=10)
        Time = ctk.CTkEntry(l_in_f1, textvariable=self.var_atten_time, font=('Arial', 16, 'bold',))
        Time.grid(row=3, column=1, padx=10, pady=10, sticky=W)

        # Student Name
        Std_name = ctk.CTkLabel(l_in_f1, text='Student Name :', font=('Arial', 16, 'bold',), width=150)
        Std_name.grid(row=1, column=2, padx=10, pady=10)
        Stdname = ctk.CTkEntry(l_in_f1, textvariable=self.var_atten_name, font=('Arial', 16, 'bold',))
        Stdname.grid(row=1, column=3, padx=10, pady=10, sticky=W)

        # Departement
        Department = ctk.CTkLabel(l_in_f1, text='Department     :', font=('Arial', 16, 'bold',), width=150)
        Department.grid(row=2, column=2, padx=10, pady=10)
        Department = ctk.CTkEntry(l_in_f1, textvariable=self.var_atten_dep, font=('Arial', 16, 'bold',))
        Department.grid(row=2, column=3, padx=10, pady=10, sticky=W)

        # Date
        Date = ctk.CTkLabel(l_in_f1, text='Date                :', font=('Arial', 16, 'bold',), width=150)
        Date.grid(row=3, column=2, padx=10, pady=10)
        Date = ctk.CTkEntry(l_in_f1, textvariable=self.var_atten_date, font=('Arial', 16, 'bold',))
        Date.grid(row=3, column=3, padx=10, pady=10, sticky=W)

        # Attendance_Status
        Attendence_Status = ctk.CTkLabel(l_in_f1, text='Attendance Status:', font=('Arial', 16, 'bold',))
        Attendence_Status.grid(row=6, column=0, padx=10, pady=10)
        self.var_atten_attendance = ctk.StringVar(value='Status')
        year_combo = ctk.CTkOptionMenu(l_in_f1, variable=self.var_atten_attendance, values=['Status','Present','Abesent'], font=('Arial', 16, 'bold',),state='readonly')
        year_combo.grid(row=6, column=1, padx=10, pady=10, sticky=W)

        # Button Frame
        btnFrame = ctk.CTkFrame(lblf1, border_width=0, fg_color='transparent')
        btnFrame.place(relx=0.5, rely=0.7, anchor=CENTER)

        Exportbtn = ctk.CTkButton(btnFrame, text='Export', font=('Arial', 26, 'bold',),command=self.exportCsv)
        Exportbtn.grid(row=0, column=0)

        Importbtn = ctk.CTkButton(btnFrame, text='Import', font=('Arial', 26, 'bold',),command=self.importCsv)
        Importbtn.grid(row=0, column=1, padx=100)


        Resetbtn = ctk.CTkButton(btnFrame, text='Reset', font=('Arial', 26, 'bold',),command=self.reset_data)
        Resetbtn.grid(row=0, column=2)

        # upbtn = ctk.CTkButton(lblf1, text='update', font=('Arial', 26, 'bold',),command=self.update_data)
        # upbtn.place(relx=0.5, rely=0.8, anchor=CENTER)


        # RIGHT FRAME
        f1 = ctk.CTkFrame(self.imglbl, border_width=2, width=700, height=500)
        f1.place(relx=0.75, rely=0.55, anchor=CENTER)

        # ===============Table Frame===========

        table = Frame(f1, bd=0, bg='#2E2E2E')
        table.place(x=13, y=10, width=850, height=600)

        #==================Scrolll bar===============

        scroll_x = ctk.CTkScrollbar(table, bg_color='transparent', fg_color='transparent', orientation=HORIZONTAL)
        scroll_y = ctk.CTkScrollbar(table, bg_color='transparent', fg_color='transparent', orientation=VERTICAL)
        
        style = ttk.Style(table)
        # set ttk theme to "clam" which support the fieldbackground option
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#2E2E2E", foreground="white", font=('Arial', 13, 'bold'))
        style.configure("Treeview", background="#2E2E2E", fieldbackground="#2E2E2E", foreground="white", font=('Arial', 12, 'bold'))
        
        self.student_table = ttk.Treeview(table, columns=(
        'id', 'roll', 'name','department', 'time', 'date', 'attendance'),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.configure(command=self.student_table.xview)
        scroll_y.configure(command=self.student_table.yview)

        self.student_table.heading('id', text='Attendance Id')
        self.student_table.heading('roll', text='Roll_no')
        self.student_table.heading('name', text='Name')
        self.student_table.heading('department', text='Department')
        self.student_table.heading('time', text='Time')
        self.student_table.heading('date', text='Date')
        self.student_table.heading('attendance', text='Attendance')

        self.student_table['show'] = 'headings'

        self.student_table.column('id', width=120)
        self.student_table.column('roll', width=120)
        self.student_table.column('name', width=120)
        self.student_table.column('department', width=120)
        self.student_table.column('time', width=120)
        self.student_table.column('date', width=120)
        self.student_table.column('attendance', width=120)


        self.student_table.pack(fill=BOTH, expand=1)

        self.student_table.bind('<ButtonRelease>',self.get_cursor)

        # ====================================fetch data=======================================

    def fetchData(self,rows):
        self.student_table.delete(*self.student_table.get_children())
        for i in rows:
            self.student_table.insert('',END,values=i)
    #import CSV
    def importCsv(self):
        global mydata
        mydata.clear()
        fln=filedialog.askopenfilename(initialdir=os.getcwd(),title='Open CSV',filetypes=(('CSV File','.csv'),('All File','*.*')),parent=self.atd)
        with open(fln) as myfile:
            csvread=csv.reader(myfile,delimiter=',')
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)


    # Export CSV
    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror('No Data','No Data Found To Export',parent=self.atd)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Open CSV', filetypes=(('CSV File', '.csv'), ('All File', '*.*')), parent=self.atd)
            with open(fln,mode='w',newline='') as myfile:
                exp_write=csv.writer(myfile,delimiter=',')
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo('Data Export','Your data Exported To '+os.path.basename(fln)+'Successfully',parent=self.atd)
        except Exception as es:
            messagebox.showerror('Error',f'Due To :{str(es)}',parent=self.atd)

    def get_cursor(self,event=''):
        cursor_row=self.student_table.focus()
        content=self.student_table.item(cursor_row)
        rows=content['values']
        self.var_atten_id.set(rows[0]),
        self.var_atten_roll.set(rows[1]),
        self.var_atten_name.set(rows[2]),
        self.var_atten_dep.set(rows[3]),
        self.var_atten_time.set(rows[4]),
        self.var_atten_date.set(rows[5]),
        self.var_atten_attendance.set(rows[6])


    def reset_data(self):
        self.var_atten_id.set('')
        self.var_atten_roll.set('')
        self.var_atten_name.set('')
        self.var_atten_dep.set('')
        self.var_atten_time.set('')
        self.var_atten_date.set('')
        self.var_atten_attendance.set('Status')




if __name__=='__main__':
    main()