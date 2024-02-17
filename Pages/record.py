
import customtkinter as ck
from PIL import Image
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from pygame import mixer
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector
from db import mycursor,mydb

class Record(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.bookmark_image = ck.CTkImage(Image.open("imags/notes.png"),size=(40,40))
        self.label = ck.CTkLabel(self, text="السجل ",image=self.bookmark_image,corner_radius=20,compound="right",height=50,font=ck.CTkFont(size=30,weight="bold")) 
        self.label.grid(row=0, column=0, columnspan=2,sticky="nsew")
    

        left_frame = ck.CTkFrame(self,fg_color="transparent")
        right_frame = ck.CTkFrame(self,fg_color="transparent")
        right_frame.grid(row=1, column=1, sticky="nsew")

        self.totalPrice=ck.StringVar()
        self.totalPrice.set("name" )

        mixer.init()

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
        

        button_frame = ck.CTkFrame(left_frame,fg_color="transparent")
        button_frame.pack(expand=False,padx=15,pady=0)


        total_frame = ck.CTkFrame(left_frame,fg_color="transparent")
        total_frame.pack(pady=20)




        ####### Right table #############
        columns2 = ('name','price','rem','orderid')
        self.table2 = ttk.Treeview(right_frame,columns=columns2,height=14,selectmode='browse',show='headings')

        self.table2.column("#1", anchor="c", minwidth=200, width=200)
        self.table2.column("#2", anchor="c", minwidth=100, width=100)
        self.table2.column("#3", anchor="c", minwidth=100, width=100)
        self.table2.column("#4", anchor="c", minwidth=100, width=100)
        
        self.table2.heading('name', text='الزبون')
        self.table2.heading('price', text=' المبلغ الاصلي')
        self.table2.heading('rem', text=' المبلغ المتبقي')
        self.table2.heading('orderid', text='رقم الفاتورة')

        self.table2.bind('<Motion>', 'break')
        self.table2.bind("<<TreeviewSelect>>", self.on_item_select)


        self.search_entry = ck.CTkEntry(right_frame,placeholder_text="search")
        self.search_entry.pack(pady=35)
        # self.search_entry.bind("<KeyRelease>", self.search)
        self.table2.pack(expand=False,padx=0,pady=0)

        add_frame = ck.CTkFrame(right_frame,fg_color="transparent")
        add_frame.pack(fill=ck.Y,expand=False,padx=15,pady=15)

        self.pay_win_button = ck.CTkButton(add_frame, text="دفعة ",height=30,command=self.pay_wind,font=ck.CTkFont(size=20,weight="bold"))
        self.pay_win_button.configure(state="disabled")
        self.pay_win_button.grid(row=1, column=0, padx=10)

        self.det_button = ck.CTkButton(add_frame, text="تفاصيل ",height=30,command=self.det,font=ck.CTkFont(size=20,weight="bold"))
        self.det_button.configure(state="disabled")
        self.det_button.grid(row=0, column=0, padx=10,pady=10)


        
        self.intTable()
      

    def intTable(self):

        for row in self.table2.get_children():
            self.table2.delete(row)

        mycursor.execute("SELECT OrderId,CustomerID,remainAmount,TotalAmount FROM Orders where Status=0 ORDER BY OrderDate DESC ")
        mysite = mycursor.fetchall()
        for site in mysite:
            mycursor.execute("SELECT CustomerName FROM customers where CustomerID=%s",(site[1],))
            name = mycursor.fetchall()
            if name[0] :
                self.table2.insert('','end',values=(name[0],site[3],site[2],site[0]))

   

    def intTable1(self):
        selected_item = self.table2.focus()
        values =  self.table2.item(selected_item, 'values')

        for row in self.table.get_children():
            self.table.delete(row)

        mycursor.execute("SELECT paymentDate,Amount FROM payments where OrderID=%s ORDER BY paymentDate DESC ",(values[3],))
        mysite = mycursor.fetchall()
        for site in mysite:
            self.table.insert('','end',values=(site))

    def pay_wind(self):
        self.de_win = ck.CTkToplevel(self)
        self.amount = ck.CTkEntry(self.de_win)
        self.amount.pack(padx=10,pady=30)

        self.pay_button = ck.CTkButton(self.de_win, text="دفع ",height=30,command=self.pay,font=ck.CTkFont(size=20,weight="bold"))
        self.pay_button.pack(padx=10,pady=30)


        self.de_win.geometry("440x340+600+100")
        self.de_win.title('دفعة')
   
    def det(self):
        de_win = ck.CTkToplevel(self)
        selected_item = self.table2.focus()
        values =  self.table2.item(selected_item, 'values')
        mycursor.execute("SELECT CustomerID FROM orders where OrderID=%s",(values[3],))
        userid = mycursor.fetchone()
        mycursor.execute("SELECT CustomerName , Phone FROM customers where CustomerID=%s",(userid[0],))
        user = mycursor.fetchone()

        de_win.geometry("440x500+600+100")
        de_win.title('التفاصيل')

        name = ck.CTkLabel(de_win,text=f"name : {user[0]}",text_color="black",corner_radius=20,height=30,font=ck.CTkFont(size=20,weight="bold") )
        name.pack(pady=10)
        phone = ck.CTkLabel(de_win,text=f"Phone : {user[1]}",text_color="black",corner_radius=20,height=30,font=ck.CTkFont(size=20,weight="bold"))
        phone.pack(pady=10)


        columns = ('date','amount')
        self.table = ttk.Treeview(de_win ,columns=columns,height=14,selectmode='browse',show='headings')

        self.table.column("#1", anchor="c", minwidth=300, width=300)
        self.table.column("#2", anchor="c", minwidth=100, width=100)
        

        self.table.heading('date', text='التاريخ')
        self.table.heading('amount', text='المبلغ')
        self.table.pack(padx=30,pady=10)

        

        self.table.bind('<Motion>', 'break')
        self.intTable1()

        
    def pay(self):
        selected_item = self.table2.focus()
        
        if selected_item:
            if (not self.amount.get() or not self.amount.get().isdigit() ):
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","قيم الإدخال غير صحيح",icon="warning")
                self.amount.delete(0,'end')
                self.amount.insert(0, "1")
            
            else:
                values =  self.table2.item(selected_item, 'values')
                if  float(self.amount.get()) > float(values[2])  :
                    messagebox.showwarning("Warning Message",f"لا يمكنك دفع اكثر من {values[2]}",icon="warning")
                    return

                insert_pay_query = "INSERT INTO payments (paymentDate,Amount,OrderID) VALUES (%s, %s,%s)"
                order_data = (datetime.now(), self.amount.get(),values[3])  
                mycursor.execute(insert_pay_query, order_data)
                mydb.commit() 
                # self.table.insert('','end',values=(datetime.now(), self.amount.get()))
                update_query = "UPDATE Orders SET remainAmount=%s WHERE OrderID=%s"
                update_values = (float(values[2]) - float(self.amount.get()), values[3])
                mycursor.execute(update_query, update_values)
                mydb.commit()
                        # Modify the desired column with the new value
                values = list(values)
                values[2] = ( float(values[2]) - float(self.amount.get()))

                # Update the values for the selected item
                self.table2.item(selected_item, values=tuple(values))
                if values[2] ==0 :
                    update_query = "UPDATE Orders SET Status=1 WHERE OrderID=%s"
                    mycursor.execute(update_query, (values[3],))
                    mydb.commit()
                    self.table2.delete(selected_item)
                
                self.de_win.destroy()

    def on_item_select(self,event):
        selected_item = self.table2.focus()
        if selected_item:
                self.pay_win_button.configure(state="normal")
                self.det_button.configure(state="normal")
        else :
            self.pay_win_button.configure(state="disabled")
            self.det_button.configure(state="disabled")
  
