
import customtkinter as ck
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from db import mycursor,mydb
import mysql.connector
from datetime import datetime
from PIL import Image,ImageTk
from pygame import mixer


class Suppliers(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

        self.bookmark_image = ck.CTkImage(Image.open("imags/delivery-courier.png"),size=(40,40))
        self.label = ck.CTkLabel(self, text="المزودين ",image=self.bookmark_image,corner_radius=20,compound="right",height=50,font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)
        

        self.search_entry = ck.CTkEntry(self,placeholder_text="search")
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<KeyRelease>", self.search)

        columns = ('id','name', 'phone')

        self.table = ttk.Treeview(self,
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

        button_frame = ck.CTkFrame(self,fg_color="transparent")
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
                    sql = "INSERT INTO Suppliers (SupplierName,ContactNumber) VALUES (%s,%s)"
                    mycursor.execute(sql, (self.entry.get(),self.entry2.get()))
                    mydb.commit()    
                    self.intTable()
                    self.entry.delete(0,'end')
                    self.entry2.delete(0,'end')
                  
                    mixer.music.load("sounds/done.wav")
                    mixer.music.play()

                    new_window.destroy()

        new_window = tk.Toplevel(self)
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

            

        def editPhone():
            nwindow = tk.Toplevel(self)
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


        new_window = tk.Toplevel(self)
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

    def show_detial(self):
         selected_item = self.table.focus()
         if selected_item:
            self.show_detial_info()
         else:  
             mixer.music.load("sounds/error.mp3")
             mixer.music.play()
             messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")

    def show_detial_info(self):
        
        new_window = tk.Toplevel(self)
        new_window.geometry("760x660")
        new_window.title('Daftar Application')
        

        center_x = int(580)
        center_y = int(150)
        new_window.geometry(f"+{center_x}+{center_y}")

        label = ck.CTkLabel(new_window,width=200,text="تفاصيل" ,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold"))
        label.pack(pady=10)
       
        
        selected_item = self.table.focus()
        values =  self.table.item(selected_item, 'values')

        columns = ("id","total","date")
        self.table2 = ttk.Treeview(new_window,columns=columns,height=12, selectmode='browse',show='headings')

        self.table2.column("id", anchor="center",width=110,minwidth=110)
        self.table2.column("total", anchor="center",width=110, minwidth=110)
        self.table2.column("date", anchor="center",width=110, minwidth=110)
     
        self.table2.heading('id', text='رمز فاتورة الشراء')
        self.table2.heading("total", text='مجموع')
        self.table2.heading('date', text='التاريخ')

        self.table2.bind('<Motion>','break')

        name_var = tk.StringVar()
        name_var.set(values[1])   
        
        labelFrame =ck.CTkFrame(new_window,fg_color="transparent")
        labelFrame.pack(padx=15,pady=25)

        label1 = ck.CTkLabel(labelFrame,width=200,text="الاسم: " +name_var.get() ,font=ck.CTkFont(size=19,weight="bold"))
        label1.grid(row=0, column=2, padx=10)
        
        self.table2.pack(pady=20)

        button_frame = ck.CTkFrame(new_window,fg_color="transparent")
        button_frame.pack(fill=ck.Y,expand=True,padx=15,pady=45)

        self.detial_button2 = ck.CTkButton(button_frame, text="تفاصيل",fg_color="green",height=20,command=self.show_detial,font=ck.CTkFont(size=16,weight="bold"))
        self.detial_button2.grid(row=0, column=0, padx=10)
        
        self.add_button2 = ck.CTkButton(button_frame, text="اضافة فاتورة مشتريات",height=20,command=self.add_data,font=ck.CTkFont(size=16,weight="bold"))
        self.add_button2.grid(row=0, column=1, padx=10)

        self.edit_button2 = ck.CTkButton(button_frame, text="تعديل",height=20,command=self.edit_item,font=ck.CTkFont(size=16,weight="bold"))
        self.edit_button2.grid(row=0, column=2, padx=10)

        self.delete_button2 = ck.CTkButton(button_frame, text="حذف",height=20,fg_color="red", command=self.delete_item,font=ck.CTkFont(size=16,weight="bold"))
        self.delete_button2.grid(row=0, column=3, padx=10)

        self.detial_button2.configure(state="disabled")
        self.edit_button2.configure(state="disabled")
        self.delete_button2.configure(state="disabled")       

        self.intTable2()


    def intTable2(self):
        for row in self.table2.get_children():
            self.table2.delete(row)

        sql_query = """
                    SELECT Products.ProductID, Products.ProductName, Products.sell_Price ,OrderDetails.Quantity,OrderDetails.Subtotal
                    FROM Orders
                    JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
                    JOIN Products ON OrderDetails.ProductID = Products.ProductID
                    WHERE Orders.OrderID = %s;
                """

        # mycursor.execute(sql_query, (values[0],))
        results = mycursor.fetchall()

        for site in results:
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

    def is_exists(self,name):
    
        select_query = "SELECT * FROM Suppliers WHERE SupplierID = %s"
    
        try:
            mycursor.execute(select_query, (name,))
            result = mycursor.fetchall()
            return bool(result)
        
        except mysql.connector.Error as err:
            messagebox.showwarning("Warning Message","حركة خاطئة",icon="warning")
            return False
        
        