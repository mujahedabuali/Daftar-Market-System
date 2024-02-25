
import customtkinter as ck
from PIL import Image
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from db import mycursor,mydb
import mysql.connector
from PIL import Image,ImageTk
import ctypes
from pygame import mixer
import os
import sys
import subprocess
import webbrowser


from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from datetime import datetime


class Store(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

        mixer.init()

        self.block_image = ck.CTkImage(Image.open("imags/storehouse.png"),size=(40,40))
        self.label = ck.CTkLabel(self, text="المستودع  ",corner_radius=20,height=50,image=self.block_image,compound="right",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=20)
        

        top_frame= ck.CTkFrame(self,fg_color="transparent")
        top_frame.pack(fill=ck.X,expand=False,padx=5,pady=5)

        search_frame= ck.CTkFrame(top_frame,fg_color="transparent")
        search_frame.pack(fill=ck.Y,expand=False,padx=10,pady=7)

        topBttn_frame= ck.CTkFrame(top_frame,fg_color="transparent")
        topBttn_frame.pack(side="right", padx=10)
        
        self.search_entry = ck.CTkEntry(search_frame,placeholder_text="search by name")
        self.search_entry.grid(row=0, column=0)
        self.search_entry.bind("<KeyRelease>", self.search)

        self.search_entry2 = ck.CTkEntry(search_frame,placeholder_text="search by id",width=90)
        self.search_entry2.grid(row=0, column=2,padx=10)
        self.search_entry2.bind("<KeyRelease>", self.searchByID)


        self.print_button = ck.CTkButton(topBttn_frame, text="طباعة تقارير",height=20,width=15,command=self.Xprint,font=ck.CTkFont(size=14,weight="bold"))
        self.print_button.grid(row=2, column=0,padx=10)

        self.edit_button = ck.CTkButton(topBttn_frame, text="تعديل",height=20,width=14,command=self.edit_item,font=ck.CTkFont(size=14,weight="bold"))
        self.edit_button.grid(row=2, column=1,padx=10)

        self.delete_button = ck.CTkButton(topBttn_frame, text="حذف",height=20,width=14,fg_color="red", command=self.delete_item,font=ck.CTkFont(size=14,weight="bold"))
        self.delete_button.grid(row=2, column=2, padx=10)
        
        columns = ('id','name', 'cont','unit','price', 'date',"price_buy")

        self.table = ttk.Treeview(self,
                              columns=columns,
                              height=19,
                              selectmode='browse',
                              show='headings')

        self.table.column("#1", anchor="c", minwidth=30, width=30)
        self.table.column("#2", anchor="c", minwidth=260, width=260)
        self.table.column("#3", anchor="c", minwidth=50, width=50)
        self.table.column("#4", anchor="c", minwidth=80, width=80)
        self.table.column("#5", anchor="c", minwidth=80, width=80)
        self.table.column("#6", anchor="c", minwidth=120, width=120)
        self.table.column("#7", anchor="c", minwidth=50, width=50)

        self.table.heading('id', text='رمز الصنف ')
        self.table.heading('name', text='الاسم')
        self.table.heading('cont', text='كمية')
        self.table.heading('unit', text='وحدة')
        self.table.heading('price', text='سعر البيع')
        self.table.heading('date', text='تاريخ الادخال')
        self.table.heading('price_buy', text='سعر الشراء')

        self.table.bind('<Motion>', 'break')
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=100,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=10)
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat",
                        font=ck.CTkFont(size=30,weight="bold"))
        
        style.map("Treeview.Heading",
                    background=[('active', '#3484F0')])


        self.scrollbar = ck.CTkScrollbar(self, orientation=ck.VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side=ck.RIGHT, fill=ck.Y)

        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.table.pack(fill=ck.BOTH, expand=False,padx=15)


        button_frame = ck.CTkFrame(self,fg_color="transparent")
        button_frame.pack(fill=ck.Y,expand=True,padx=15,pady=45)

        self.add_button = ck.CTkButton(button_frame, text=" اضافة عنصر جديد",height=30,command=self.add_data,font=ck.CTkFont(size=20,weight="bold"))
        self.add_button.grid(row=0, column=0, padx=10)

        self.plus_button = ck.CTkButton(button_frame, text="زيادة الكمية",height=30,command=self.plus_data,fg_color="green",font=ck.CTkFont(size=20,weight="bold"))
        self.plus_button.grid(row=0, column=1, padx=10)

       

        self.edit_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")  
        self.plus_button.configure(state="disabled")     

        self.intTable()


    def intTable(self):

        for row in self.table.get_children():
            self.table.delete(row)

        mycursor.execute("SELECT ProductID,ProductName,StockQuantity,Unit,sell_Price,ProductDate,Price FROM Products ORDER BY ProductID DESC")
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

    def searchByID(self, event):
        search_query = self.search_entry2.get().lower()
        self.table.selection_remove(self.table.selection())
        
        for item in self.table.get_children():
            id = str(self.table.item(item)["values"][0]).lower()
            if search_query in id:
                self.table.selection_add(item)
                self.table.see(item)

    def add_data(self):
        self.add_window()

    def add_window(self):

        def get():
            list =[self.entry,self.entry2,self.entry3,self.entry4]
            
            entry_texts = [entry.get() for entry in list]
            if any(not text for text in entry_texts):
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","قم بادخال جميع الحقول",icon="warning")
            elif self.entry.get()[0].isdigit() or not (self.entry2.get().isdigit() or self.entry2.get().count('.') == 1) or not (self.entry3.get().isdigit() or self.entry3.get().count('.') == 1) or not (self.entry4.get().isdigit() or self.entry4.get().count('.') == 1):
                  mixer.music.load("sounds/error.mp3")
                  mixer.music.play()
                  messagebox.showwarning("Warning Message","قيم الإدخال غير صحيحة",icon="warning")
            elif self.is_exists(self.entry.get()):
                 mixer.music.load("sounds/error.mp3")
                 mixer.music.play()
                 messagebox.showwarning("Warning Message","موجود في المخزن",icon="warning")
            else:
                    
                    self.convert_arabic_to_english(self.entry2)
                    self.convert_arabic_to_english(self.entry3)
                    self.convert_arabic_to_english(self.entry4)

                    current_date = datetime.now().date()
                    sql = "INSERT INTO Products (ProductName, Price,sell_Price,StockQuantity,ProductDate,Unit) VALUES (%s,%s,%s,%s,%s,%s)"
                    mycursor.execute(sql, (self.entry.get(),self.entry4.get(),self.entry2.get(),self.entry3.get(),current_date,self.unit_dropdown.get()))
                    mydb.commit()    
                    self.intTable()
                    self.entry.delete(0,'end')
                    self.entry2.delete(0,'end')
                    self.entry3.delete(0,'end')
                    self.entry4.delete(0,'end')

                    mixer.music.load("sounds/done.wav")
                    mixer.music.play()

        new_window = tk.Toplevel(self)
        new_window.geometry("500x600")
        new_window.title('Daftar Application')

        self.label = ck.CTkLabel(new_window, text='اضافة عنصر جديد ',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)


        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        label1 = ck.CTkLabel(new_window,width=200,text="الاسم:",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<Control-a>", lambda event: self.entry.select_range(0, 'end'))
        self.entry.bind("<Control-c>", lambda event: self.entry.clipboard_append(self.entry.selection_get()))
        self.entry.bind("<Control-p>", lambda event: self.entry.insert('insert', self.entry.clipboard_get()))

        label3 = ck.CTkLabel(new_window,width=200,text="الكمية:",font=ck.CTkFont(size=21,weight="bold"))
        label3.pack(padx=10, pady=10)

        self.entry3 = ck.CTkEntry(new_window,width=200)
        self.entry3.pack(padx=10, pady=10)

        label4 = ck.CTkLabel(new_window,width=200,text="سعر الشراء:",font=ck.CTkFont(size=21,weight="bold"))
        label4.pack(padx=10, pady=10)

        self.entry4 = ck.CTkEntry(new_window,width=200)
        self.entry4.pack(padx=10, pady=10)

        label2 = ck.CTkLabel(new_window,width=200,text="سعر البيع:",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)

        self.entry2 = ck.CTkEntry(new_window,width=200)
        self.entry2.pack(padx=10, pady=10)



        self.unit_dropdown = ck.CTkComboBox(new_window, values=["قطعة","متر","صندوق","جوز","كيس","كيلو","طن","غير ذلك"])
        self.unit_dropdown.pack(pady=10)
        self.unit_dropdown.set("قطعة")

        ok_button = ck.CTkButton(new_window, text="إضافة", command=get)
        ok_button.pack(padx=10, pady=10)



    def plus_data(self):
        self.plus_window()

    def plus_window(self):

        def get():
           
            if (not entry or not (entry.get().isdigit()) or not(int(entry.get())>0)):
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
            else:
                    mixer.music.load("sounds/done.wav")
                    mixer.music.play()
                    self.convert_arabic_to_english(entry)

                    update_query = "UPDATE Products SET StockQuantity = %s WHERE ProductID=%s"
                    mycursor.execute(update_query, (float(entry.get())+float(self.entry2.get()),values[0]))
                    mydb.commit()
                 
                    self.intTable()
                    self.entry2.configure(state="normal")
                    num = self.entry2.get()
                    self.entry2.delete(0,'end')
                    self.entry2.insert(0,float(entry.get())+float(num))
                    self.entry2.configure(state="disabled")

                    entry.delete(0,'end')
                    entry.insert(0,0)
            

        new_window = tk.Toplevel(self)
        new_window.geometry("440x400")
        new_window.title('Daftar Application')

        self.label = ck.CTkLabel(new_window, text='تعزيز الكمية',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)

        selected_item = self.table.focus()
        values =  self.table.item(selected_item, 'values')


        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        label1 = ck.CTkLabel(new_window,width=200,text="الاسم:",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)

        self.entry.insert(0,values[1])
        self.entry.configure(state="disabled")

        label2 = ck.CTkLabel(new_window,width=200,text="الكمية:",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)

        self.entry2 = ck.CTkEntry(new_window,width=200)
        self.entry2.pack(padx=10, pady=10)

        self.entry2.insert(0,values[2])
        self.entry2.configure(state="disabled")

        inc_frame= ck.CTkFrame(new_window,fg_color="transparent")
        inc_frame.pack(pady=15)

        entry = ck.CTkEntry(inc_frame,width=120)
        entry.insert(0,0)
        entry.grid(row=0, column=1,padx=5)

        label = ck.CTkLabel(inc_frame,text="+",font=ck.CTkFont(size=15,weight="bold"))
        label.grid(row=0, column=0)

        
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

        def get(type,text0,window):

            text=self.convert_arabic_to_english2(text0)

            if type == "name":
                if (not text):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE Products SET ProductName = %s WHERE ProductID=%s"
                mycursor.execute(update_query, (text,values[0]))
                mydb.commit()

                self.intTable()
                self.entry.configure(state="normal")
                self.entry.delete(0,'end')
                self.entry.insert(0,text)
                self.entry.configure(state="disabled")

                mixer.music.load("sounds/done.wav")
                mixer.music.play()
                window.destroy()

            elif type == "sell": 
                if (not text or not (text.isdigit() or text.count('.') == 1) ):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                
                update_query = "UPDATE Products SET sell_Price = %s WHERE ProductID=%s"
                mycursor.execute(update_query, (text,values[0]))
                mydb.commit()

                self.intTable()
                self.entry2.configure(state="normal")
                self.entry2.delete(0,'end')
                self.entry2.insert(0,text)
                self.entry2.configure(state="disabled")

                mixer.music.load("sounds/done.wav")
                mixer.music.play()
                window.destroy()
 
            elif type == "cont": 
                if (not text or not (text.isdigit()) ):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE Products SET StockQuantity = %s WHERE ProductID=%s"
                mycursor.execute(update_query, (text,values[0]))
                mydb.commit()

                self.intTable()
                self.entry3.configure(state="normal")
                self.entry3.delete(0,'end')
                self.entry3.insert(0,text)
                self.entry3.configure(state="disabled")

                mixer.music.load("sounds/done.wav")
                mixer.music.play()
                window.destroy()
  
            elif type == "price": 
                if (not text or not (text.isdigit() or text.count('.') == 1) ):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE Products SET Price = %s WHERE ProductID=%s"
                mycursor.execute(update_query, (text,values[0]))
                mydb.commit()

                self.intTable()
                self.entry4.configure(state="normal")
                self.entry4.delete(0,'end')
                self.entry4.insert(0,text)
                self.entry4.configure(state="disabled")

                mixer.music.load("sounds/done.wav")
                mixer.music.play()
                window.destroy()
  
            elif type == "unit": 
                if (not text):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE Products SET Unit = %s WHERE ProductID=%s"
                mycursor.execute(update_query, (text,values[0]))
                mydb.commit()

                self.intTable()
                self.entry5.configure(state="normal")
                self.entry5.delete(0,'end')
                self.entry5.insert(0,text)
                self.entry5.configure(state="disabled")

                mixer.music.load("sounds/done.wav")
                mixer.music.play()
                window.destroy()
     
        def editName():
            nwindow = tk.Toplevel(self)
            nwindow.geometry("450x150")
            nwindow.title('Daftar Application ')

            center_x = int(760)
            center_y = int(300)
            nwindow.geometry(f"+{center_x}+{center_y}")

            label = ck.CTkLabel(nwindow, text=' الاسم الجديد',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold")) 
            label.pack(pady=5)

            entryN = ck.CTkEntry(nwindow,width=270)
            entryN.pack(padx=10, pady=10)

            entryN.insert(0,self.entry.get())

            ok_button = ck.CTkButton(nwindow, text="تعديل", command=lambda:get("name",entryN.get(),nwindow))
            ok_button.pack(padx=10, pady=10)  

            

        def editSell():
            nwindow = tk.Toplevel(self)
            nwindow.geometry("450x250")
            nwindow.title('Daftar Application ')

            center_x = int(760)
            center_y = int(300)
            nwindow.geometry(f"+{center_x}+{center_y}")

            self.label = ck.CTkLabel(nwindow, text=' سعر البيع الجديد ',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold")) 
            self.label.pack(pady=5)

            entryN = ck.CTkEntry(nwindow,width=270)
            entryN.pack(padx=10, pady=10)

            entryN.insert(0,self.entry2.get())

            ok_button = ck.CTkButton(nwindow, text="تعديل", command=lambda:get("sell",entryN.get(),nwindow))
            ok_button.pack(padx=10, pady=10)  

        def editPrice():
            new_window = tk.Toplevel(self)
            new_window.geometry("450x250")
            new_window.title('Daftar Application ')

            center_x = int(760)
            center_y = int(300)
            new_window.geometry(f"+{center_x}+{center_y}")

            self.label = ck.CTkLabel(new_window, text='تعديل سعر الشراء',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold")) 
            self.label.pack(pady=5)

            entryN = ck.CTkEntry(new_window,width=270)
            entryN.pack(padx=10, pady=10)

            entryN.insert(0,self.entry4.get())

            ok_button = ck.CTkButton(new_window, text="تعديل", command=lambda:get("price",entryN.get(),new_window))
            ok_button.pack(padx=10, pady=10)  

        def editCont():
            new_window = tk.Toplevel(self)
            new_window.geometry("450x250")
            new_window.title('Daftar Application ')

            center_x = int(760)
            center_y = int(300)
            new_window.geometry(f"+{center_x}+{center_y}")

            self.label = ck.CTkLabel(new_window, text='تعديل الكمية',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold")) 
            self.label.pack(pady=5)

            entryN = ck.CTkEntry(new_window,width=270)
            entryN.pack(padx=10, pady=10)

            entryN.insert(0,self.entry3.get())

            ok_button = ck.CTkButton(new_window, text="تعديل", command=lambda:get("cont",entryN.get(),new_window))
            ok_button.pack(padx=10, pady=10)  

        def editUnit():
            new_window = tk.Toplevel(self)
            new_window.geometry("450x250")
            new_window.title('Daftar Application ')
            center_x = int(760)
            center_y = int(300)
            new_window.geometry(f"+{center_x}+{center_y}")

            self.label = ck.CTkLabel(new_window, text='تعديل الوحدة',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold")) 
            self.label.pack(pady=5)

            self.unit_dropdown = ck.CTkComboBox(new_window, values=["حبة", "صندوق", "كيس","كيلو","طن","غير ذلك"])
            self.unit_dropdown.pack(pady=10)
            self.unit_dropdown.set(self.entry5.get())

            ok_button = ck.CTkButton(new_window, text="تعديل", command=lambda:get("unit",self.unit_dropdown.get(),new_window))
            ok_button.pack(padx=10, pady=10)  


        new_window = tk.Toplevel(self)
        new_window.geometry("500x700")
        new_window.title('Daftar Application ')

        self.label = ck.CTkLabel(new_window, text='تعديل عنصر',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)

        center_x = int(750)
        center_y = int(200)
        new_window.geometry(f"+{center_x}+{center_y}")

        original_image = Image.open("imags/edit.png")
        self.editMG = original_image.resize((15, 15))
        self.editMG = ImageTk.PhotoImage(self.editMG)


        label1 = ck.CTkLabel(new_window,width=200,text="الاسم:",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)
        self.editName_butt = tk.Button(new_window,image=self.editMG,command=editName)
        self.editName_butt.pack()  

        self.entry = ck.CTkEntry(new_window,width=270)
        self.entry.pack(padx=10, pady=10)

        label2 = ck.CTkLabel(new_window,width=200,text="سعر البيع:",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)
        self.editSellPrice_butt = tk.Button(new_window,image=self.editMG,command=editSell)
        self.editSellPrice_butt.pack()  

        self.entry2 = ck.CTkEntry(new_window,width=200)
        self.entry2.pack(padx=10, pady=10)
        

        label3 = ck.CTkLabel(new_window,width=200,text="الكمية:",font=ck.CTkFont(size=21,weight="bold"))
        label3.pack(padx=10, pady=10)
        self.editCont_butt = tk.Button(new_window,image=self.editMG,command=editCont)
        self.editCont_butt.pack()  

        self.entry3 = ck.CTkEntry(new_window,width=200)
        self.entry3.pack(padx=10, pady=10)

        label4 = ck.CTkLabel(new_window,width=200,text="سعر الشراء:",font=ck.CTkFont(size=21,weight="bold"))
        label4.pack(padx=10, pady=10)
        self.editPrice_butt = tk.Button(new_window,image=self.editMG,command=editPrice)
        self.editPrice_butt.pack()  

        self.entry4 = ck.CTkEntry(new_window,width=200)
        self.entry4.pack(padx=10, pady=10)

        label5 = ck.CTkLabel(new_window,width=200,text="الصنف:",font=ck.CTkFont(size=21,weight="bold"))
        label5.pack(padx=10, pady=10)
        self.editUnit_butt = tk.Button(new_window,image=self.editMG,command=editUnit)
        self.editUnit_butt.pack()  

        self.entry5 = ck.CTkEntry(new_window,width=200)
        self.entry5.pack(padx=10, pady=10)
 
        selected_item = self.table.focus()

        values =  self.table.item(selected_item, 'values')

        self.entry.delete(0,'end')
        self.entry2.delete(0,'end')
        self.entry3.delete(0,'end')
        self.entry4.delete(0,'end')
        self.entry5.delete(0,'end')

        self.entry.insert(0,values[1])
        self.entry2.insert(0,values[4])
        self.entry3.insert(0,values[2])
        self.entry4.insert(0,values[6])
        self.entry5.insert(0,values[3])

        self.entry.configure(state="disabled")
        self.entry2.configure(state="disabled")
        self.entry3.configure(state="disabled")
        self.entry4.configure(state="disabled")
        self.entry5.configure(state="disabled") 

    def delete_item(self):
         selected_item = self.table.focus()
         if selected_item:
            values = self.table.item(selected_item, "values")
            mixer.music.load("sounds/warning.wav")
            mixer.music.play()
            sure = messagebox.askyesno("Confirmation", f"متأكد ؟ \n حذف {values[1]}",icon="warning")
            if sure :
                try:
                    mycursor.execute("DELETE FROM Products WHERE ProductID = %s",(values[0],))
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
                self.plus_button.configure(state="normal") 
        else :
                self.edit_button.configure(state="disabled")
                self.delete_button.configure(state="disabled")  
                self.plus_button.configure(state="disabled")      


    def Xprint(self):

        new_window = tk.Toplevel(self)
        new_window.geometry("440x250")
        new_window.title('Daftar Application')

        self.label = ck.CTkLabel(new_window, text='طباعة تقارير',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)

        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")


        print1_button = ck.CTkButton(new_window, text="تقرير جرد مخازن", command=self.printAssist,fg_color="green",font=ck.CTkFont(size=15,weight="bold"))
        print1_button.pack(padx=10, pady=15)   

        print2_button = ck.CTkButton(new_window, text="تقرير جرد مخازن مع شؤون مالية", command=self.printAssist2,fg_color="green",font=ck.CTkFont(size=15,weight="bold"))
        print2_button.pack(padx=10, pady=15)   

    def is_exists(self,name):
    
        select_query = "SELECT * FROM Products WHERE ProductName = %s"
    
        try:
            mycursor.execute(select_query, (name,))
            result = mycursor.fetchall()
            return bool(result)
        
        except mysql.connector.Error as err:
            return False
        
    def printAssist2(self):
        
            sql_query = """
                    SELECT ProductID,ProductName, sell_Price ,StockQuantity,Unit,Price
                    FROM Products
                """

            mycursor.execute(sql_query)

            results = mycursor.fetchall()


            table_data = [['رمز الصنف', 'اسم الصنف', 'سعر البيع', 'كمية','وحدة','سعر الشراء','#']]

            i=1
            for row in results:
                table_row = [row[0], row[1], row[2], row[3],row[4],row[5],i]
                table_data.append(table_row)
                i+=1
    
            self.print2(table_data,f"storeReport_Admins.pdf")
         


    def print2(self,schedule_data,output_filename):
        pdf = SimpleDocTemplate(output_filename, pagesize=letter)
        pdfmetrics.registerFont(TTFont('Arabic', 'arfonts-traditional-arabic-bold/traditional-arabic-bold.ttf'))
        
        company_info = {
        'name': 'المخماسي لمواد البناء والادوات الصحية',
        'telephone': '0569-660392',
        'address': 'مخماس - الشارع الرئيسي'
        }
        
        text = company_info['name']
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text1 = get_display(reshaped_text)

        text = company_info['telephone']
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text2 = get_display(reshaped_text)

        text = company_info['address']
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text3 = get_display(reshaped_text)

        pdf_canvas = canvas.Canvas(output_filename, pagesize=letter)

        pdf_canvas.setFont("Arabic", 20)

        middle_x = letter[0] / 2
        company_name_x = middle_x-21 - pdf_canvas.stringWidth(bidi_text1, "Arabic", 14) / 2


        pdf_canvas.drawString(company_name_x, 750, bidi_text1)

        pdf_canvas.setFont("Arabic", 12)

        pdf_canvas.drawString(30, 730, f"{bidi_text2}")

        address_width = pdf_canvas.stringWidth(bidi_text3, "Arabic", 12)
        pdf_canvas.drawString(letter[0] - address_width - 30, 730, bidi_text3)

        line_start = 30
        line_end = letter[0] - 30
        pdf_canvas.line(line_start, 700, line_end, 700)


        title = "كشف مخازن - نسخة خاصة"
        pdf_canvas.setFont("Arabic", 23)
        reshaped_text = arabic_reshaper.reshape(title)
        bidi_text4 = get_display(reshaped_text)
        title_width = pdf_canvas.stringWidth(bidi_text4, "Arabic", 18)
        title_x = (letter[0] - title_width) / 2
        pdf_canvas.drawString(title_x-5, 670, bidi_text4)

        
        cell_height = 20

        x_start = 60
        y_start = 585

        pdf_canvas.setFont("Arabic", 12)

        def draw_table_row(row, y):
                pdf_canvas.setFont("Arabic", 12)

                cell_width = 60
                x = x_start + 0 * cell_width
                reshaped_text = arabic_reshaper.reshape(f"{str(row[0])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(x + 7, y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
                pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

                cell_width = 170
                reshaped_text = arabic_reshaper.reshape(f"{str(row[1])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(205 - pdf_canvas.stringWidth(bidi_text, "Arabic", 12) / 2 , y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(120, y + 21, 160 + cell_width, y + 21)
                pdf_canvas.rect(120, y + 21, cell_width, -cell_height, stroke=1, fill=0)

                cell_width = 60
                x = x_start + 3.83 * cell_width
                reshaped_text = arabic_reshaper.reshape(f"{str(row[2])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(x + 7, y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
                pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

                cell_width = 60
                x = x_start + 4.83 * cell_width
                reshaped_text = arabic_reshaper.reshape(f"{str(row[3])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(x + 7, y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
                pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)
                
                cell_width = 60
                x = x_start + 5.83 * cell_width
                reshaped_text = arabic_reshaper.reshape(f"{str(row[4])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(x + 7, y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
                pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

                cell_width = 60
                x = x_start + 6.83 * cell_width
                reshaped_text = arabic_reshaper.reshape(f"{str(row[5])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(x + 7, y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
                pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

                cell_width = 30
                x = x_start + 15.68 * cell_width
                reshaped_text = arabic_reshaper.reshape(f"{str(row[6])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(x + 12, y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
                pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)


        row_index=1
        for row in (schedule_data):
            y = y_start - (row_index-1) * cell_height

            if y <= 30:
                pdf_canvas.showPage()
                y_start = 740
                row_index=1
                y = y_start

            row_index+=1  
            draw_table_row(row, y)


        pdf_canvas.save()
                

        pdf_absolute_path = os.path.abspath(output_filename)

        if sys.platform.startswith('win'):
            os.startfile(pdf_absolute_path)
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', pdf_absolute_path])
        elif sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', pdf_absolute_path])
        else:
            webbrowser.open(pdf_absolute_path)    
        

        
    def printAssist(self):
        
            sql_query = """
                    SELECT ProductID,ProductName ,StockQuantity,Unit
                    FROM Products
                """

            mycursor.execute(sql_query)

            results = mycursor.fetchall()


            table_data = [['رمز الصنف', 'اسم الصنف', 'كمية','وحدة','#']]

            i=1
            for row in results:
                table_row = [row[0], row[1], row[2], row[3],i]
                table_data.append(table_row)
                i+=1

    
            self.print1(table_data,f"storeReport.pdf")
         


    def print1(self,schedule_data,output_filename):
        pdf = SimpleDocTemplate(output_filename, pagesize=letter)
        pdfmetrics.registerFont(TTFont('Arabic', 'arfonts-traditional-arabic-bold/traditional-arabic-bold.ttf'))
        
        company_info = {
        'name': 'المخماسي لمواد البناء والادوات الصحية',
        'telephone': '0569-660392',
        'address': 'مخماس - الشارع الرئيسي'
        }
        
        text = company_info['name']
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text1 = get_display(reshaped_text)

        text = company_info['telephone']
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text2 = get_display(reshaped_text)

        text = company_info['address']
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text3 = get_display(reshaped_text)

        pdf_canvas = canvas.Canvas(output_filename, pagesize=letter)

        pdf_canvas.setFont("Arabic", 20)

        middle_x = letter[0] / 2
        company_name_x = middle_x-21 - pdf_canvas.stringWidth(bidi_text1, "Arabic", 14) / 2


        pdf_canvas.drawString(company_name_x, 750, bidi_text1)

        pdf_canvas.setFont("Arabic", 12)

        pdf_canvas.drawString(30, 730, f"{bidi_text2}")

        address_width = pdf_canvas.stringWidth(bidi_text3, "Arabic", 12)
        pdf_canvas.drawString(letter[0] - address_width - 30, 730, bidi_text3)

        line_start = 30
        line_end = letter[0] - 30
        pdf_canvas.line(line_start, 700, line_end, 700)


        title = "كشف مخازن"
        pdf_canvas.setFont("Arabic", 23)
        reshaped_text = arabic_reshaper.reshape(title)
        bidi_text4 = get_display(reshaped_text)
        title_width = pdf_canvas.stringWidth(bidi_text4, "Arabic", 18)
        title_x = (letter[0] - title_width) / 2
        pdf_canvas.drawString(title_x-5, 670, bidi_text4)

        
        cell_height = 20

        x_start = 125
        y_start = 585

        pdf_canvas.setFont("Arabic", 12)

        def draw_table_row(row, y):
                pdf_canvas.setFont("Arabic", 12)

                cell_width = 60
                x = x_start + 0 * cell_width
                reshaped_text = arabic_reshaper.reshape(f"{str(row[0])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(x + 12, y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
                pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

                cell_width = 170
                reshaped_text = arabic_reshaper.reshape(f"{str(row[1])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(270 - pdf_canvas.stringWidth(bidi_text, "Arabic", 12) / 2 , y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(185, y + 21, 185 + cell_width, y + 21)
                pdf_canvas.rect(185, y + 21, cell_width, -cell_height, stroke=1, fill=0)

                cell_width = 60
                x = x_start + 3.83 * cell_width
                reshaped_text = arabic_reshaper.reshape(f"{str(row[2])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(x + 12, y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
                pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

                cell_width = 60
                x = x_start + 4.83 * cell_width
                reshaped_text = arabic_reshaper.reshape(f"{str(row[3])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(x + 12, y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
                pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

                cell_width = 30
                x = x_start + 11.68 * cell_width
                reshaped_text = arabic_reshaper.reshape(f"{str(row[4])} ")
                bidi_text = get_display(reshaped_text)
                pdf_canvas.drawString(x + 12, y + 5, bidi_text)
                pdf_canvas.setStrokeColor(colors.blue)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
                pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)
                
        row_index=1
        for row in (schedule_data):
            y = y_start - (row_index-1) * cell_height

            if y <= 30:
                pdf_canvas.showPage()
                y_start = 740
                row_index=1
                y = y_start

            row_index+=1  
            draw_table_row(row, y)


        pdf_canvas.save()
                

        pdf_absolute_path = os.path.abspath(output_filename)

        if sys.platform.startswith('win'):
            os.startfile(pdf_absolute_path)
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', pdf_absolute_path])
        elif sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', pdf_absolute_path])
        else:
            webbrowser.open(pdf_absolute_path)    

    def convert_arabic_to_english(self,entry):
        arabic_to_english = {
            '٠': '0',
            '١': '1',
            '٢': '2',
            '٣': '3',
            '٤': '4',
            '٥': '5',
            '٦': '6',
            '٧': '7',
            '٨': '8',
            '٩': '9'
        }

        entry_value = entry.get()

        for arabic_digit, english_digit in arabic_to_english.items():
            entry_value = entry_value.replace(arabic_digit, english_digit)

        entry.delete(0,"end")
        entry.insert(0,entry_value)

    def convert_arabic_to_english2(self,text):
        arabic_to_english = {
            '٠': '0',
            '١': '1',
            '٢': '2',
            '٣': '3',
            '٤': '4',
            '٥': '5',
            '٦': '6',
            '٧': '7',
            '٨': '8',
            '٩': '9'
        }

        entry_value = text

        for arabic_digit, english_digit in arabic_to_english.items():
            entry_value = entry_value.replace(arabic_digit, english_digit)

        text1=entry_value
        return text1

