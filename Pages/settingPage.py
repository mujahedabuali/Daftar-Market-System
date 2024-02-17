
#for make a Web filter page
import customtkinter as ck
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from PIL import Image
from db import mycursor, mydb
import hashlib
import re
import tkinter
import math
import random
from pygame import mixer


class Setting_Page(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)


        self.setting_image = ck.CTkImage(Image.open("imags/settings.png"),size=(30,30))
        self.label = ck.CTkLabel(self, text="الاعدادات ",corner_radius=20,image=self.setting_image,compound="right",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=10)

        name=ck.CTkLabel(self, text="المخماسي لمواد البناء",text_color="#2e8fe7",font=ck.CTkFont(family="Times New Roman", size=25,weight="bold"))
        name.pack(pady=50)

        self.pass_image = ck.CTkImage(Image.open("imags/password.png"),size=(50,50))
        self.pass_button = ck.CTkButton(self, text="تغيير كلمة المرور",height=50,width=400,image=self.pass_image,compound="left",font=ck.CTkFont(size=22,weight="bold"))
        self.pass_button.pack(pady=20)

        self.email_image = ck.CTkImage(Image.open("imags/email.png"),size=(40,40))
        self.email_button = ck.CTkButton(self, text="تغيير البريد الالكتروني",height=55,width=400,image=self.email_image,compound="left",font=ck.CTkFont(size=22,weight="bold"))
        self.email_button.pack(pady=30)


        theme=ck.CTkLabel(self, text="الوضع الليلي",font=ck.CTkFont(size=17,weight="bold"))
        theme.pack(pady=5)
        self.appearance_mode_optionemenu = ck.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)

        self.appearance_mode_optionemenu.pack(pady=10)

        scall=ck.CTkLabel(self, text="حجم النصوص",font=ck.CTkFont(size=17,weight="bold"))
        scall.pack(pady=5)
        self.scaling_optionemenu = ck.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.pack(pady=10)

        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")

        # passlabl=ck.CTkLabel(self, text="Password:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold"))
        # passlabl2=ck.CTkLabel(self, text="Re-Enter Password:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold"))
        # emailLabl=ck.CTkLabel(self, text="Email:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold"))
       
        # # self.err = ck.CTkLabel(self, text="",fg_color="red",font=ck.CTkFont(family="Times New Roman", size=16,weight="bold"))
        # # self.err.place(x=430,y=750)
        
        # self.password_entry = ck.CTkEntry(self, show="*", width=200,placeholder_text="ex:MM#@3...to 8 digit")
        # self.password_entry2 = ck.CTkEntry(self, show="*", width=200)
        # self.email_entry = ck.CTkEntry(self, width=200)
        # self.phone_entry = ck.CTkEntry(self, width=200)
        # self.password_strength = ck.CTkLabel(self, text="Password strength: ",font=("Time New Roman", 14,"italic"))

        # passlabl.pack(pady=10)
        # self.password_entry.pack(pady=10)
        # passlabl2.pack(pady=5)
        # self.password_strength.pack()
        # self.password_entry2.pack(pady=10)
        # emailLabl.pack(pady=10)
        # self.email_entry.pack(pady=10)

        # self.password_entry.bind("<KeyRelease>", self.check_password)
        # self.checkbox_var = ck.IntVar()
        # self.checkbox1 = ck.CTkCheckBox(self,text=' Real-Time Bloking',variable=self.checkbox_var,font=("Times New Roman", 18)) 
        # self.checkbox1.place(x=400,y=600)
        
         # Save button
        # save_button = ck.CTkButton(self, text="Save Changes", command=self.save_changes)
        # save_button.place(x=430,y=540)
        # ptt_button = ck.CTkButton(self, text="Change Pattren",fg_color="green",command=self.pattren)
        # ptt_button.place(x=430,y=500)

        # mycursor.execute("SELECT username,email,phonenumber,realtime_block FROM userdata WHERE username = %s", (self.entered_username,))
        # userdata = mycursor.fetchone()
        # self.username_entry.insert(0,userdata[0])
        # self.email_entry.insert(0,userdata[1])
        # self.phone_entry.insert(0, userdata[2])
        # if userdata[3]==1:
        #     self.checkbox1.select()
        #     self.checkbox_var=1
        # else:
        #     self.checkbox1.deselect()
        #     self.checkbox_var=0


    # def save_changes(self):
    #     entered_username = self.login_page_instance.get_entered_username()

    #     # Get values from entry widgets
    #     new_password = self.password_entry.get()
    #     new_password2 = self.password_entry2.get()
    #     new_email = self.email_entry.get()
    #     new_phone = self.phone_entry.get()
    #     realtime_block_value = 1 if self.checkbox1.get() == 1 else 0


    #     # Check if all fields are not empty
    #     if not all([new_password, new_password2, new_email, new_phone]):
    #         self.err.configure(text="Please fill all the fields!")
    #         return

    #     # Check if the password and re-entered password match
    #     if new_password != new_password2:
    #         self.err.configure(text="The two passwords are not matched!")
    #         return
    #     passStrong = self.check_password("xx")
    #     if passStrong != "Strong" and passStrong != "Very Strong":
    #         self.err.configure(text="The  passwords are not Strong!")
    #         return

    #     # Update the user's information in the 'userdata' table
    #     update_query = """
    #     UPDATE userdata
    #     SET password = %s, email = %s, phonenumber = %s, realtime_block = %s
    #     WHERE username = %s
    #     """
    #     self.err.configure(text="")
    #     # Hash the new password before updating
    #     hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

    #     # Execute the update query
    #     mycursor.execute(update_query, (hashed_password, new_email, new_phone,realtime_block_value,entered_username))
    #     CTkMessagebox(title="Successful Message",message="Successfully changed!",icon="info",fade_in_duration=5)

    #     mydb.commit()

    # def check_password(self,xx):

    #     password = self.password_entry.get()

    #     length_error = len(password) < 8
    #     digit_error = re.search(r"\d", password) is None
    #     uppercase_error = re.search(r"[A-Z]", password) is None
    #     lowercase_error = re.search(r"[a-z]", password) is None
    #     symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~\"]", password) is None

    #     score = 5 - sum([length_error, digit_error, uppercase_error, lowercase_error, symbol_error])

    #     strength_level = {0: "Blank", 1: "Very Weak", 2: "Weak", 3: "Medium", 4: "Strong", 5: "Very Strong"}
    #     strength_color = {0: "white", 1: "red", 2: "orange", 3: "yellow", 4: "limegreen", 5: "green"}
 
    #     self.password_strength.configure(text=f"Password strength: {strength_level[score]}", text_color=strength_color[score])
    #     return strength_level[score]

    
    # def pattren(self):
    #     pat = ck.CTkToplevel(self)
    #     pat.title("set Pattern")
    #     ck.set_appearance_mode("Dark")
    #     pat.geometry("610x650")
        
    #     center_x = int(600)
    #     center_y = int(220)
    #     pat.geometry(f"+{center_x}+{center_y}")
    #     size = 100
    #     angle = 72
    #     self.star_count=0

    #     self.st = []

    #     mainLabel = ck.CTkLabel(pat,text="  Select 3 Stars  ",height=30,font=("Times New Roman", 25))
    #     mainLabel.pack(pady=10)
        
    #     canvas = tkinter.Canvas(pat, width=500, height=500, bg="black")
    #     canvas.pack()

    #     selected = ck.CTkLabel(pat,text="",height=20,text_color="green",font=("Times New Roman", 25))
    #     selected.pack(pady=10)

    #     def submit2():
    #         update_query = """UPDATE userdata SET pattren = %s WHERE username = %s"""
    #         mycursor.execute(update_query, (",".join(self.st),self.entered_username))
    #         mydb.commit()
    #         pat.destroy()

    #     submit_button1 = ck.CTkButton(pat, text="Submit", command=submit2,state="disabled")
    #     submit_button1.pack(pady=10)  


    #     def draw_star(x, y, size, angle, fill):
    #         points = []
    #         for i in range(5):
    #             x1 = x + size * math.cos(math.radians(angle + i * 144))
    #             y1 = y + size * math.sin(math.radians(angle + i * 144))
    #             points.append(x1)
    #             points.append(y1)
    #         return canvas.create_polygon(points, fill=fill, outline="white", width=3)

    #     def press(event):
        
    #         if self.star_count < 3:
    #             mixer.init()
    #             mixer.music.load("buttonclick.wav")
    #             mixer.music.play()
    #             item = canvas.find_withtag(tkinter.CURRENT)[0]
    #             color = colors_dict[item]
    #             self.st.append(color)

    #             selected.configure(text=" ".join(self.st),text_color="yellow")
    #             self.star_count+=1

    #             if self.star_count==3:
    #                 submit_button1.configure(state="normal")
                   

    #     stars = []
    #     colors_dict = {}
    #     colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    #     for i in range(6):

    #         x = random.randint(50, 450)
    #         y = random.randint(50, 450)

    #         fill = colors[i]
    #         star = draw_star(x, y, size, angle, fill)
    #         stars.append(star)
    #         colors_dict[star] = fill

    #         canvas.bind("<Button-1>", press)
        

    #     Unvalidlabel = ck.CTkLabel(pat, text="",font=("TkDefaultFont", 14), text_color="red")
    #     Unvalidlabel.pack(pady=4)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ck.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ck.set_widget_scaling(new_scaling_float)