import customtkinter as customtkinter
from PIL import Image, ImageTk, ImageOps, ImageDraw
from db import mycursor, mydb
import hashlib
import smtplib
from email.mime.text import MIMEText
import string
import tkinter
import random
from pygame import mixer
import math
from CTkMessagebox import CTkMessagebox

class login_page(customtkinter.CTkFrame):
    
    def __init__(self, parent,login):
        self.actionLogin = login
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        
        self.logoMuj_image = customtkinter.CTkImage(Image.open("imags/logo_muj.png"),size=(400,400))

        label = customtkinter.CTkLabel(self,text="المخماسي لمواد البناء   ",corner_radius=5,text_color="#2e8fe7",font=customtkinter.CTkFont(family="DecoType Naskh",size=100)) 
        label.pack() 

        self.logoLabl = customtkinter.CTkLabel(self,image=self.logoMuj_image,text="")
        self.logoLabl.pack(pady=10)

        self.user_pass = customtkinter.CTkEntry(self, placeholder_text="Password", width=200, show="*")
        self.user_pass.pack(pady=20, padx=10) 

        button = customtkinter.CTkButton(self,text='Login',command=self.actionLogin) 
        button.pack(pady=0,padx=10) 

        self.label_phone=customtkinter.CTkLabel(self,text="Forget Password ",cursor="hand2",height=30,font=("TkDefaultFont", 12, "underline"))
        self.label_phone.pack(pady=0)

        self.label_message = customtkinter.CTkLabel(self, text="", text_color="red")
        self.label_message.pack(pady=10)
        
        self.label_phone.bind("<Button-1>", self.open_forgot_password_window)

    def open_forgot_password_window(self, event):
        forgot_password_window = customtkinter.CTkToplevel(self)
        forgot_password_window.title("Forgot Password")
        customtkinter.set_appearance_mode("Dark")
        forgot_password_window.geometry("450x450")
        
        center_x = int(700)
        center_y = int(400)
        forgot_password_window.geometry(f"+{center_x}+{center_y}")

        mainLabel = customtkinter.CTkLabel(forgot_password_window,text="  Forget Password Page  ",cursor="hand2",image=self.signUp_image,compound="right",height=30,font=("Times New Roman", 25))
        mainLabel.pack(pady=10)

        label0 = customtkinter.CTkLabel(forgot_password_window, text="User Name:",font=("TkDefaultFont", 16))
        label0.pack(pady=10)

        name_entry = customtkinter.CTkEntry(forgot_password_window)
        name_entry.pack(pady=10)

        label = customtkinter.CTkLabel(forgot_password_window, text="Email:",font=("TkDefaultFont", 16))
        label.pack(pady=10)

        email_entry = customtkinter.CTkEntry(forgot_password_window)
        email_entry.pack(pady=10)

        label3 = customtkinter.CTkLabel(forgot_password_window, text="Phone:",font=("TkDefaultFont", 16))
        label3.pack(pady=10)

        ph_entry = customtkinter.CTkEntry(forgot_password_window)
        ph_entry.pack(pady=10)

        
        def ver():
            if not all([email_entry , name_entry, ph_entry]):
                CTkMessagebox(title="Failed Message", message="Please fill all the fields!", icon="info", fade_in_duration=5)
            else:
                mycursor.execute("SELECT * FROM userdata WHERE username = %s ", (name_entry.get(),))
                result = mycursor.fetchone()
                
                if result[1] ==name_entry.get() and result[3] ==email_entry.get() and result[4] ==ph_entry.get():        
                    email = email_entry.get()
                    self.user_entry.insert(0,name_entry.get())
                    verify_code = self.send_verification_code(email)  
                    self.vertfic(verify_code,name_entry.get(),True)
                    forgot_password_window.destroy()

        send_button = customtkinter.CTkButton(forgot_password_window,text='Send',command=ver) 
        send_button.pack(pady=6,padx=10)
      

   
    def pattren(self,entered_username):
        pat = customtkinter.CTkToplevel(self)
        pat.title("Verficiation Pattern")
        customtkinter.set_appearance_mode("Dark")
        pat.geometry("600x610")
        
        center_x = int(600)
        center_y = int(220)
        pat.geometry(f"+{center_x}+{center_y}")
        size = 100
        angle = 72
        self.star_count=0

        self.st = []

        mainLabel = customtkinter.CTkLabel(pat,text="  Select 3 Stars  ",height=30,font=("Times New Roman", 25))
        mainLabel.pack(pady=10)
        
        canvas = tkinter.Canvas(pat, width=500, height=500, bg="black")
        canvas.pack()

        selected = customtkinter.CTkLabel(pat,text="",height=20,text_color="red",font=("Times New Roman", 25))
        selected.pack(pady=10)


        def draw_star(x, y, size, angle, fill):
            points = []
            for i in range(5):
                x1 = x + size * math.cos(math.radians(angle + i * 144))
                y1 = y + size * math.sin(math.radians(angle + i * 144))
                points.append(x1)
                points.append(y1)
            return canvas.create_polygon(points, fill=fill, outline="white", width=3)

        def press(event):
        
            if self.star_count < 3:
                mixer.init()
                mixer.music.load("buttonclick.wav")
                mixer.music.play()
                item = canvas.find_withtag(tkinter.CURRENT)[0]
                color = colors_dict[item]
                self.st.append(color)

                self.star_count+=1
                selected.configure(text=self.star_count,text_color="yellow")

                if self.star_count==3:
                     mycursor.execute("SELECT pattren FROM userdata WHERE username = %s", (entered_username,))
                     userdata = mycursor.fetchone()
                     pt = ",".join(self.st)
                     pt2=hashlib.sha256(pt.encode()).hexdigest()
                     
                
                     if pt2==userdata[0]:
                        selected.configure(text="")   
                        self.actionLogin()
                        pat.destroy()   
                     else:
                         selected.configure(text="Wrong Pattren!!")   
                         self.st = [] 
                         self.star_count=0


        stars = []
        colors_dict = {}
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        for i in range(6):

            x = random.randint(50, 450)
            y = random.randint(50, 450)

            fill = colors[i]
            star = draw_star(x, y, size, angle, fill)
            stars.append(star)
            colors_dict[star] = fill

            canvas.bind("<Button-1>", press)
        

        Unvalidlabel = customtkinter.CTkLabel(pat, text="",font=("TkDefaultFont", 14), text_color="red")
        Unvalidlabel.pack(pady=4)    

    def login(self): 
        entered_username = self.user_entry.get()
        entered_password = hashlib.sha256(self.user_pass.get().encode()).hexdigest()

        mycursor.execute("SELECT * FROM userdata WHERE username = %s AND password = %s", (entered_username, entered_password))
        result = mycursor.fetchone()
        mycursor.execute("SELECT email FROM userdata WHERE username = %s AND password = %s", (entered_username, entered_password))
        result1 = mycursor.fetchone()
        
        if result and result1:
                self.label_message.configure(text="")
                # target_username = "entered_username"
                email = result1[0]
                verification_code = self.send_verification_code(email)  
                self.vertfic(verification_code,entered_username)

        else:
                self.label_message.configure(text="Invalid Username or Password")
       

    def vertfic(self,verification_code,entered_username,forget=False):
        ver = customtkinter.CTkToplevel(self)
        ver.title(" Vertfication Page")
        customtkinter.set_appearance_mode("Dark")
        ver.geometry("350x250")
        
        center_x = int(700)
        center_y = int(400)
        ver.geometry(f"+{center_x}+{center_y}")

        mainLabel = customtkinter.CTkLabel(ver,text="  Vertfication Page  ",cursor="hand2",height=30,font=("Times New Roman", 25))
        mainLabel.pack(pady=10)
        
        label1 = customtkinter.CTkLabel(ver, text="Code on you Email:",font=("TkDefaultFont", 16))
        label1.pack(pady=7)

        email_entry = customtkinter.CTkEntry(ver)
        email_entry.pack(pady=5)

        Wronglabel = customtkinter.CTkLabel(ver, text="",font=("TkDefaultFont", 14), text_color="red")
        Wronglabel.pack(pady=10)


        def check():
            
            entered_code = email_entry.get()

            if entered_code == verification_code:
                mycursor.execute("UPDATE lastuser SET username = %s WHERE id = 1", (entered_username,))

                mydb.commit()
                ver.destroy()
                if forget == False:
                    self.pattren(entered_username)
                else : self.actionLogin()   
            else:
                Wronglabel.configure(text="*Wrong Code")


        submit_button = customtkinter.CTkButton(ver, text="Submit", command=check )
        submit_button.pack(pady=10)  


    def send_verification_code(self, email):

        verification_code = ''.join(random.choices(string.digits, k=6)) 

        self.verification_code = verification_code

        subject = "Verification Code for Safe Web"
        body = f"Your verification code is: {verification_code}"
        sender_email = "adhamturki321@gmail.com" 
        receiver_email = email

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_username = "adhamturki321@gmail.com"
        smtp_password = "hzaimilhhzljcgvn"

        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return verification_code

   
    