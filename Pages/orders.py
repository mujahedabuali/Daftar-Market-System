
import customtkinter as ck
from PIL import Image
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from db import mycursor,mydb
import mysql.connector
from pygame import mixer


class Orders(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

        self.bookmark_image = ck.CTkImage(Image.open("imags/order.png"),size=(40,40))
        self.label = ck.CTkLabel(self, text="طلبيات ",image=self.bookmark_image,corner_radius=20,compound="right",height=50,font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)
        
        self.correctIMG = ck.CTkImage(Image.open("imags/check-mark.png"),size=(30,30))

        search_entry = ck.CTkEntry(self,placeholder_text="search")
        search_entry.pack(pady=10)
        
        columns = ("id","name","date","total","payed","recive","remain")
        self.table = ttk.Treeview(self,columns=columns,height=20, selectmode='browse',show='headings')

        self.table.column("id", anchor="center",width=50,minwidth=50)
        self.table.column("name", anchor="center",width=250,minwidth=250)
        self.table.column("date", anchor="center",width=80, minwidth=80)
        self.table.column("total", anchor="center",width=80, minwidth=80)
        self.table.column("payed", anchor="center",width=80, minwidth=80)
        self.table.column("recive", anchor="center",width=80, minwidth=80)
        self.table.column("remain", anchor="center",width=100, minwidth=100)
     
        self.table.heading('id', text='رمز الفاتورة ')
        self.table.heading('name', text='اسم الزبون')
        self.table.heading('date', text='تاريخ الطلبية')
        self.table.heading("total", text='قيمة الفاتورة')
        self.table.heading("payed", text='الدفع')
        self.table.heading("recive", text='تسليم')
        self.table.heading("remain", text='الدفع المتبقي')

        self.table.bind('<Motion>','break')
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, fieldbackground="Black")
        style.map("Treeview", background=[('selected', '#347083')])
        style.configure("Treeview", highlightthickness=0, bd=0)


        self.scrollbar = ck.CTkScrollbar(self, orientation=ck.VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side=ck.RIGHT, fill=ck.Y)

        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.table.pack(fill=ck.BOTH, expand=False,padx=15,pady=30)

        button_frame = ck.CTkFrame(self,fg_color="transparent")
        button_frame.pack(fill=ck.Y,expand=True,padx=15,pady=45) 

        self.detail_button = ck.CTkButton(button_frame, text="تفاصيل الفاتورة",height=40,command=self.show_detial,font=ck.CTkFont(size=20,weight="bold"))
        self.detail_button.grid(row=0, column=1, padx=10)
        self.detail_button.configure(state="disabled")

        self.done_button = ck.CTkButton(button_frame, text=" تسليم",fg_color="green",image=self.correctIMG, compound="left",height=40,command=self.done_info,font=ck.CTkFont(size=20,weight="bold"))
        self.done_button.grid(row=0, column=0, padx=10)
        self.done_button.configure(state="disabled")

        self.intTable()


    def intTable(self):

        for row in self.table.get_children():
            self.table.delete(row)

        mycursor.execute("SELECT OrderID,CustomerID,OrderDate,TotalAmount,Status,receive,remainAmount FROM Orders WHERE receive =0 ORDER BY OrderDate DESC " )
        mysite = mycursor.fetchall()


        for site in mysite:
            name =self.get_customer_name(site[1])
            status = " كامل" if site[4] == "1" else "ناقص"
            receive = "استلم" if site[5] == 1 else "لم يستلم"
            remain ="-" if not site[6]else site[6]
            site_with_name = (site[0],name, site[2], site[3], status, receive,remain)
            self.table.insert('','end',values=(site_with_name))

    def search(self, event):
        search_query = self.search_entry.get().lower()
        self.table.selection_remove(self.table.selection())
        
        for item in self.table.get_children():
            name = self.table.item(item)["values"][0]
            name = name.lower()

            if search_query in name:
                self.table.selection_add(item)
                self.table.see(item)


    def get_customer_name(self,customer_id):
        select_customer_query = "SELECT CustomerName FROM Customers WHERE CustomerID = %s"
        mycursor.execute(select_customer_query, (customer_id,))
        result = mycursor.fetchall()
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
        new_window.title('تفاصيل الفاتورة')

        center_x = int(550)
        center_y = int(150)
        new_window.geometry(f"+{center_x}+{center_y}")

       
        
        selected_item = self.table.focus()
        values =  self.table.item(selected_item, 'values')

        columns = ("id","name","date","remain","total")
        table = ttk.Treeview(new_window,columns=columns,height=15, selectmode='browse',show='headings')

        table.column("id", anchor="center",width=60,minwidth=60)
        table.column("name", anchor="center",width=250,minwidth=250)
        table.column("date", anchor="center",width=80, minwidth=80)
        table.column("remain", anchor="center",width=100, minwidth=100)
        table.column("total", anchor="center",width=80, minwidth=80)
     
        table.heading('id', text='رمز الصنف')
        table.heading('name', text='اسم الصنف')
        table.heading('date', text='السعر')
        table.heading("remain", text='كمية')
        table.heading("total", text='مجموع')

        table.bind('<Motion>','break')

        name_var = tk.StringVar()
        name_var.set(values[1])  # Set an initial value

        total_var = tk.StringVar()
        total_var.set(values[3])  # Set an initial value

        date_var = tk.StringVar()
        date_var.set(values[2])  # Set an initial value
        
        labelFrame =ck.CTkFrame(new_window,fg_color="transparent")
        labelFrame.pack(padx=15,pady=25)

        label1 = ck.CTkLabel(labelFrame,width=200,text="الاسم: " +name_var.get() ,font=ck.CTkFont(size=19,weight="bold"))
        label1.grid(row=0, column=2, padx=10)

        label2 = ck.CTkLabel(labelFrame,width=200,text=" مجموع الفاتورة: "+total_var.get(),font=ck.CTkFont(size=19,weight="bold"))
        label2.grid(row=0, column=1, padx=10)

        label3 = ck.CTkLabel(labelFrame,width=200,text="تاريخ : "+date_var.get(),font=ck.CTkFont(size=19,weight="bold"))
        label3.grid(row=0, column=0, padx=10)
        
        
        table.pack(pady=20)

        for row in table.get_children():
            table.delete(row)

        sql_query = """
                    SELECT Products.ProductID, Products.ProductName, Products.Price ,OrderDetails.Quantity,OrderDetails.Subtotal
                    FROM Orders
                    JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
                    JOIN Products ON OrderDetails.ProductID = Products.ProductID
                    WHERE Orders.OrderID = %s;
                """

        mycursor.execute(sql_query, (values[0],))

        results = mycursor.fetchall()

        for site in results:
            table.insert('','end',values=(site))


    def done(self):
        selected_item = self.table.focus()
        if selected_item:
            self.show_detial_info()
        else:  
            mixer.music.load("sounds/error.mp3")
            mixer.music.play()
            messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")

    def done_info(self):
        
        selected_item = self.table.focus()
        values =  self.table.item(selected_item, 'values')

        sql_query = """
                    UPDATE Orders
                    SET receive = 1
                    WHERE Orders.OrderID = %s;
                """

        mycursor.execute(sql_query, (values[0],))
        mydb.commit()

        mixer.music.load("sounds/done.wav")
        mixer.music.play()
        
        self.intTable()

    def on_item_select(self,event):
        selected_item = self.table.focus()
        if selected_item:
                self.detail_button.configure(state="normal")
                self.done_button.configure(state="normal")
        else :
                self.detail_button.configure(state="disabled")  
                self.done_button.configure(state="normal")  
