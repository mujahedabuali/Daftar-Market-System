
import customtkinter as ck
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from pygame import mixer
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector
from db import mycursor,mydb

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from datetime import datetime

import webbrowser
import os
import sys
import subprocess
import webbrowser



class page4(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.bookmark_image = ck.CTkImage(Image.open("imags/cash.png"),size=(40,40))
        self.label = ck.CTkLabel(self, text="البيع ",image=self.bookmark_image,corner_radius=20,compound="right",height=50,font=ck.CTkFont(size=30,weight="bold")) 
        self.label.grid(row=0, column=0, columnspan=2,sticky="nsew")
    

        left_frame = ck.CTkFrame(self,fg_color="transparent")
        left_frame.grid(row=1, column=0, sticky="nsew")
        right_frame = ck.CTkFrame(self,fg_color="transparent")
        right_frame.grid(row=1, column=1, sticky="nsew")

        self.totalPrice=ck.StringVar()
        self.totalPrice.set("المجموع : 0.00")
        self.Origin_price_variabled=0.00

        self.discontLabl="%0.00"
        self.AfterDiscountVar=self.Origin_price_variabled

        self.AfterDiscount=ck.StringVar()
        self.AfterDiscount.set("المجموع : {:.2f}".format(float(self.AfterDiscountVar)))


        mixer.init()

        ##########left table###############
        columns = ('id','name','price','cont','unit','discont','total_price')
        self.table = ttk.Treeview(left_frame ,columns=columns,height=14,selectmode='browse',show='headings')

        self.table.column("id", anchor="c", minwidth=60, width=60)
        self.table.column("name", anchor="c", minwidth=220, width=220)
        self.table.column("price", anchor="c", minwidth=70, width=70)
        self.table.column("cont", anchor="c", minwidth=80, width=80)
        self.table.column("unit", anchor="c", minwidth=80, width=80)
        self.table.column("discont", anchor="c", minwidth=90, width=90)
        self.table.column("total_price", anchor="c", minwidth=110, width=110)
        

        self.table.heading('id', text='الرمز')
        self.table.heading('name', text='العنصر')
        self.table.heading('price', text='السعر')
        self.table.heading('cont', text='كمية')
        self.table.heading('unit', text='وحدة')
        self.table.heading('discont', text='خصم')
        self.table.heading('total_price', text='مجموع')
        

        self.table.bind('<Motion>', 'break')

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

        
        self.table.pack(padx=30,pady=100)

        button_frame = ck.CTkFrame(left_frame,fg_color="transparent")
        button_frame.pack(expand=False,padx=15,pady=0)

        self.edit_button = ck.CTkButton(button_frame, text="تعديل",height=30,command=self.edit_item,font=ck.CTkFont(size=20,weight="bold"))
        self.edit_button.grid(row=0, column=1, padx=10)

        self.delete_button = ck.CTkButton(button_frame, text="حذف",height=30,fg_color="red", command=self.delete_item,font=ck.CTkFont(size=20,weight="bold"))
        self.delete_button.grid(row=0, column=2, padx=10)

        total_frame = ck.CTkFrame(left_frame,fg_color="transparent")
        total_frame.pack(pady=20)
        self.total = ck.CTkLabel(total_frame,textvariable=self.totalPrice,text_color="green",corner_radius=20,height=30,font=ck.CTkFont(size=25,weight="bold"))
        self.total.grid(row=0, column=1, padx=10,pady=10)

        self.done_button = ck.CTkButton(total_frame, text="بيع",height=30,fg_color="green", command=self.buy,font=ck.CTkFont(size=20,weight="bold"))
        self.done_button.grid(row=2, column=1, padx=10,columnspan=2,pady=25)
        self.done_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")
        self.edit_button.configure(state="disabled")
        

        ####### Right table #############
        columns2 = ('id','name','price','unit')
        self.table2 = ttk.Treeview(right_frame,columns=columns2,height=14,selectmode='browse',show='headings')

        self.table2.column("id", anchor="c", minwidth=60, width=60)
        self.table2.column("name", anchor="c", minwidth=255, width=255)
        self.table2.column("price", anchor="c", minwidth=65, width=65)
        self.table2.column("unit", anchor="c", minwidth=45, width=45)
        
        self.table2.heading('id', text='الرمز')
        self.table2.heading('name', text='العنصر')
        self.table2.heading('price', text='السعر')
        self.table2.heading('unit', text='وحدة')

        self.table2.bind('<Motion>', 'break')
        self.table.bind("<<TreeviewSelect>>", self.on_item_select2)

        search_frame= ck.CTkFrame(right_frame,fg_color="transparent")
        search_frame.pack(fill=ck.Y,expand=False,padx=10,pady=20)

        self.search_entry = ck.CTkEntry(search_frame,placeholder_text="search")
        self.search_entry.grid(row=0, column=0)
        self.search_entry.bind("<KeyRelease>", self.search)

        self.search_entry2 = ck.CTkEntry(search_frame,placeholder_text="search by id",width=90)
        self.search_entry2.grid(row=0, column=2,padx=10)
        self.search_entry2.bind("<KeyRelease>", self.searchByID)

        self.table2.pack(fill=ck.Y,expand=False,padx=10,pady=33)

        add_frame = ck.CTkFrame(right_frame,fg_color="transparent")
        add_frame.pack(fill=ck.Y,expand=False,padx=15,pady=15)

        self.nameAdded = ck.CTkLabel(add_frame,text="",text_color="#2e8fe7",corner_radius=20,height=20,font=ck.CTkFont(size=16,weight="bold"))
        self.nameAdded.grid(row=0, column=0, padx=10,pady=10)

        self.table2.bind("<<TreeviewSelect>>", self.on_item_select_and_update_name_added)

        self.add_button = ck.CTkButton(add_frame, text="إضافة",height=30,command=self.add_data,font=ck.CTkFont(size=20,weight="bold"))
        self.add_button.configure(state="disabled")
        self.add_button.grid(row=2, column=0, padx=10)

        self.cont_entry = ck.CTkEntry(add_frame)
        self.cont_entry.grid(row=1, column=0, padx=10,pady=10)
        self.cont_entry.insert(0, "1")
        
        self.intTable2()
      

    def intTable2(self):

        for row in self.table2.get_children():
            self.table2.delete(row)

        mycursor.execute("SELECT ProductID,ProductName,sell_Price,Unit FROM Products WHERE StockQuantity > 0 ORDER BY ProductID desc")
        mysite = mycursor.fetchall()
        for site in mysite:
            self.table2.insert('','end',values=(site))
    
    def on_item_select_and_update_name_added(self, event):
        self.on_item_select(event)
        self.update_nameAdded(event)

    def update_nameAdded(self, event):
        selected_item = self.table2.selection()
        if selected_item:
            name = self.table2.item(selected_item, "values")[1]
            self.nameAdded.configure(text=f"{name}")
        else:
             self.nameAdded.configure(text="")

   
    def add_data(self):
        selected_item = self.table2.focus()
        
        if selected_item:
            if (not self.is_valid_entry(self.cont_entry.get())):
                self.cont_entry.delete(0,'end')
                self.cont_entry.insert(0, "1")
            
            else:
                    values =  self.table2.item(selected_item, 'values')
                    
                    if not self.table.exists(values[0]):
                        if not self.is_exists(float(self.cont_entry.get())):
                            mixer.music.load("sounds/error.mp3")
                            mixer.music.play()
                            messagebox.showwarning("Warning Message","غير موجود في المخزن!",icon="warning")
                            self.cont_entry.delete(0,'end')
                            self.cont_entry.insert(0, "1")

                        else: 
                            self.table.insert('','end',iid=values[0],values=(values[0],values[1],values[2],self.cont_entry.get(),values[3],"-",float(values[2])*float(self.cont_entry.get())))
                            self.update_total("")
                            self.buyBttonState("xx")
                            mixer.music.load("sounds/done.wav")
                            mixer.music.play()
                    else:
                          for item_id in self.table.get_children():
                            x = self.table.item(item_id, 'values')
    
                            if x[0] == values[0]:
                                new_quantity = float(x[3]) + float(self.cont_entry.get()) 

                                if not self.is_exists(new_quantity):
                                    mixer.music.load("sounds/error.mp3")
                                    mixer.music.play()
                                    messagebox.showwarning("Warning Message","غير موجود في المخزن!",icon="warning")
                                    self.cont_entry.delete(0,'end')
                                    self.cont_entry.insert(0, "1")

                                else: 
                                    new_subtotal = float((x[6])) + (float(values[2])*float(self.cont_entry.get()))
                                    self.table.set(item_id, column='cont', value=new_quantity)
                                    self.table.set(item_id, column='total_price', value=new_subtotal)
                                    self.update_total("")
                                    self.buyBttonState("xx")
                                    mixer.music.load("sounds/done.wav")
                                    mixer.music.play()
                                break  
                            
                    self.cont_entry.delete(0,'end')
                    self.cont_entry.insert(0, "1")
                    

        else:
             mixer.music.load("sounds/error.mp3")
             mixer.music.play()
             messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")


    def edit_item(self):
         selected_item = self.table.focus()
         if selected_item:
            self.edit_window()
         else:  
             mixer.init()
             mixer.music.load("sounds/error.mp3")
             mixer.music.play()
             messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")

    def edit_window(self):
        def get():
            list =[self.entry3,self.entry4]
            entry_texts = [entry.get() for entry in list]
            if any(not text for text in entry_texts):
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","قم بادخال جميع الحقول",icon="warning")
            
            else:
                    self.is_valid_entry(self.entry3.get())
                    self.convert_arabic_to_english(self.entry3)

                    self.is_valid_entry(self.entry4.get())
                    self.convert_arabic_to_english(self.entry4)

                    if not self.is_exists(float(self.entry3.get())): 
                        mixer.music.load("sounds/error.mp3")
                        mixer.music.play()
                        messagebox.showwarning("Warning Message","غير موجود في المخزن!",icon="warning")
                        self.entry3.delete(0,'end')
                        self.entry3.insert(0, "1")
                        return
                    
                    else:
                        selected_item = self.table.selection()

                        index = self.table.index(selected_item[0])
                        item_id = self.table.get_children()[index]

                        x=self.table.item(item_id, "values")

                        new_cont = self.entry3.get()
                        new_total = float(new_cont)*float(x[2])
                        disPers=x[5]
                        
                        if float(self.entry4.get())>=0 and float(self.entry4.get())<=float(values[2]):
                            newPriceX=values[2]
                            newPriceX=float(newPriceX)-float(self.entry4.get())
                            discounted_percentage_of_original =100-((newPriceX / float(values[2])) * 100)
                            disPers=f"% {discounted_percentage_of_original:0.2f}"

                            new_total=float(newPriceX)* float(new_cont)
                        
                            selected_item = self.table.selection()
                            index = self.table.index(selected_item[0])
                            item_id = self.table.get_children()[index]

                            self.table.set(item_id, column='total_price', value=newPriceX)
                            self.table.set(item_id, column='discont', value=disPers)
                        else:
                            mixer.music.load("sounds/error.mp3")
                            mixer.music.play()
                            messagebox.showwarning("Warning Message","ادخال خاطئ",icon="warning")
                            return

                        if self.entry4.get() == "0":
                            self.table.item(item_id, values=(x[0], x[1],x[2], new_cont,x[4],"-",new_total))
                        else:
                            self.table.item(item_id, values=(x[0], x[1],x[2], new_cont,x[4],disPers,new_total))
                        self.update_total("")
                        mixer.music.load("sounds/done.wav")
                        mixer.music.play()
                        new_window.destroy()

        new_window = tk.Toplevel(self)
        new_window.geometry("400x400")
        new_window.title('Daftar Application')

        self.label = ck.CTkLabel(new_window, text='تعديل ',corner_radius=20,height=50,text_color="#2e8fe7",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)

        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        selected_item = self.table.focus()
        values =  self.table.item(selected_item, 'values')

        name_var = tk.StringVar()
        name_var.set(values[1])   

        label1 = ck.CTkLabel(new_window,width=200,text="" +name_var.get(),text_color="#2e8fe7",font=ck.CTkFont(size=19,weight="bold"))
        label1.pack(pady=15)

        label3 = ck.CTkLabel(new_window,width=200,text="الكمية:",font=ck.CTkFont(size=21,weight="bold"))
        label3.pack(padx=10, pady=10)

        self.entry3 = ck.CTkEntry(new_window,width=200)
        self.entry3.pack(padx=10, pady=10)

        label4 = ck.CTkLabel(new_window,width=200,text="خصم:",font=ck.CTkFont(size=21,weight="bold"))
        label4.pack(padx=10, pady=10)

        self.entry4 = ck.CTkEntry(new_window,width=200)
        self.entry4.pack(padx=10, pady=10)

        self.entry3.delete(0,'end')
        self.entry3.insert(0,values[3])

        self.entry4.delete(0,'end')
        if values[5] =="-":
            self.entry4.insert(0,0)
        else: self.entry4.insert(0,values[5])

        ok_button = ck.CTkButton(new_window, text="تعديل", command=get)
        ok_button.pack(padx=10, pady=10)   

    def delete_item(self):
         selected_item = self.table.focus()
         if selected_item:
            values = self.table.item(selected_item, "values")
            mixer.init()
            mixer.music.load("sounds/warning.wav")
            mixer.music.play()
            sure = messagebox.askyesno("Confirmation", f"متأكد ؟ \n حذف {values[0]}",icon="warning")
            if sure :
                self.table.delete(selected_item)
            
                self.update_total("")
                mixer.music.load("sounds/done.wav")
                mixer.music.play()
               
         else: 
            mixer.music.load("sounds/error.mp3")
            mixer.music.play()
            messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")
         
    def on_item_select(self,event):
        selected_item = self.table2.focus()
        if selected_item:
                self.add_button.configure(state="normal")
        else :self.add_button.configure(state="disabled")

    def on_item_select2(self,event):
        selected_item = self.table.focus()
        if selected_item:
                self.delete_button.configure(state="normal")
                self.edit_button.configure(state="normal")
        else :
                self.delete_button.configure(state="disabled")
                self.edit_button.configure(state="disabled")

    def buyBttonState(self,event):
         if self.table.get_children():
            self.done_button.configure(state="normal")
         else:
             self.done_button.configure(state="disabled")
         
    
    def update_total(self,event):

        total_price = 0.0
        for item_id in self.table.get_children():
            values = self.table.item(item_id, "values")
            total_price += float(values[6])

        self.Origin_price_variabled=total_price
        self.AfterDiscountVar=self.Origin_price_variabled
        self.totalPrice.set("المجموع : {:.2f}".format(float(self.Origin_price_variabled)))


    def is_exists(self,cont):
    
        selected_item = self.table2.focus()
        values =  self.table2.item(selected_item, 'values')
        select_query = "SELECT StockQuantity FROM Products WHERE ProductID = %s"
    
        try:
            mycursor.execute(select_query, (values[0],))
            result = mycursor.fetchone()
            
            if result and result[0] >= int(cont):
             return True
            return False

        
        except mysql.connector.Error as err:
            messagebox.showwarning("Warning Message","حركة خاطئة",icon="warning")
            return False
        

    def buy(self):
        
        def get_order_details_from_tree():
            order_details_data = []

            for child_id in self.table.get_children():
                values = self.table.item(child_id, 'values')
                order_details_data.append(tuple(values))

            return order_details_data  
                
        def full_pay():

            sure = messagebox.askyesno("Confirmation", "تاكيد ؟ ",icon="warning")
            if sure : 
                
                if not self.Name_entry.get() :
                    insert_order_query = "INSERT INTO Orders (OrderDate, TotalAmount, Status,receive,AfterDiscount,remainAmount,discount) VALUES (%s, %s, %s,%s,%s,%s,%s)"
                    order_data = (datetime.now(), self.Origin_price_variabled, '1',checkbox_var.get(),self.AfterDiscountVar,0.00,self.discontLabl)
                    mycursor.execute(insert_order_query, order_data)
                    mydb.commit()
                    
                    order_id = mycursor.lastrowid
                    order_details_data = get_order_details_from_tree()


                    insert_payments_query = "INSERT INTO payments (paymentDate, OrderID, Amount) VALUES (%s,%s,%s)"
                    payments_data = (datetime.now(),order_id,self.AfterDiscountVar)
                    mycursor.execute(insert_payments_query, payments_data)
                    mydb.commit()
                    
                    insert_order_details_query = "INSERT INTO OrderDetails (OrderID, ProductID, Quantity, Subtotal,discount,ProductPrice) VALUES (%s,%s, %s, %s, %s,%s)"

                    detials_data=[]
                    for x in order_details_data:
                        if (x[0]) is not None:
                            detials_data.append((order_id, (x[0]),x[3],x[6],x[5],x[2])) 
                    
                    
                    mycursor.executemany(insert_order_details_query,detials_data)
                    mydb.commit()

                    update_product_quantity_query = "UPDATE Products SET StockQuantity = StockQuantity - %s WHERE ProductID = %s"
                    for xx in detials_data:
                        mycursor.execute(update_product_quantity_query, (xx[2], xx[1]))

                    mydb.commit()

                    Xprint = messagebox.askyesno("Confirmation", "طباعة الفاتورة ؟ ",icon="info")
                    if Xprint : self.printAssist(order_id)
                    
                    mixer.music.load("sounds/done.wav")
                    mixer.music.play()
                    new_window.destroy()

                else :
                            if self.existCustom ==True:
                                customer_id = self.ExistCustomerID
                            else:    
                                insert_customer_query = "INSERT INTO Customers (CustomerName) VALUES (%s)"
                                mycursor.execute(insert_customer_query, (self.Name_entry.get(),))
                                mydb.commit()
                                customer_id = mycursor.lastrowid
                


                            insert_order_query = "INSERT INTO Orders (OrderDate,CustomerID,TotalAmount, Status,receive,AfterDiscount,remainAmount,discount) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)"
                            order_data = (datetime.now(),customer_id,self.Origin_price_variabled, '1',checkbox_var.get(),self.AfterDiscountVar,0.00,self.discontLabl)
                            mycursor.execute(insert_order_query, order_data)
                            mydb.commit()
                
                            
                            order_id = mycursor.lastrowid
                            order_details_data = get_order_details_from_tree()

                            insert_payments_query = "INSERT INTO payments (paymentDate, OrderID, Amount) VALUES (%s,%s,%s)"
                            payments_data = (datetime.now(),order_id,self.AfterDiscountVar)
                            mycursor.execute(insert_payments_query, payments_data)
                            mydb.commit()                            

                            insert_order_details_query = "INSERT INTO OrderDetails (OrderID, ProductID, Quantity, Subtotal,discount,ProductPrice) VALUES (%s,%s, %s, %s, %s,%s)"

                            detials_data=[]
                            for x in order_details_data:
                                if (x[0]) is not None:
                                     x3=self.convert_arabic_to_englishText(x[3])    
                                     x5=self.convert_arabic_to_englishText(x[5]) 
                                     detials_data.append((order_id, (x[0]),x3,x[6],x5,x[2])) 
                        
                            mycursor.executemany(insert_order_details_query,detials_data)
                            mydb.commit()

                            update_product_quantity_query = "UPDATE Products SET StockQuantity = StockQuantity - %s WHERE ProductID = %s"
                            for xx in detials_data:
                                 mycursor.execute(update_product_quantity_query, (xx[2], xx[1]))

                            mydb.commit()

                            
                            Xprint = messagebox.askyesno("Confirmation", "طباعة الفاتورة ؟ ",icon="info")
                            if Xprint : self.printAssist(order_id)

                            mixer.music.load("sounds/done.wav")
                            mixer.music.play()
                            new_window.destroy()
   
        def part_done():
            sure = messagebox.askyesno("Confirmation", "تاكيد ؟ ",icon="warning")
            if sure :
                if not self.Name_entry.get() :
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play()
                    messagebox.showwarning("Warning Message","قم بإدخال اسم الزبون",icon="warning")
                    return

                elif not payValue_entry.get() or float(payValue_entry.get())>self.AfterDiscountVar :
                    mixer.music.load("sounds/error.mp3")
                    mixer.music.play() 
                    messagebox.showwarning("Warning Message","قم بإدخال قيمة الدفع ",icon="warning")
                    return

                

                if self.existCustom ==True:
                    customer_id = self.ExistCustomerID
                else:    
                    insert_customer_query = "INSERT INTO Customers (CustomerName,Phone) VALUES (%s,%s)"
                    mycursor.execute(insert_customer_query, (self.Name_entry.get(), self.phone_entry.get()))
                    mydb.commit()
                    customer_id = mycursor.lastrowid

                insert_order_query = "INSERT INTO Orders (OrderDate,CustomerID,TotalAmount,remainAmount, Status,receive,discount,AfterDiscount) VALUES (%s,%s,%s,%s,%s, %s, %s,%s)"
                order_data = (datetime.now(),customer_id,self.Origin_price_variabled,(float(self.AfterDiscountVar)-float(payValue_entry.get())), '0',checkbox_var.get(),self.discontLabl,self.AfterDiscountVar)
                mycursor.execute(insert_order_query, order_data)
                mydb.commit()
        
                
                order_id = mycursor.lastrowid
                order_details_data = get_order_details_from_tree()
                if float(payValue_entry.get())>0:
                    insert_order_query = "INSERT INTO payments (paymentDate, OrderID, Amount) VALUES (%s,%s,%s)"
                    order_data = (datetime.now(),order_id,float(payValue_entry.get()))
                    mycursor.execute(insert_order_query, order_data)
                    mydb.commit()

                
                
                insert_order_details_query = "INSERT INTO OrderDetails (OrderID, ProductID, Quantity, Subtotal,discount,ProductPrice) VALUES (%s,%s, %s, %s, %s,%s)"

                detials_data=[]
                for x in order_details_data:
                    if (x[0]) is not None:
                        x3=self.convert_arabic_to_englishText(x[3])    
                        x5=self.convert_arabic_to_englishText(x[5]) 
                        detials_data.append((order_id, (x[0]),x3,x[6],x5,x[2]))
                
                
                mycursor.executemany(insert_order_details_query,detials_data)
                mydb.commit()

                update_product_quantity_query = "UPDATE Products SET StockQuantity = StockQuantity - %s WHERE ProductID = %s"
                for xx in detials_data:
                        mycursor.execute(update_product_quantity_query, (xx[2], xx[1]))

                mydb.commit()

                print = messagebox.askyesno("Confirmation", "طباعة الفاتورة ؟ ",icon="info")
                if print : self.printAssist(order_id)

                mixer.music.load("sounds/done.wav")
                mixer.music.play()
                new_window.destroy()

        new_window = tk.Toplevel(self)
        new_window.geometry("500x615")
        new_window.title('Daftar Application')

        center_x = int(730)
        center_y = int(250)
        new_window.geometry(f"+{center_x}+{center_y}")

        total_frame= ck.CTkFrame(new_window,fg_color="transparent")
        total_frame.pack(fill=ck.Y,expand=False,pady=30)

        total = ck.CTkLabel(total_frame,textvariable=self.totalPrice,text=f"{self.totalPrice.get()}",text_color="green",corner_radius=20,height=30,font=ck.CTkFont(size=25,weight="bold"))
        total.grid(row=0, column=0)  

        self.AfterDisocuntLabl = ck.CTkLabel(total_frame,textvariable=self.AfterDiscount,text=f"{self.AfterDiscount.get()}",corner_radius=20,height=30,font=ck.CTkFont(size=19,weight="bold"))

        original_image = Image.open("imags/edit.png")
        self.editMG = original_image.resize((15, 15))
        self.editMG = ImageTk.PhotoImage(self.editMG)

        self.edit_butt = tk.Button(total_frame,image=self.editMG,command=self.editShow)
        self.edit_butt.grid(row=0, column=1)  

        self.discount_frame= ck.CTkFrame(total_frame,fg_color="transparent")

        self.discontLbl=ck.CTkLabel(self.discount_frame,text=f"خصم: ",text_color="#2e8fe7",corner_radius=20,height=30,font=ck.CTkFont(size=16,weight="bold"))
        self.edit_entry =ck.CTkEntry(self.discount_frame,width=100,height=10)
        self.edit_entry.bind("<Return>", self.editTotal)

        self.discontLbl.grid(row=1, column=3)
        self.edit_entry.grid(row=1, column=2)

        self.radio_var = tk.IntVar(value=0)
        self.radio_button_1 = ck.CTkRadioButton(master=self.discount_frame,text="%",variable=self.radio_var, value=1)
        self.radio_button_1.grid(row=1, column=0)
        self.radio_button_2 = ck.CTkRadioButton(master=self.discount_frame,text="شيكل", variable=self.radio_var, value=0)
        self.radio_button_2.grid(row=1, column=1)

        checkbox_var = tk.IntVar()
        recive = ck.CTkCheckBox(new_window,text="استلم",text_color="#2e8fe7",font=ck.CTkFont(size=21,weight="bold"),variable=checkbox_var)
        recive.pack(padx=10, pady=20)


        label1 = ck.CTkLabel(new_window,width=200,text="الاسم",font=ck.CTkFont(size=18,weight="bold"))
        label1.pack(padx=10, pady=5)

        search_button = ck.CTkButton(new_window, text="بحث",height=15,width=45, fg_color="transparent",command=self.search_coustomer,border_width=2, text_color=("gray10", "#DCE4EE"),font=ck.CTkFont(size=14,weight="bold"))
        search_button.pack(pady=5)  

        self.Name_entry = ck.CTkEntry(new_window,width=200,placeholder_text="زبون جديد")
        self.Name_entry.pack(padx=10, pady=10)

        self.tabview = ck.CTkTabview(new_window, width=250)
        self.tabview.pack(pady=(20, 0))
        self.tabview.add("دفع كامل")
        self.tabview.add("الدفع غير مكتمل")
        self.tabview.tab("دفع كامل").grid_columnconfigure(0, weight=1)
        self.tabview.tab("الدفع غير مكتمل").grid_columnconfigure(0, weight=1)


        full_button = ck.CTkButton( self.tabview.tab("دفع كامل"), text="دفع كامل",height=25,fg_color="green", command=full_pay,font=ck.CTkFont(size=20,weight="bold"))
        full_button.pack(padx=10, pady=15)  

        self.printIMG = ck.CTkImage(Image.open("imags/printer.png"),size=(25,25))

        payLabel = ck.CTkLabel(self.tabview.tab("الدفع غير مكتمل"),text="قيمة الدفع",font=ck.CTkFont(size=17,weight="bold"))
        payValue_entry = ck.CTkEntry(self.tabview.tab("الدفع غير مكتمل"),width=110)

        phoneLabel = ck.CTkLabel(self.tabview.tab("الدفع غير مكتمل"),text="هاتف",font=ck.CTkFont(size=17,weight="bold"))
        self.phone_entry = ck.CTkEntry(self.tabview.tab("الدفع غير مكتمل"),width=120)

        done_button = ck.CTkButton(self.tabview.tab("الدفع غير مكتمل"), text="تم",command=part_done,fg_color="green",height=16,font=ck.CTkFont(size=16,weight="bold"))

        payLabel.pack(pady=7)
        payValue_entry.pack(pady=7)
        phoneLabel.pack(pady=7)
        self.phone_entry.pack(pady=7)
        done_button.pack()

        self.existCustom = False
        self.ExistCustomerID=None

    
    def editShow(self):
        self.discount_frame.grid(row=1, column=0,pady=18,padx=10)
    
    def editTotal(self,event):

        if self.is_valid_entry(self.edit_entry.get()) :

                if self.radio_var.get() == 0 :
                    if float(self.edit_entry.get())>=0 and float(self.edit_entry.get())<=self.Origin_price_variabled:
                        newPrice=self.Origin_price_variabled
                        newPrice=float(newPrice)-float(self.edit_entry.get())
                        discounted_percentage_of_original =100-((newPrice / self.Origin_price_variabled) * 100)
                        self.AfterDiscount.set("المجموع : {:.2f}".format(float(newPrice)))
                        self.discontLabl=f"% {discounted_percentage_of_original:0.3f}"
                        self.AfterDiscountVar=newPrice
                    else:
                        mixer.music.load("sounds/error.mp3")
                        mixer.music.play()
                        messagebox.showwarning("Warning Message","ادخال خاطئ",icon="warning")
                    
                elif self.radio_var.get() == 1 :
                    if float(self.edit_entry.get())>=0 and float(self.edit_entry.get())<=100:
                        newPrice=self.Origin_price_variabled
                        discount_amount=(float(self.edit_entry.get()) / 100) * float(newPrice)
                        discounted_price = float(newPrice) - discount_amount

                        self.AfterDiscount.set("المجموع : {:.2f}".format(float(discounted_price)))
                        self.discontLabl=f"% {self.edit_entry.get()}"
                        self.AfterDiscountVar=discounted_price
                    else:
                        mixer.music.load("sounds/error.mp3")
                        mixer.music.play()
                        messagebox.showwarning("Warning Message","ادخال خاطئ",icon="warning")
                
                self.discount_frame.grid_forget()
                self.AfterDisocuntLabl.grid(row=1, column=0)
        
           
    def search_coustomer(self):

        new_window = tk.Toplevel(self)
        new_window.geometry("640x560")
        new_window.title('Daftar Application')
        

        center_x = int(550)
        center_y = int(150)
        new_window.geometry(f"+{center_x}+{center_y}")

        label = ck.CTkLabel(new_window,width=200,text="الزبائن" ,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold"))
        label.pack(pady=10)
       

        columns = ("id","name","phone")
        table = ttk.Treeview(new_window,columns=columns,height=15, selectmode='browse',show='headings')

        table.column("id", anchor="center",width=70,minwidth=70)
        table.column("name", anchor="center",width=280,minwidth=280)
        table.column("phone", anchor="center",width=70, minwidth=70)
     
        table.heading('id', text='رمز ')
        table.heading('name', text='اسم الزبون')
        table.heading("phone", text='هاتف')

        table.bind('<Motion>','break')
        table.pack(pady=20)

        def selectee():
            selected_item = table.focus()
            values =  table.item(selected_item, 'values')
            self.Name_entry.delete(0,'end')
            self.Name_entry.insert(0, values[1])
            self.phone_entry.delete(0,'end')
            if values[2] == "None":
                self.phone_entry.insert(0,"")
            else:     self.phone_entry.insert(0,values[2])

            self.ExistCustomerID =values[0]
            self.existCustom=True
            
            new_window.destroy()

        done_button = ck.CTkButton(new_window, text="اختر",command=selectee,height=16,font=ck.CTkFont(size=19,weight="bold"))
        done_button.pack(pady=10)


        for row in table.get_children():
            table.delete(row)

        sql_query = """
                    SELECT *
                    FROM Customers
                    Order by CustomerID Asc;
                """

        mycursor.execute(sql_query)

        results = mycursor.fetchall()

        for site in results:
            table.insert('','end',values=(site))

    def is_valid_entry(self,entry_value):
            try:
                float_value = float(entry_value)
                return True
            except ValueError:
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","ادخال خاطئ",icon="warning")
                return False


    def clear(self):
         for row in self.table.get_children():
            self.table.delete(row)

         self.done_button.configure(state="disabled")
         self.Origin_price_variabled=0.00
         self.totalPrice.set("المجموع : 0.00")
         self.cont_entry.delete(0,'end')
         self.cont_entry.insert(0, "1")



    def printAssist(self,order_id):
         
            sql_query = """
                    SELECT Products.ProductID,Products.ProductName, OrderDetails.ProductPrice ,OrderDetails.discount,OrderDetails.Quantity,Products.Unit , OrderDetails.Subtotal, remainAmount, TotalAmount
                    FROM Orders
                    JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
                    JOIN Products ON OrderDetails.ProductID = Products.ProductID
                    WHERE Orders.OrderID = %s;
                """

            mycursor.execute(sql_query, (order_id,))

            results = mycursor.fetchall()


            table_data = [['رمز الصنف','اسم الصنف', 'السعر','خصم', 'الكمية','وحدة', 'المجموع']]

            if results:
                total_amount = results[0][-1] 
        
            for row in results:
                table_row = [row[0], row[1], row[2], row[3],row[4],row[5],row[6]]
                table_data.append(table_row)
    
            if not self.Name_entry.get(): name="-" 
            else:name=self.Name_entry.get()

            sql_query = """
                    SELECT Orders.discount
                    FROM Orders
                    WHERE Orders.OrderID = %s;
                """

            mycursor.execute(sql_query, (order_id,))

            results2 = mycursor.fetchone()

            self.printX(table_data,name,total_amount,order_id,results2[0],f"{order_id}.pdf")


    def printX(self,schedule_data,name,total,id,discount,output_filename):
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


    def search(self, event):
        search_query = self.search_entry.get().lower()

        self.table2.delete(*self.table2.get_children())

        if search_query:
            sql = f"SELECT ProductID,ProductName,sell_Price,Unit  FROM Products WHERE LOWER(ProductName) LIKE '%{search_query}%' and StockQuantity > 0"
            mycursor.execute(sql)
            matching_products = mycursor.fetchall()

            for product in matching_products:
                self.table2.insert("", "end", values=product)
        
        else:self.intTable2()

    
    def searchByID(self, event):
        search_query = self.search_entry2.get().lower()

        self.table2.delete(*self.table2.get_children())

        if search_query:
            sql = f"SELECT ProductID,ProductName,sell_Price,Unit  FROM Products WHERE LOWER(ProductID) LIKE '%{search_query}%' and StockQuantity > 0"
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

    def convert_arabic_to_englishText(self, text):
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
        text = str(text)

        for arabic_digit, english_digit in arabic_to_english.items():
            text = text.replace(arabic_digit, english_digit)

        return text
    

    def is_valid_entry(self,entry_value):
            try:
                float_value = float(entry_value)
                return True
            except ValueError:
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","ادخال خاطئ",icon="warning")
                return False
