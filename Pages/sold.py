
import customtkinter as ck
from PIL import Image,ImageTk
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from db import mycursor,mydb
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

class Sold(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)
    
        self.tabview = ck.CTkTabview(self, width=1200)
        self.tabview.grid(pady=(20, 0))
        self.tabview.add("مبيعات")
        self.tabview.add("زبائن")
        self.tabview.tab("مبيعات").grid_columnconfigure(0, weight=1)  
        self.tabview.tab("زبائن").grid_columnconfigure(0, weight=1)

        self.search_entry = ck.CTkEntry(self.tabview.tab("مبيعات"),placeholder_text="search")
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<KeyRelease>", self.search)
        
        columns = ("id","name","date","total","discount","finalTotal","payed","recive","remain")
        self.table = ttk.Treeview(self.tabview.tab("مبيعات"),columns=columns,height=20, selectmode='browse',show='headings')

        self.table.column("id", anchor="center",width=50,minwidth=50)
        self.table.column("name", anchor="center",width=250,minwidth=250)
        self.table.column("date", anchor="center",width=80, minwidth=80)
        self.table.column("total", anchor="center",width=80, minwidth=80)
        self.table.column("discount", anchor="center",width=80, minwidth=80)
        self.table.column("finalTotal", anchor="center",width=150, minwidth=150)
        self.table.column("payed", anchor="center",width=80, minwidth=80)
        self.table.column("recive", anchor="center",width=80, minwidth=80)
        self.table.column("remain", anchor="center",width=80, minwidth=80)
     
        self.table.heading('id', text='رمز الفاتورة ')
        self.table.heading('name', text='اسم الزبون')
        self.table.heading('date', text='تاريخ الطلبية')
        self.table.heading("total", text='قيمة الفاتورة')
        self.table.heading("discount", text='خصم')
        self.table.heading("finalTotal", text='المجموع')
        self.table.heading("payed", text='الدفع')
        self.table.heading("recive", text='تسليم')
        self.table.heading("remain", text='الدفع المتبقي')

        self.table.bind('<Motion>','break')
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, fieldbackground="Black")
        style.map("Treeview", background=[('selected', '#347083')])
        style.configure("Treeview", highlightthickness=0, bd=0)

        self.table.pack(fill=ck.BOTH, expand=False,padx=15,pady=30)

        button_frame = ck.CTkFrame(self.tabview.tab("مبيعات"),fg_color="transparent")
        button_frame.pack(fill=ck.Y,expand=True,padx=15,pady=45) 

        self.detail_button = ck.CTkButton(button_frame, text="تفاصيل الفاتورة",height=30,command=self.show_detial,font=ck.CTkFont(size=20,weight="bold"))
        self.detail_button.grid(row=0, column=0, padx=10)
        self.detail_button.configure(state="disabled")

        self.printIMG = ck.CTkImage(Image.open("imags/printer.png"),size=(30,30))
        self.print_button = ck.CTkButton(button_frame, text="",image=self.printIMG,compound="left",width=10,fg_color="transparent",command=self.printAssist)
        self.print_button.grid(row=1, column=0,columnspan=2,pady=15)
        self.print_button.configure(state="disabled")

        self.edit_button = ck.CTkButton(button_frame, text="تعديل",font=ck.CTkFont(size=20,weight="bold"),width=10,height=34,command=self.edit_Order)
        self.edit_button.grid(row=0, column=1, padx=10)
        self.edit_button.configure(state="disabled")
  
        self.intTable()

        ###### customers ######

        self.search_entry2 = ck.CTkEntry(self.tabview.tab("زبائن"),placeholder_text="search")
        self.search_entry2.pack(pady=10)
        self.search_entry2.bind("<KeyRelease>", self.search2)
        
        columns2 = ("id","name","phone")
        self.table2 = ttk.Treeview(self.tabview.tab("زبائن"),columns=columns2,height=20, selectmode='browse',show='headings')

        self.table2.column("id", anchor="center",width=50,minwidth=50)
        self.table2.column("name", anchor="center",width=250,minwidth=250)
        self.table2.column("phone", anchor="center",width=80, minwidth=80)
    
        self.table2.heading('id', text='رمز الزبون')
        self.table2.heading('name', text='اسم الزبون')
        self.table2.heading("phone", text='هاتف')

        self.table2.bind('<Motion>','break')
        self.table2.bind("<<TreeviewSelect>>", self.on_item_select2)

        self.table2.pack(fill=ck.BOTH, expand=False,padx=15,pady=30)

        button_frame2 = ck.CTkFrame(self.tabview.tab("زبائن"),fg_color="transparent")
        button_frame2.pack(fill=ck.Y,expand=True,padx=15,pady=45) 

        self.print_button2 = ck.CTkButton(button_frame2, text="كشف حساب",image=self.printIMG,compound="left",font=ck.CTkFont(size=20,weight="bold"),width=10,command=self.customerPrintAssist)
        self.print_button2.grid(row=0, column=2, padx=10)
        self.print_button2.configure(state="disabled")

        self.edit_button2 = ck.CTkButton(button_frame2, text="تعديل الزبون",font=ck.CTkFont(size=20,weight="bold"),width=10,height=38,command=self.edit_Customer)
        self.edit_button2.grid(row=0, column=1, padx=10)
        self.edit_button2.configure(state="disabled")

        # self.delete_button2 = ck.CTkButton(button_frame2, text="حذف",fg_color="red",font=ck.CTkFont(size=20,weight="bold"),width=10,height=30,command=self.printAssist)
        # self.delete_button2.grid(row=0, column=0, padx=10)
        # self.delete_button2.configure(state="disabled")
  
 
        self.intTable2()


    def intTable(self):

        for row in self.table.get_children():
            self.table.delete(row)

        mycursor.execute("SELECT * FROM Orders ORDER BY OrderID DESC")
        mysite = mycursor.fetchall()


        for site in mysite:
            name =self.get_customer_name(site[1])
            status = " كامل" if site[4] == "1" else "ناقص"
            receive = "استلم" if site[5] == 1 else "لم يستلم"
            remain ="-" if (not site[6] or site[6] == 0.00) else site[6]
            site_with_name = (site[0],name, site[2],site[3],site[7],site[8], status, receive,remain)
            self.table.insert('','end',values=(site_with_name))

    def intTable2(self):

        for row in self.table2.get_children():
            self.table2.delete(row)

        sql_query = """
                    SELECT *
                    FROM Customers
                    Order by CustomerID Asc;
                """

        mycursor.execute(sql_query)

        results = mycursor.fetchall()

        for site in results:
            self.table2.insert('','end',values=(site))


    def edit_Customer(self):
         selected_item = self.table2.focus()
         if selected_item:
            self.edit_CustomerW()
         else:  
             mixer.music.load("sounds/error.mp3")
             mixer.music.play()
             messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")

    def edit_CustomerW(self):

        def get(type,text0,window):

            text=self.convert_arabic_to_english2(text0)

            if type == "name":
                if (not text):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE Customers SET CustomerName = %s WHERE CustomerID=%s"
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
            
            elif type == "phone":
                if (not text):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE Customers SET Phone = %s WHERE CustomerID=%s"
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
            nwindow.geometry("450x150")
            nwindow.title('Daftar Application ')

            center_x = int(760)
            center_y = int(300)
            nwindow.geometry(f"+{center_x}+{center_y}")

            label = ck.CTkLabel(nwindow, text=' الهاتف الجديد',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold")) 
            label.pack(pady=5)

            entryN = ck.CTkEntry(nwindow,width=270)
            entryN.pack(padx=10, pady=10)

            entryN.insert(0,self.entry2.get())

            ok_button = ck.CTkButton(nwindow, text="تعديل", command=lambda:get("phone",entryN.get(),nwindow))
            ok_button.pack(padx=10, pady=10)  

            
        new_window = tk.Toplevel(self)
        new_window.geometry("460x400")
        new_window.title('Daftar Application ')

        self.label = ck.CTkLabel(new_window, text='تعديل الزبون',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
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

        label2 = ck.CTkLabel(new_window,width=200,text="الهاتف:",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)
        self.editSellPrice_butt = tk.Button(new_window,image=self.editMG,command=editPhone)
        self.editSellPrice_butt.pack()  

        self.entry2 = ck.CTkEntry(new_window,width=200)
        self.entry2.pack(padx=10, pady=10)
        
        selected_item = self.table2.focus()

        values =  self.table2.item(selected_item, 'values')

        self.entry.delete(0,'end')
        self.entry2.delete(0,'end')
       

        self.entry.insert(0,values[1])
        self.entry2.insert(0,values[2])

        self.entry.configure(state="disabled")
        self.entry2.configure(state="disabled")

    def edit_Order(self):
         selected_item = self.table.focus()
         if selected_item:
            self.edit_OrderW()
         else:  
             mixer.music.load("sounds/error.mp3")
             mixer.music.play()
             messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")

    def edit_OrderW(self):

        def get(type,text0,window):

            text=self.convert_arabic_to_english2(text0)

            if type == "name":
                if (not text):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE Customers SET CustomerName = %s WHERE CustomerID=%s"
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
            
            elif type == "phone":
                if (not text):
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بادخال قيم صحيحة",icon="warning")
                    return
                
                update_query = "UPDATE Customers SET Phone = %s WHERE CustomerID=%s"
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
            nwindow.geometry("450x150")
            nwindow.title('Daftar Application ')

            center_x = int(760)
            center_y = int(300)
            nwindow.geometry(f"+{center_x}+{center_y}")

            label = ck.CTkLabel(nwindow, text=' الهاتف الجديد',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold")) 
            label.pack(pady=5)

            entryN = ck.CTkEntry(nwindow,width=270)
            entryN.pack(padx=10, pady=10)

            entryN.insert(0,self.entry2.get())

            ok_button = ck.CTkButton(nwindow, text="تعديل", command=lambda:get("phone",entryN.get(),nwindow))
            ok_button.pack(padx=10, pady=10)  

            
        new_window = tk.Toplevel(self)
        new_window.geometry("420x360")
        new_window.title('Daftar Application ')

        self.label = ck.CTkLabel(new_window, text='تعديل الفاتورة',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)

        center_x = int(750)
        center_y = int(200)
        new_window.geometry(f"+{center_x}+{center_y}")
       

        label1 = ck.CTkLabel(new_window,width=200,text="دفع كامل:",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)
        
        self.entry = ck.CTkEntry(new_window,width=270)
        self.entry.pack(padx=10, pady=10)

        label2 = ck.CTkLabel(new_window,width=200,text="استلم:",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)

        selected_item = self.table.focus()
        values =  self.table.item(selected_item, 'values')

    

    def get_customer_name(self,customer_id):
        select_customer_query = "SELECT CustomerName FROM Customers WHERE CustomerID = %s"
        mycursor.execute(select_customer_query, (customer_id,))
        result = mycursor.fetchone()
        if result:
            return result[0]
        else:
            return "-"        
        

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
        new_window.geometry("800x600")
        new_window.title('Daftar Application')
        

        center_x = int(550)
        center_y = int(150)
        new_window.geometry(f"+{center_x}+{center_y}")

        label = ck.CTkLabel(new_window,width=200,text="تفاصيل الفاتورة" ,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold"))
        label.pack(pady=10)
       
        
        selected_item = self.table.focus()
        values =  self.table.item(selected_item, 'values')

        columns = ("id","name","date","dis","remain","total")
        table = ttk.Treeview(new_window,columns=columns,height=15, selectmode='browse',show='headings')

        table.column("id", anchor="center",width=70,minwidth=70)
        table.column("name", anchor="center",width=280,minwidth=280)
        table.column("date", anchor="center",width=70, minwidth=70)
        table.column("dis", anchor="center",width=70, minwidth=70)
        table.column("remain", anchor="center",width=90, minwidth=90)
        table.column("total", anchor="center",width=90, minwidth=90)
     
        table.heading('id', text='رمز الصنف')
        table.heading('name', text='اسم الصنف')
        table.heading('date', text='السعر')
        table.heading('dis', text='خصم')
        table.heading("remain", text='كمية')
        table.heading("total", text='مجموع')

        table.bind('<Motion>','break')

        name_var = tk.StringVar()
        name_var.set(values[1]) 

        total_var = tk.StringVar()
        total_var.set(values[3]) 

        date_var = tk.StringVar()
        date_var.set(values[2])  

        discont = tk.StringVar()
        discont.set(values[4])  

        totalAfter = tk.StringVar()
        totalAfter.set(values[5])  
        
        labelFrame =ck.CTkFrame(new_window,fg_color="transparent")
        labelFrame.pack(padx=15,pady=25)

        label1 = ck.CTkLabel(labelFrame,width=200,text="الاسم: " +name_var.get() ,font=ck.CTkFont(size=19,weight="bold"))
        label1.grid(row=0, column=2, padx=10)

        label2 = ck.CTkLabel(labelFrame,width=200,text="قيمة الفاتورة الاصلية: "+total_var.get(),font=ck.CTkFont(size=19,weight="bold"))
        label2.grid(row=0, column=1, padx=10)

        label3 = ck.CTkLabel(labelFrame,width=200,text="تاريخ : "+date_var.get(),font=ck.CTkFont(size=19,weight="bold"))
        label3.grid(row=0, column=0, padx=10)

        label4 = ck.CTkLabel(labelFrame,width=200,text="المجموع: " +totalAfter.get() ,text_color="green",font=ck.CTkFont(size=19,weight="bold"))
        label4.grid(row=1, column=1, padx=10,pady=10)

        label5 = ck.CTkLabel(labelFrame,width=200,text="خصم: "+discont.get(),font=ck.CTkFont(size=19,weight="bold"))
        label5.grid(row=1, column=2, padx=10,pady=10)


        def stat():
                new_window = tk.Toplevel(self)
                new_window.geometry("390x280")
                new_window.title('Daftar Application')
                

                center_x = int(710)
                center_y = int(300)
                new_window.geometry(f"+{center_x}+{center_y}")

                label = ck.CTkLabel(new_window,width=200,text="حسابات خاصة" ,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold"))
                label.pack(pady=10)

                sql_query = """
                   SELECT
                        SUM(od.Subtotal) AS TotalRevenue
                    FROM
                        OrderDetails od
                    JOIN
                        Products p ON od.ProductID = p.ProductID
                    WHERE
                        od.OrderID = %s;

                """

                mycursor.execute(sql_query, (values[0],))
                x1 = mycursor.fetchone()

                sql_query = """
                    SELECT
                        SUM(od.Subtotal - (p.Price * od.Quantity)) AS TotalProfit
                    FROM
                        OrderDetails od
                    JOIN
                        Products p ON od.ProductID = p.ProductID
                    WHERE
                        od.OrderID = %s;
                """

                mycursor.execute(sql_query, (values[0],))
                x3 = mycursor.fetchone()

                sql_query = """
                    SELECT
                        SUM(p.Price * od.Quantity) AS Total
                    FROM
                        OrderDetails od
                    JOIN
                        Products p ON od.ProductID = p.ProductID
                    WHERE
                        od.OrderID = %s;
                """

                mycursor.execute(sql_query, (values[0],))
                x2 = mycursor.fetchone()

                label2 = ck.CTkLabel(new_window,width=200,text=f"مجموع الفاتورة : {float(x1[0])} " ,font=ck.CTkFont(size=17,weight="bold"))
                label2.pack(pady=10)

                label3 = ck.CTkLabel(new_window,width=200,text=f"تكلفة : {float(x2[0])} " ,font=ck.CTkFont(size=17,weight="bold"))
                label3.pack(pady=10)

                label4 = ck.CTkLabel(new_window,width=200,text=f"ربح : {float(x3[0])}" ,font=ck.CTkFont(size=17,weight="bold"))
                label4.pack(pady=10)
        stat_button = ck.CTkButton(labelFrame, text="حسابات",command=stat)
        stat_button.grid(row=2, column=1, padx=10,pady=10)
        

        
        table.pack(pady=20)

        for row in table.get_children():
            table.delete(row)

        sql_query = """
                    SELECT Products.ProductID, Products.ProductName, OrderDetails.ProductPrice,OrderDetails.discount,OrderDetails.Quantity,OrderDetails.Subtotal
                    FROM Orders
                    JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
                    JOIN Products ON OrderDetails.ProductID = Products.ProductID
                    WHERE Orders.OrderID = %s;
                """

        mycursor.execute(sql_query, (values[0],))

        results = mycursor.fetchall()

        for site in results:
            table.insert('','end',values=(site))


    def on_item_select(self,event):
        selected_item = self.table.focus()
        if selected_item:
                self.detail_button.configure(state="normal")
                self.print_button.configure(state="normal")
                self.edit_button.configure(state="normal")
        else :
                self.print_button.configure(state="disabled")  
                self.detail_button.configure(state="disabled")
                self.edit_button.configure(state="disabled")

    def on_item_select2(self,event):
        selected_item = self.table2.focus()
        if selected_item:
                self.print_button2.configure(state="normal")
                self.edit_button2.configure(state="normal")
        else :
                self.print_button2.configure(state="disabled")    
                self.edit_button2.configure(state="disabled")    


    def printAssist(self):
         selected_item = self.table.focus()
         if selected_item:

            values = self.table.item(selected_item, "values")

            sql_query = """
                    SELECT Products.ProductID,Products.ProductName, OrderDetails.ProductPrice ,OrderDetails.discount,OrderDetails.Quantity,Products.Unit , OrderDetails.Subtotal, remainAmount, TotalAmount
                    FROM Orders
                    JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
                    JOIN Products ON OrderDetails.ProductID = Products.ProductID
                    WHERE Orders.OrderID = %s;
                """

            mycursor.execute(sql_query, (values[0],))

            results = mycursor.fetchall()


            table_data = [['رمز الصنف','اسم الصنف', 'السعر','خصم', 'الكمية','وحدة', 'المجموع']]

            for row in results:
                table_row = [row[0], row[1], row[2], row[3],row[4],row[5],row[6]]
                table_data.append(table_row)

            sql_query = """
                    SELECT Orders.discount
                    FROM Orders
                    WHERE Orders.OrderID = %s;
                """

            mycursor.execute(sql_query, (values[0],))

            results2 = mycursor.fetchone()
    
            self.Xprint(table_data,values[1],values[3],values[0],results2[0],f"{values[0]}.pdf")
         
         else:  
             mixer.music.load("sounds/error.mp3")
             mixer.music.play()
             messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")

    def Xprint(self,schedule_data,name,total,id,discount,output_filename):
        pdf = SimpleDocTemplate(output_filename, pagesize=letter)
        pdfmetrics.registerFont(TTFont('Arabic', 'arfonts-traditional-arabic-bold/traditional-arabic-bold.ttf'))
        
        company_info = {
        'name': 'المخماسي لمواد البناء والادوات الصحية',
        'telephone': '0598-508615',
        'address': 'مخماس - الشارع الرئيسي'
        }
        
        # text = company_info['name']
        # reshaped_text = arabic_reshaper.reshape(text)
        # bidi_text1 = get_display(reshaped_text)

        # text = company_info['telephone']
        # reshaped_text = arabic_reshaper.reshape(text)
        # bidi_text2 = get_display(reshaped_text)

        # text = company_info['address']
        # reshaped_text = arabic_reshaper.reshape(text)
        # bidi_text3 = get_display(reshaped_text)


        # pdf_canvas.setFont("Arabic", 20)

        # middle_x = letter[0] / 2
        # company_name_x = middle_x-21 - pdf_canvas.stringWidth(bidi_text1, "Arabic", 14) / 2


        # pdf_canvas.drawString(company_name_x, 750, bidi_text1)

        pdf_canvas = canvas.Canvas(output_filename, pagesize=letter)
        pdf_canvas.setFont("Arabic", 12)

        # pdf_canvas.drawString(30, 730, f"{bidi_text2}")

        # address_width = pdf_canvas.stringWidth(bidi_text3, "Arabic", 12)
        # pdf_canvas.drawString(letter[0] - address_width - 30, 730, bidi_text3)

        # line_start = 30
        # line_end = letter[0] - 30
        # pdf_canvas.line(line_start, 700, line_end, 700)




        title = "مبيعات"
        pdf_canvas.setFont("Arabic", 27)
        reshaped_text = arabic_reshaper.reshape(title)
        bidi_text4 = get_display(reshaped_text)
        title_width = pdf_canvas.stringWidth(bidi_text4, "Arabic", 19)
        title_x = (letter[0] - title_width) / 2
        pdf_canvas.drawString(title_x, 700, bidi_text4)



        current_date = datetime.now().strftime("%Y-%m-%d")
        current_date2 = datetime.now().strftime("%I:%M")

        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f"{current_date} ")
        bidi_text5 = get_display(reshaped_text)

        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f"{current_date2} ")
        bidi_text55 = get_display(reshaped_text)

        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f"{name}")
        bidi_text8 = get_display(reshaped_text)

        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f" سند رقم: {id}")
        bidi_text88 = get_display(reshaped_text)


        pdf_canvas.drawString(50, 630, bidi_text5)
        pdf_canvas.drawString(65, 610, bidi_text55)
        pdf_canvas.drawString(495, 630, bidi_text8)
        pdf_canvas.drawString(495, 605, bidi_text88)
                
        cell_height = 20

        x_start = 70
        y_start = 540

        pdf_canvas.setFont("Arabic", 12)

        def draw_table_row(row, y):
            pdf_canvas.setFont("Arabic", 12)

            cell_width = 60
            x = x_start + 0 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[0])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 10, y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

            cell_width = 170
            x = x_start + 2.83 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[1])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(211 - pdf_canvas.stringWidth(bidi_text, "Arabic", 12) / 2 , y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(130, y + 21, 130 + cell_width, y + 21)
            pdf_canvas.rect(130, y + 21, cell_width, -cell_height, stroke=1, fill=0)

            cell_width = 60
            x = x_start + 3.83 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[2])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 10, y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

            # cell_width = 60
            # x = x_start + 4.83 * cell_width
            # reshaped_text = arabic_reshaper.reshape(f"{str(row[3])} ")
            # bidi_text = get_display(reshaped_text)
            # pdf_canvas.drawString(x + 10, y + 5, bidi_text)
            # pdf_canvas.setStrokeColor(colors.blue)
            # pdf_canvas.setLineWidth(1)
            # pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            # pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

            cell_width = 60
            x = x_start + 4.83 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[4])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 10, y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)
            
            cell_width = 60
            x = x_start + 5.83 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[5])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 10, y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

            cell_width = 60
            x = x_start + 6.83 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[6])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 7, y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)


        y_prime=0
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
            y_prime=y    

        # label = "خصم :"
        # pdf_canvas.setFont("Arabic", 11)
        # reshaped_text = arabic_reshaper.reshape(f"{label} ")
        # bidi_text6 = get_display(reshaped_text)
        # label_width = pdf_canvas.stringWidth(bidi_text6, "Arabic", 19)
        # label_width = (letter[0] - label_width) / 2

        # pdf_canvas.drawString(label_width+15, y_prime-70, f"{discount} {bidi_text6} ")

        label = "المبلغ الاجمالي بالشيكل :"
        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f"{label} ")
        bidi_text6 = get_display(reshaped_text)
        label_width = pdf_canvas.stringWidth(bidi_text6, "Arabic", 19)
        label_width = (letter[0] - label_width) / 2

        pdf_canvas.drawString(label_width+7, y_prime-100, f"{total} {bidi_text6} ")

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

    def customerPrintAssist(self):
         selected_item = self.table2.focus()
         if selected_item:

            values = self.table2.item(selected_item, "values")

            sql_query = """
                WITH TransactionData AS (
                    SELECT 'Order' AS Type,
                        OrderID AS TransactionID,
                        OrderDate AS TransactionDate,
                        TotalAmount AS OrderAmount,
                        NULL AS PaymentAmount
                    FROM Orders
                    WHERE CustomerID = %s

                    UNION

                    SELECT 'Payment' AS Type,
                        paymentId AS TransactionID,
                        paymentDate AS TransactionDate,
                        NULL AS OrderAmount,
                        Amount AS PaymentAmount
                    FROM Payments
                    WHERE OrderID IN (SELECT OrderID FROM Orders WHERE CustomerID = %s)
                )

                SELECT
                    
                    TransactionDate,
                    Type,
                    TransactionID,
                    OrderAmount,
                    PaymentAmount,

                    SUM(COALESCE(OrderAmount, 0) - COALESCE(PaymentAmount, 0)) OVER (ORDER BY TransactionDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS DynamicTotal
                FROM TransactionData
                ORDER BY TransactionDate;
                                """

            mycursor.execute(sql_query, (values[0],values[0]))

            results = mycursor.fetchall()


            table_data = [['التاريخ','بيان', 'مدين','دائن', 'اجمالي']]

            for row in results:
                if row[1] =='Order':
                    table_row = [row[0], f"مشتريات فاتورة رقم- {row[2]} ", "-" if row[3] is None else  row[3] ,"-" if row[4] is None else  row[4],row[5]]
                    table_data.append(table_row)
                elif row[1] =='Payment':
                    table_row = [row[0], f"استلام نقدي سند قبض رقم- {row[2]} ",  "-" if row[3] is None else  row[3] ,"-" if row[4] is None else  row[4],row[5]]
                    table_data.append(table_row)

    
            self.customerXprint(table_data,values[1],f"{values[0]}Account.pdf")
         
         else:  
             mixer.music.load("sounds/error.mp3")
             mixer.music.play()
             messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")


    def customerXprint(self,schedule_data,name,output_filename):
        pdf = SimpleDocTemplate(output_filename, pagesize=letter)
        pdfmetrics.registerFont(TTFont('Arabic', 'arfonts-traditional-arabic-bold/traditional-arabic-bold.ttf'))
        
        company_info = {
        'name': 'المخماسي لمواد البناء والادوات الصحية',
        'telephone': '0598-508615',
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

        title = "كشف حساب"
        pdf_canvas.setFont("Arabic", 27)
        reshaped_text = arabic_reshaper.reshape(title)
        bidi_text4 = get_display(reshaped_text)
        title_width = pdf_canvas.stringWidth(bidi_text4, "Arabic", 19)
        title_x = (letter[0] - title_width) / 2
        pdf_canvas.drawString(title_x, 670, bidi_text4)



        current_date = datetime.now().strftime("%Y-%m-%d")
        current_date2 = datetime.now().strftime("%I:%M")

        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f"{current_date} ")
        bidi_text5 = get_display(reshaped_text)

        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f"{current_date2} ")
        bidi_text55 = get_display(reshaped_text)

        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f"{name}")
        bidi_text8 = get_display(reshaped_text)


        pdf_canvas.drawString(50, 630, bidi_text5)
        pdf_canvas.drawString(65, 610, bidi_text55)
        pdf_canvas.drawString(495, 630, bidi_text8)
                
        cell_height = 20

        x_start = 100
        y_start = 540

        pdf_canvas.setFont("Arabic", 12)

        def draw_table_row(row, y):
            pdf_canvas.setFont("Arabic", 12)

            cell_width = 100
            x = x_start + 0 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[0])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 10, y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

            cell_width = 170
            x = x_start + 4.83 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[1])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(282 - pdf_canvas.stringWidth(bidi_text, "Arabic", 12) / 2 , y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(200, y + 21, 130 + cell_width, y + 21)
            pdf_canvas.rect(200, y + 21, cell_width, -cell_height, stroke=1, fill=0)

            cell_width = 60
            x = x_start + 4.50 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[2])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 17, y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)


            cell_width = 60
            x = x_start + 5.50 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[3])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 17, y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)
            
            cell_width = 60
            x = x_start + 6.50 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[4])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 17, y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)
          

        y_prime=0
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
            y_prime=y    

      

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

    def search(self, event):
        search_query = self.search_entry.get().lower()

        self.table.delete(*self.table.get_children())

        if search_query:
            sql = f"SELECT * FROM Orders WHERE LOWER(OrderID) LIKE '%{search_query}%'"
            mycursor.execute(sql)
            matching_products = mycursor.fetchall()

            for product in matching_products:
                self.table.insert("", "end", values=product)

        else:self.intTable()

    def search2(self, event):
        search_query2 = self.search_entry2.get().lower()

        self.table2.delete(*self.table2.get_children())

        if search_query2:
            sql = f"SELECT * FROM Customers WHERE LOWER(CustomerName) LIKE '%{search_query2}%'"
            mycursor.execute(sql)
            matching_products = mycursor.fetchall()

            for product in matching_products:
                self.table2.insert("", "end", values=product)

        else:self.intTable2()

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

