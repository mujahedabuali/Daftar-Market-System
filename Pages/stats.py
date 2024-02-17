import customtkinter as ck
from PIL import Image
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from db import mycursor,mydb


class page3(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

      
        # print(entered_username)

        self.bookmark_image = ck.CTkImage(Image.open("imags/stats.png"),size=(40,40))
        self.label = ck.CTkLabel(self, text="حسابات  ",image=self.bookmark_image,corner_radius=20,compound="right",height=50,font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)
        
        


       