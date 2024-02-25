
import customtkinter as ck
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from db import mycursor,mydb
import mysql.connector
from datetime import datetime
from PIL import Image,ImageTk
from tkcalendar import Calendar
from pygame import mixer


class Suppliers(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.main_frame = ck.CTkFrame(self,fg_color="transparent")
        self.main_frame.grid(row=0, column=0,pady=60)
        self.grid_columnconfigure(0, weight=10)

        self.bookmark_image = ck.CTkImage(Image.open("imags/delivery-courier.png"),size=(40,40))
        self.label = ck.CTkLabel(self.main_frame, text="المزودين ",image=self.bookmark_image,corner_radius=20,compound="right",height=50,font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)
        

        self.search_entry = ck.CTkEntry(self.main_frame,placeholder_text="search")
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<KeyRelease>", self.search)

        columns = ('id','name', 'phone')

        self.table = ttk.Treeview(self.main_frame,
                              columns=columns,
                              height=16,
                              selectmode='browse',
                              show='headings')

        self.table.column("#1", anchor="c", minwidth=100, width=100)
        self.table.column("#2", anchor="c", minwidth=220, width=220)
        self.table.column("#3", anchor="c", minwidth=100, width=100)

        self.table.heading('id', text='رمز المزود')
        self.table.heading('name', text='اسم المزود')
        self.table.heading('phone', text='هاتف')
    

        self.table.bind('<Motion>', 'break')
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)

        self.table.pack(pady=15)

        button_frame = ck.CTkFrame(self.main_frame,fg_color="transparent")
        button_frame.pack(fill=ck.Y,expand=True,padx=15,pady=45)

        self.detial_button = ck.CTkButton(button_frame, text="تفاصيل",fg_color="green",height=30,command=self.show_detial,font=ck.CTkFont(size=20,weight="bold"))
        self.detial_button.grid(row=0, column=0, padx=10)
        
        self.add_button = ck.CTkButton(button_frame, text="اضافة مزود جديد",height=30,command=self.add_data,font=ck.CTkFont(size=20,weight="bold"))
        self.add_button.grid(row=0, column=1, padx=10)

        self.edit_button = ck.CTkButton(button_frame, text="تعديل",height=30,command=self.edit_item,font=ck.CTkFont(size=20,weight="bold"))
        self.edit_button.grid(row=0, column=2, padx=10)

        self.delete_button = ck.CTkButton(button_frame, text="حذف",height=30,fg_color="red", command=self.delete_item,font=ck.CTkFont(size=20,weight="bold"))
        self.delete_button.grid(row=0, column=3, padx=10)

        self.detial_button.configure(state="disabled")
        self.edit_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")       

        self.intTable()


    def intTable(self):

        for row in self.table.get_children():
            self.table.delete(row)

        mycursor.execute("SELECT * FROM Suppliers")
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
            list =[self.entry]
            entry_texts = [entry.get() for entry in list]
            if any(not text for text in entry_texts):
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","قم بادخال جميع الحقول",icon="warning")

            elif self.is_exists(self.entry.get()):
                 mixer.music.load("sounds/error.mp3")
                 mixer.music.play()
                 messagebox.showwarning("Warning Message","موجود !!",icon="warning")
            else:
                    self.convert_arabic_to_english(self.entry2)
                    sql = "INSERT INTO Suppliers (SupplierName,ContactNumber) VALUES (%s,%s)"
                    mycursor.execute(sql, (self.entry.get(),self.entry2.get()))
                    mydb.commit()    
                    self.intTable()
                    self.entry.delete(0,'end')
                    self.entry2.delete(0,'end')
                  
                    mixer.music.load("sounds/done.wav")
                    mixer.music.play()

                    new_window.destroy()

        new_window = tk.Toplevel(self.main_frame)
        new_window.geometry("420x380")
        new_window.title('Daftar Application')

        self.label = ck.CTkLabel(new_window, text='اضافة مزود',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)


        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        label1 = ck.CTkLabel(new_window,width=200,text="الاسم:",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)

        label2 = ck.CTkLabel(new_window,width=200,text="هاتف:",font=ck.CTkFont(size=21,weight="bold"))
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

        def get(type,text,window):

            if type == "name":
                if (not text):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE Suppliers SET SupplierName = %s WHERE SupplierID=%s"
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

            elif type == "phone": 
                if (not text):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE Suppliers SET ContactNumber = %s WHERE SupplierID=%s"
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
 
    
        def editName():
            nwindow = tk.Toplevel(self.main_frame)
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

            self.convert_arabic_to_english(entryN)
            ok_button = ck.CTkButton(nwindow, text="تعديل", command=lambda:get("name",entryN.get(),nwindow))
            ok_button.pack(padx=10, pady=10)  

            

        def editPhone():
            nwindow = tk.Toplevel(self.main_frame)
            nwindow.geometry("450x250")
            nwindow.title('Daftar Application ')

            center_x = int(760)
            center_y = int(300)
            nwindow.geometry(f"+{center_x}+{center_y}")

            self.label = ck.CTkLabel(nwindow, text=' رقم الهاتف الجديد ',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold")) 
            self.label.pack(pady=5)

            entryN = ck.CTkEntry(nwindow,width=270)
            entryN.pack(padx=10, pady=10)

            entryN.insert(0,self.entry2.get())

            ok_button = ck.CTkButton(nwindow, text="تعديل", command=lambda:get("phone",entryN.get(),nwindow))
            ok_button.pack(padx=10, pady=10)  


        new_window = tk.Toplevel(self.main_frame)
        new_window.geometry("420x380")
        new_window.title('Daftar Application ')

        self.label = ck.CTkLabel(new_window, text='تعديل المزود',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
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

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)

        label2 = ck.CTkLabel(new_window,width=200,text=" هاتف:",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)
        self.editPhone_butt = tk.Button(new_window,image=self.editMG,command=editPhone)
        self.editPhone_butt.pack()  

        self.entry2 = ck.CTkEntry(new_window,width=200)
        self.entry2.pack(padx=10, pady=10)
        
        selected_item = self.table.focus()

        values =  self.table.item(selected_item, 'values')

        self.entry.delete(0,'end')
        self.entry2.delete(0,'end')

        self.entry.insert(0,values[1])
        self.entry2.insert(0,values[2])

        self.entry.configure(state="disabled")
        self.entry2.configure(state="disabled")

    def edit_item2(self):
         selected_item = self.table2.focus()
         if selected_item:
            self.edit_window2()
         else:  
             mixer.music.load("sounds/error.mp3")
             mixer.music.play()
             messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")

    def edit_window2(self):

        def get(type,text,window):

            if type == "name":
                if (not text):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE purchases SET info = %s WHERE Id=%s"
                mycursor.execute(update_query, (text,values[0]))
                mydb.commit()

                self.intTable2()
                self.entry.configure(state="normal")
                self.entry.delete(0,'end')
                self.entry.insert(0,text)
                self.entry.configure(state="disabled")

                mixer.music.load("sounds/done.wav")
                mixer.music.play()
                window.destroy()

            elif type == "price": 
                if (not text):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE purchases SET Amount = %s WHERE Id=%s"
                mycursor.execute(update_query, (text,values[0]))
                mydb.commit()

                self.intTable2()
                self.entry2.configure(state="normal")
                self.entry2.delete(0,'end')
                self.entry2.insert(0,text)
                self.entry2.configure(state="disabled")

                mixer.music.load("sounds/done.wav")
                mixer.music.play()
                window.destroy()
 
    
        def editName():
            nwindow = tk.Toplevel(self.main_frame)
            nwindow.geometry("450x150")
            nwindow.title('Daftar Application ')

            center_x = int(760)
            center_y = int(300)
            nwindow.geometry(f"+{center_x}+{center_y}")

            label = ck.CTkLabel(nwindow, text=' الوصف الجديد',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold")) 
            label.pack(pady=5)

            entryN = ck.CTkEntry(nwindow,width=270)
            entryN.pack(padx=10, pady=10)

            entryN.insert(0,self.entry.get())

            self.convert_arabic_to_english(entryN)
            ok_button = ck.CTkButton(nwindow, text="تعديل", command=lambda:get("name",entryN.get(),nwindow))
            ok_button.pack(padx=10, pady=10)  

            

        def editPhone():
            nwindow = tk.Toplevel(self.main_frame)
            nwindow.geometry("450x250")
            nwindow.title('Daftar Application ')

            center_x = int(760)
            center_y = int(300)
            nwindow.geometry(f"+{center_x}+{center_y}")

            self.label = ck.CTkLabel(nwindow, text='قيمة السند الجديدة:',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold")) 
            self.label.pack(pady=5)

            entryN = ck.CTkEntry(nwindow,width=270)
            entryN.pack(padx=10, pady=10)

            entryN.insert(0,self.entry2.get())

            ok_button = ck.CTkButton(nwindow, text="تعديل", command=lambda:get("price",entryN.get(),nwindow))
            ok_button.pack(padx=10, pady=10)  


        new_window = tk.Toplevel(self.main_frame)
        new_window.geometry("420x380")
        new_window.title('Daftar Application ')

        self.label = ck.CTkLabel(new_window, text='تعديل سند الشراء',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)

        center_x = int(750)
        center_y = int(200)
        new_window.geometry(f"+{center_x}+{center_y}")

        original_image = Image.open("imags/edit.png")
        self.editMG = original_image.resize((15, 15))
        self.editMG = ImageTk.PhotoImage(self.editMG)


        label1 = ck.CTkLabel(new_window,width=200,text="الوصف :",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)
        self.editName_butt = tk.Button(new_window,image=self.editMG,command=editName)
        self.editName_butt.pack()  

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)

        label2 = ck.CTkLabel(new_window,width=200,text=" قيمة السند :",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)
        self.editPhone_butt = tk.Button(new_window,image=self.editMG,command=editPhone)
        self.editPhone_butt.pack()  

        self.entry2 = ck.CTkEntry(new_window,width=200)
        self.entry2.pack(padx=10, pady=10)
        
        selected_item = self.table2.focus()

        values =  self.table2.item(selected_item, 'values')

        self.entry.delete(0,'end')
        self.entry2.delete(0,'end')

        self.entry.insert(0,values[1])
        self.entry2.insert(0,values[3])

        self.entry.configure(state="disabled")
        self.entry2.configure(state="disabled")

    def delete_item(self):
         selected_item = self.table.focus()
         if selected_item:
            values = self.table.item(selected_item, "values")
            mixer.music.load("sounds/warning.wav")
            mixer.music.play()
            sure = messagebox.askyesno("Confirmation", f"متأكد ؟ \n حذف {values[1]}",icon="warning")
            if sure :
                try:
                    mycursor.execute("DELETE FROM Suppliers WHERE SupplierID = %s",(values[0],))
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
    
    def delete_item2(self):
         selected_item = self.table2.focus()
         if selected_item:
            values = self.table2.item(selected_item, "values")
            mixer.music.load("sounds/warning.wav")
            mixer.music.play()
            sure = messagebox.askyesno("Confirmation", f"متأكد ؟ \n حذف {values[1]}",icon="warning")
            if sure :
                try:
                    mycursor.execute("DELETE FROM purchases WHERE Id = %s",(values[0],))
                    mydb.commit() 
                    self.intTable2()
                    mixer.music.load("sounds/done.wav")
                    mixer.music.play()
                except mysql.connector.Error as err:
                    messagebox.showwarning("Warning Message","حركة خاطئة",icon="warning")  
                    self.intTable2() 
         else:  
            mixer.music.load("sounds/error.mp3")
            mixer.music.play()
            messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")

    def show_detial(self):
         selected_item = self.table.focus()
         if selected_item:
            self.show_detial_info()
         else:  
             mixer.music.load("sounds/error.mp3")
             mixer.music.play()
             messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")

    def show_detial_info(self):
        self.main_frame.grid_forget()
        self.detial_frame =ck.CTkFrame(self,fg_color="transparent")
        self.detial_frame.grid(row=0, column=0)
        
        label = ck.CTkLabel( self.detial_frame,width=200,text=" تفاصيل المزود" ,text_color="#2e8fe7",font=ck.CTkFont(size=25,weight="bold"))
        label.pack(pady=10)
       
        
        selected_item = self.table.focus()
        self.valuesO =  self.table.item(selected_item, 'values')
   

        columns = ("id","decrip","date","total","state")
        self.table2 = ttk.Treeview( self.detial_frame,columns=columns,height=14, selectmode='browse',show='headings')

        self.table2.column("id", anchor="center",width=110,minwidth=110)
        self.table2.column("decrip", anchor="center",width=150, minwidth=150)
        self.table2.column("total", anchor="center",width=110, minwidth=110)
        self.table2.column("date", anchor="center",width=110, minwidth=110)
        self.table2.column("state", anchor="center",width=90, minwidth=90)
     
        self.table2.heading('id', text='رمز سند الشراء')
        self.table2.heading('decrip', text='وصف')
        self.table2.heading("total", text='قيمة السند')
        self.table2.heading('date', text='التاريخ')
        self.table2.heading('state', text='مجموع الدفعات')


        self.table2.bind('<Motion>','break')
        self.table2.bind("<<TreeviewSelect>>", self.on_item_select2)

        name_var = tk.StringVar()
        name_var.set(self.valuesO[1])   
        
        
        label1 = ck.CTkLabel(self.detial_frame,width=200,text="الاسم: " +name_var.get(),text_color="#2e8fe7",font=ck.CTkFont(size=19,weight="bold"))
        label1.pack(pady=15)
        
        self.table2.pack(pady=20)

        button_frame = ck.CTkFrame(self.detial_frame,fg_color="transparent")
        button_frame.pack(fill=ck.Y,expand=True,padx=15,pady=45)

        self.detial_button2 = ck.CTkButton(button_frame, text="الدفعات",fg_color="green",height=20,command=self.show_detial2,font=ck.CTkFont(size=16,weight="bold"))
        self.detial_button2.grid(row=0, column=0, padx=10)
        
        self.add_button2 = ck.CTkButton(button_frame, text="اضافة فاتورة مشتريات",height=20,command=self.add_data2,font=ck.CTkFont(size=16,weight="bold"))
        self.add_button2.grid(row=0, column=1, padx=10)

        self.edit_button2 = ck.CTkButton(button_frame, text="تعديل",height=20,command=self.edit_item2,font=ck.CTkFont(size=16,weight="bold"))
        self.edit_button2.grid(row=0, column=2, padx=10)

        self.delete_button2 = ck.CTkButton(button_frame, text="حذف",height=20,fg_color="red", command=self.delete_item2,font=ck.CTkFont(size=16,weight="bold"))
        self.delete_button2.grid(row=0, column=3, padx=10)

        self.ret_button = ck.CTkButton(self.detial_frame, text="رجوع",height=20, command=self.ret,font=ck.CTkFont(size=16,weight="bold"))
        self.ret_button.pack(pady=20)

        self.detial_button2.configure(state="disabled")
        self.edit_button2.configure(state="disabled")
        self.delete_button2.configure(state="disabled")       

        self.intTable2()


    def intTable2(self):
        for row in self.table2.get_children():
            self.table2.delete(row)

        mycursor.execute("""
        SELECT 
            P.Id, 
            P.info, 
            P.Date, 
            P.Amount,
            COALESCE(SUM(PP.amount), 0) AS total_purchase_pay
        FROM 
            purchases P
        LEFT JOIN 
            Purchase_pay PP ON P.Id = PP.PurchasesId
        WHERE 
            P.SupplierID = %s
        GROUP BY 
            P.Id, P.info, P.Date, P.Amount
    """, (self.valuesO[0],))

        mysite = mycursor.fetchall()

        for site in mysite:
            self.table2.insert('','end',values=(site))

    def on_item_select(self,event):
        selected_item = self.table.focus()
        if selected_item:
                self.edit_button.configure(state="normal")
                self.delete_button.configure(state="normal")
                self.detial_button.configure(state="normal")
        else :
                self.edit_button.configure(state="disabled")
                self.delete_button.configure(state="disabled") 
                self.detial_button.configure(state="disabled")    
    
    
    def on_item_select2(self,event):
        selected_item = self.table2.focus()
        if selected_item:
                self.edit_button2.configure(state="normal")
                self.delete_button2.configure(state="normal")
                self.detial_button2.configure(state="normal")
        else :
                self.edit_button2.configure(state="disabled")
                self.delete_button2.configure(state="disabled") 
                self.detial_button2.configure(state="disabled")    

    def add_data2(self):
        self.add_window2()

    def add_window2(self):

        def get():
            list =[self.entry,self.entry2]
            entry_texts = [entry.get() for entry in list]
            if any(not text for text in entry_texts):
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","قم بادخال جميع الحقول",icon="warning")

            else:
                    selected_item = self.table.focus()
                    self.valuesO =  self.table.item(selected_item, 'values')
                    
                    self.convert_arabic_to_english(self.entry2)
                    current_date = datetime.now().date()
                    sql = "INSERT INTO purchases (Date,SupplierID,Amount,info) VALUES (%s,%s,%s,%s)"
                    mycursor.execute(sql, (current_date,self.valuesO[0],self.entry2.get(),self.entry.get()))
                    mydb.commit()    
                    self.intTable2()
                    self.entry.delete(0,'end')
                    self.entry2.delete(0,'end')
                  
                    mixer.music.load("sounds/done.wav")
                    mixer.music.play()

                    new_window.destroy()

        new_window = tk.Toplevel(self.main_frame)
        new_window.geometry("420x380")
        new_window.title('Daftar Application')

        self.label = ck.CTkLabel(new_window, text='اضافة سند مشتريات',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)

        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        label1 = ck.CTkLabel(new_window,width=200,text="وصف:",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)

        label2 = ck.CTkLabel(new_window,width=200,text="قيمة:",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)

        self.entry2 = ck.CTkEntry(new_window,width=200)
        self.entry2.pack(padx=10, pady=10)

        ok_button = ck.CTkButton(new_window, text="إضافة", command=get)
        ok_button.pack(padx=10, pady=10)

    def show_detial2(self):
        self.show_detial_info2()

    def show_detial_info2(self):

        selected_item2 = self.table2.focus()
        self.values2 =  self.table2.item(selected_item2, 'values')
        def pay():    

            def cash():
                list =[self.entry]
                entry_texts = [entry.get() for entry in list]
                if any(not text for text in entry_texts):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال جميع الحقول",icon="warning")

                if self.is_valid_entry(self.entry.get()):
                        
                        self.convert_arabic_to_english(self.entry)
                        current_date = datetime.now().date()
                        sql = "INSERT INTO Purchase_pay (Date,PurchasesId,Amount,payment_method) VALUES (%s,%s,%s,%s)"
                        mycursor.execute(sql, (current_date,self.values2[0],self.entry.get(),"cash"))
                        mydb.commit()    
                        intTable3()
                        self.entry.delete(0,'end')
                    
                        mixer.music.load("sounds/done.wav")
                        mixer.music.play()
                else:
                     mixer.music.load("sounds/error.mp3")
                     mixer.music.play()
                     messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")

            def check():
                list =[self.entry2,self.entry3]
                entry_texts = [entry.get() for entry in list]
                if any(not text for text in entry_texts):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال جميع الحقول",icon="warning")

                if self.is_valid_entry(self.entry3.get()) and  self.is_valid_entry(self.entry2.get()):
                
                        
                        self.convert_arabic_to_english(self.entry3)
                        self.convert_arabic_to_english(self.entry2)
                        sql = "INSERT INTO Checks (check_number,amount,check_date) VALUES (%s,%s,%s)"
                        mycursor.execute(sql, (self.entry2.get(),self.entry3.get(),cal.get_date()))
                        mydb.commit()   

                        id = mycursor.lastrowid
                        self.convert_arabic_to_english(self.entry3)
                        current_date = datetime.now().date()
                        sql = "INSERT INTO Purchase_pay (Date,PurchasesId,Amount,payment_method,check_id) VALUES (%s,%s,%s,%s,%s)"
                        mycursor.execute(sql, (current_date,self.values2[0],self.entry3.get(),"check",id))
                        mydb.commit() 

                        intTable3()
                        self.entry.delete(0,'end')
                    
                        mixer.music.load("sounds/done.wav")
                        mixer.music.play()
                else:
                     mixer.music.load("sounds/error.mp3")
                     mixer.music.play()
                     messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")

            new_window = tk.Toplevel(self.main_frame)
            new_window.geometry("560x500")
            new_window.title('Daftar Application')

            tabview = ck.CTkTabview(new_window, width=510,height=350)
            tabview.grid(padx=15,pady=(20, 0))
            tabview.add("كاش")
            tabview.add("شيك مالي")
            tabview.tab("كاش").grid_columnconfigure(0, weight=1)
            tabview.tab("شيك مالي").grid_columnconfigure(0, weight=1)  

            center_x = int(790)
            center_y = int(370)
            new_window.geometry(f"+{center_x}+{center_y}")

            label1 = ck.CTkLabel(tabview.tab("كاش"),width=200,text="قيمة :",font=ck.CTkFont(size=21,weight="bold"))
            label1.pack(padx=10, pady=10)

            self.entry = ck.CTkEntry(tabview.tab("كاش"),width=200)
            self.entry.pack(padx=10, pady=10)


            ok_button = ck.CTkButton(tabview.tab("كاش"), text="إضافة", command=cash)
            ok_button.pack(padx=10, pady=10)

            ###########
            label2 = ck.CTkLabel(tabview.tab("شيك مالي"),width=200,text="رقم الشيك :",font=ck.CTkFont(size=21,weight="bold"))
            label2.pack(padx=10, pady=10)

            self.entry2 = ck.CTkEntry(tabview.tab("شيك مالي"),width=200)
            self.entry2.pack(padx=10, pady=10)

            label3 = ck.CTkLabel(tabview.tab("شيك مالي"),width=200,text="قيمة الشيك :",font=ck.CTkFont(size=21,weight="bold"))
            label3.pack(padx=10, pady=10)

            self.entry3 = ck.CTkEntry(tabview.tab("شيك مالي"),width=200)
            self.entry3.pack(padx=10, pady=10)

            label4 = ck.CTkLabel(tabview.tab("شيك مالي"),width=200,text="تاريخ الاستحقاق :",font=ck.CTkFont(size=21,weight="bold"))
            label4.pack(padx=10, pady=10)

            cal = Calendar(tabview.tab("شيك مالي"), selectmode='day',
            showweeknumbers=False, cursor="hand2", date_pattern= 'y-m-d',
            borderwidth=1)
            cal.pack(padx=10, pady=10)

            ok2_button = ck.CTkButton(tabview.tab("شيك مالي"), text="إضافة", command=check)
            ok2_button.pack(padx=10, pady=10)

        def checkInfo():
                
                def intTable4():
                    for row in self.table4.get_children():
                        self.table4.delete(row)

                    mycursor.execute("""
                                    SELECT 
                                        C.check_number,
                                        S.SupplierName,
                                        C.amount AS check_amount,
                                        C.check_date
                                    FROM 
                                        Purchase_pay PP
                                    JOIN 
                                        Checks C ON PP.check_id = C.check_id
                                    JOIN 
                                        Purchases P ON PP.PurchasesId = P.Id
                                    JOIN 
                                        Suppliers S ON P.SupplierID = S.SupplierID
                                    WHERE 
                                        P.Id =%s ;
                                """,(self.values2[0],))
                    mysite = mycursor.fetchall()
                    for site in mysite:
                        self.table4.insert('','end',values=(site))

                new_window = tk.Toplevel(self.main_frame)
                new_window.geometry("550x450")
                new_window.title('Daftar Application')      
                self.label = ck.CTkLabel(new_window, text='تفاصيل الشيكات',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
                self.label.pack(pady=5)

                center_x = int(750)
                center_y = int(350)
                new_window.geometry(f"+{center_x}+{center_y}")

                columns = ("id","name","amount","date")
                self.table4 = ttk.Treeview(new_window,columns=columns,height=11, selectmode='browse',show='headings')

                self.table4.column("id", anchor="center",width=70,minwidth=70)
                self.table4.column("name", anchor="center",width=110, minwidth=110)
                self.table4.column("amount", anchor="center",width=110, minwidth=110)
                self.table4.column("date", anchor="center",width=100, minwidth=100)
            
                self.table4.heading('id', text="رقم الشيك")
                self.table4.heading('name', text='الاسم')
                self.table4.heading("amount", text='القيمة')
                self.table4.heading('date', text='التاريخ الاستحقاق')

                self.table4.bind('<Motion>','break')
                self.table4.pack(padx=10,pady=20)

                intTable4()      

        def intTable3():
            for row in self.table3.get_children():
                self.table3.delete(row)

            mycursor.execute("SELECT Id,payment_method,amount,Date FROM Purchase_pay Where PurchasesId = %s",(self.values2[0],))
            mysite = mycursor.fetchall()
            for site in mysite:
                self.table3.insert('','end',values=(site))

        new_window = tk.Toplevel(self.main_frame)
        new_window.geometry("650x550")
        new_window.title('Daftar Application')

        self.label = ck.CTkLabel(new_window, text='تفاصيل الدفعات',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)

        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        columns = ("id","method","amount","date")
        self.table3 = ttk.Treeview(new_window,columns=columns,height=10, selectmode='browse',show='headings')

        self.table3.column("id", anchor="center",width=70,minwidth=70)
        self.table3.column("method", anchor="center",width=100, minwidth=100)
        self.table3.column("amount", anchor="center",width=110, minwidth=110)
        self.table3.column("date", anchor="center",width=100, minwidth=100)
     
        self.table3.heading('id', text='رمز السند')
        self.table3.heading('method', text='طريقة الدفع')
        self.table3.heading("amount", text='القيمة')
        self.table3.heading('date', text='التاريخ')

        self.table3.bind('<Motion>','break')
        self.table3.pack(padx=10,pady=20)

        button_frame = ck.CTkFrame(new_window,fg_color="transparent")
        button_frame.pack(fill=ck.Y,expand=True,padx=15,pady=45) 

        self.detail_button = ck.CTkButton(button_frame, text="تفاصيل الشيكات",height=40,command=checkInfo,font=ck.CTkFont(size=20,weight="bold"))
        self.detail_button.grid(row=0, column=1, padx=10)

        self.pay_button2 = ck.CTkButton(button_frame, text="تسجيل دفعة",fg_color="green",command=pay,height=40,font=ck.CTkFont(size=20,weight="bold"))
        self.pay_button2.grid(row=0, column=0, padx=10)

        intTable3()    

    def is_exists(self,name):
    
        select_query = "SELECT * FROM Suppliers WHERE SupplierID = %s"
    
        try:
            mycursor.execute(select_query, (name,))
            result = mycursor.fetchall()
            return bool(result)
        
        except mysql.connector.Error as err:
            messagebox.showwarning("Warning Message","حركة خاطئة",icon="warning")
            return False
        
    def ret(self):
        self.detial_frame.grid_forget()
        self.main_frame.grid(row=0, column=0)

    def is_valid_entry(self,entry_value):
            try:
                float_value = float(entry_value)
                return True
            except ValueError:
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","ادخال خاطئ",icon="warning")
                return False
            
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
