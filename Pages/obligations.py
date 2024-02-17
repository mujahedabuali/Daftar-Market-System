
import customtkinter as ck
from PIL import Image
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from db import mycursor,mydb
import mysql.connector
from pygame import mixer


class Obligations(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

        mixer.init()

        self.block_image = ck.CTkImage(Image.open("imags/debitt.png"),size=(40,40))
        self.label = ck.CTkLabel(self, text="التزامات  ",corner_radius=20,height=50,image=self.block_image,compound="right",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)
        
        self.search_entry = ck.CTkEntry(self,placeholder_text="search")
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<KeyRelease>", self.search)

        columns = ('id','name', 'price')

        self.table = ttk.Treeview(self,
                              columns=columns,
                              height=19,
                              selectmode='browse',
                              show='headings')

        self.table.column("#1", anchor="c", minwidth=50, width=50)
        self.table.column("#2", anchor="c", minwidth=220, width=300)
        self.table.column("#3", anchor="c", minwidth=50, width=200)

        self.table.heading('id', text='رمز الالتزام ')
        self.table.heading('name', text='الاسم')
        self.table.heading('price', text='المبلغ')

        self.table.bind('<Motion>', 'break')
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)

        self.scrollbar = ck.CTkScrollbar(self, orientation=ck.VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side=ck.RIGHT, fill=ck.Y)

        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.table.pack(fill=ck.BOTH, expand=False,padx=15)


        button_frame = ck.CTkFrame(self,fg_color="transparent")
        button_frame.pack(fill=ck.Y,expand=True,padx=15,pady=45)

        self.add_button = ck.CTkButton(button_frame, text="إضافة",height=30,command=self.add_data,font=ck.CTkFont(size=20,weight="bold"))
        self.add_button.grid(row=0, column=0, padx=10)

        self.edit_button = ck.CTkButton(button_frame, text="تعديل",height=30,command=self.edit_item,font=ck.CTkFont(size=20,weight="bold"))
        self.edit_button.grid(row=0, column=1, padx=10)

        self.delete_button = ck.CTkButton(button_frame, text="حذف",height=30,fg_color="red", command=self.delete_item,font=ck.CTkFont(size=20,weight="bold"))
        self.delete_button.grid(row=0, column=2, padx=10)

        self.edit_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")       

        self.intTable()


    def intTable(self):

        for row in self.table.get_children():
            self.table.delete(row)

        mycursor.execute("SELECT ObID,name,amount FROM obligations ORDER BY amount ASC")
        mysite = mycursor.fetchall()
        for site in mysite:
            self.table.insert('','end',values=(site))

    def search(self, event):
        search_query = self.search_entry.get().lower()
        self.table.selection_remove(self.table.selection())
        
        for item in self.table.get_children():
            name = self.table.item(item)["values"][1]
            name = name.lower()

            if search_query in name:
                self.table.selection_add(item)
                self.table.see(item)

    def add_data(self):
        self.add_window()

    def add_window(self):

        def get():
            list =[self.entry,self.entry2]
            entry_texts = [entry.get() for entry in list]
            if any(not text for text in entry_texts):
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","قم بادخال جميع الحقول",icon="warning")
            elif self.entry.get()[0].isdigit() or not (self.entry2.get().isdigit() or self.entry2.get().count('.') == 1):
                  mixer.music.load("sounds/error.mp3")
                  mixer.music.play()
                  messagebox.showwarning("Warning Message","قيم الإدخال غير صحيحة",icon="warning")
            else:
                    mixer.music.load("sounds/done.wav")
                    mixer.music.play()

                    current_date = datetime.now().date()
                    sql = "INSERT INTO Obligations (name, amount) VALUES (%s,%s)"
                    mycursor.execute(sql, (self.entry.get(),self.entry2.get()))
                    mydb.commit()    
                    self.intTable()
                    self.entry.delete(0,'end')
                    self.entry2.delete(0,'end')

        new_window = tk.Toplevel(self)
        new_window.geometry("440x500")
        new_window.title('اضافة التزام')

        self.label = ck.CTkLabel(new_window, text='اضافة التزام',corner_radius=20,height=50,text_color="red",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)


        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        label1 = ck.CTkLabel(new_window,width=200,text="الاسم:",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)

        label2 = ck.CTkLabel(new_window,width=200,text=" المبلغ:",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)

        self.entry2 = ck.CTkEntry(new_window,width=200)
        self.entry2.pack(padx=10, pady=10)

        ok_button = ck.CTkButton(new_window, text="إضافة", command=get)
        ok_button.pack(padx=10, pady=10)


    def edit_item(self):
         selected_item = self.table.focus()
         if selected_item:
            self.edit_window()
         else:  
             mixer.music.load("sounds/error.mp3")
             mixer.music.play()
             messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")

    def edit_window(self):
        def get():
            list =[self.entry,self.entry2]
            entry_texts = [entry.get() for entry in list]
            if any(not text for text in entry_texts):
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","قم بادخال جميع الحقول",icon="warning")
            elif  self.entry.get()[0].isdigit() or not (self.entry2.get().isdigit() or self.entry2.get().count('.') == 1) :
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","حركة خاطئة",icon="warning")
            else:
                    mixer.music.load("sounds/done.wav")
                    mixer.music.play()
                    selected_item = self.table.focus()
                    values =  self.table.item(selected_item, 'values')



                    sql = "UPDATE Obligations set name=%s , amount=%s"
                    mycursor.execute(sql, (self.entry.get(),self.entry2.get()))
                    mydb.commit()    
                    self.intTable()
                    self.entry.delete(0,'end')
                    self.entry2.delete(0,'end')


        new_window = tk.Toplevel(self)
        new_window.geometry("440x500")
        new_window.title('تعديل البضائع')

        self.label = ck.CTkLabel(new_window, text='تعديل البضائع',corner_radius=20,height=50,text_color="red",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)

        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        label1 = ck.CTkLabel(new_window,width=200,text="الاسم:",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)

        label2 = ck.CTkLabel(new_window,width=200,text="سعر البيع:",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)

        self.entry2 = ck.CTkEntry(new_window,width=200)
        self.entry2.pack(padx=10, pady=10)


        selected_item = self.table.focus()

        values =  self.table.item(selected_item, 'values')

        self.entry.delete(0,'end')
        self.entry2.delete(0,'end')

        self.entry.insert(0,values[1])
        self.entry2.insert(0,values[2])

        ok_button = ck.CTkButton(new_window, text="تعديل", command=get)
        ok_button.pack(padx=10, pady=10)   

    def delete_item(self):
         selected_item = self.table.focus()
         if selected_item:
            values = self.table.item(selected_item, "values")
            mixer.music.load("sounds/warning.wav")
            mixer.music.play()
            sure = messagebox.askyesno("Confirmation", f"متأكد ؟ \n حذف {values[1]}",icon="warning")
            if sure :
                try:
                    mycursor.execute("DELETE FROM Obligations WHERE ObID = %s",(values[0],))
                    mydb.commit() 
                    self.intTable()
                    mixer.music.load("sounds/done.wav")
                    mixer.music.play()
                except mysql.connector.Error as err:
                    messagebox.showwarning("Warning Message","حركة خاطئة",icon="warning")   
         else:  
            mixer.music.load("sounds/error.mp3")
            mixer.music.play()
            messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")

    def on_item_select(self,event):
        selected_item = self.table.focus()
        if selected_item:
                self.edit_button.configure(state="normal")
                self.delete_button.configure(state="normal")
        else :
                self.edit_button.configure(state="disabled")
                self.delete_button.configure(state="disabled")       

   
