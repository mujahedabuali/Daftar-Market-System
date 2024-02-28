import customtkinter as ck
from PIL import Image
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from db import mycursor,mydb
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkcalendar import Calendar
from datetime import datetime, timedelta

class Stat(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

      
        # print(entered_username)

        self.bookmark_image = ck.CTkImage(Image.open("imags/stats.png"),size=(40,40))
        self.label = ck.CTkLabel(self, text="حسابات  ",image=self.bookmark_image,corner_radius=20,compound="right",height=50,font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)
        self.tabview = ck.CTkTabview(self, width=1200)
        self.tabview.pack()
        self.tabview.add(" حسابات عامه")
        self.tabview.add("جرار")
        self.tabview.tab(" حسابات عامه").grid_columnconfigure(0, weight=1)  
        self.tabview.tab("جرار").grid_columnconfigure(0, weight=1)
        self.main = ck.CTkFrame(self.tabview.tab(" حسابات عامه"),fg_color="transparent")
        self.main.pack()
        self.date_frame = ck.CTkFrame(self.main , fg_color="transparent")
        self.date_frame.pack()
        current_date = datetime.now()
        current_day = current_date.strftime('%d')
        current_day = int(current_day)
        start_date = datetime.now() - timedelta(days=current_day-1)
        end_date = datetime.now()

        self.from_cal = Calendar(self.date_frame, selectmode='day',
            showweeknumbers=False, cursor="hand2", date_pattern= 'y-m-d',
            borderwidth=1)
        self.from_cal.selection_set(start_date)
        from_label = ck.CTkLabel(self.date_frame,text="من")
        from_label.grid(row=0,column=0 , padx=15)
        self.from_cal.grid(row=0,column=1,padx=15)
        self.to_cal = Calendar(self.date_frame, selectmode='day',
            showweeknumbers=False, cursor="hand2", date_pattern= 'y-m-d',
            borderwidth=1)
        self.to_cal.selection_set(end_date)

        to_label = ck.CTkLabel(self.date_frame,text="الى")
        to_label.grid(row=0,column=2,padx=15)
        self.to_cal.grid(row=0,column=3,padx=15)
        search_btn = ck.CTkButton(self.date_frame , text="بحث" , command=self.search, text_color="white",font=ck.CTkFont(size=18,weight="bold"))
        search_btn.grid(row=0,column=4)
        self.tables_frame = ck.CTkFrame(self.main,fg_color="transparent")
        self.tables_frame.pack()
        d_label = ck.CTkLabel(self.tables_frame , text="دائن", text_color="white",font=ck.CTkFont(size=20,weight="bold"))
        d_label.grid(row=0,column=0,pady=(20,0))
        columns = ('name','price')
        self.table = ttk.Treeview(self.tables_frame ,columns=columns,height=14,selectmode='browse',show='headings')

        self.table.column("#1", anchor="c", minwidth=300, width=300)
        self.table.column("#2", anchor="c", minwidth=100, width=100)
        

        self.table.heading('name', text='العنصر')
        self.table.heading('price', text='المبلغ')
        

        self.table.bind('<Motion>', 'break')
        self.table.grid(row=1,column=0,padx=15,pady=30)
        self.d_total_label = ck.CTkLabel(self.tables_frame , text="")
        self.d_total_label.grid(row=2,column=0)

        md_label = ck.CTkLabel(self.tables_frame , text="مدين", text_color="white",font=ck.CTkFont(size=20,weight="bold"))
        md_label.grid(row=0,column=1,pady=(30,0))
        columns = ('name','price')
        self.table2 = ttk.Treeview(self.tables_frame ,columns=columns,height=14,selectmode='browse',show='headings')

        self.table2.column("#1", anchor="c", minwidth=300, width=300)
        self.table2.column("#2", anchor="c", minwidth=100, width=100)
        

        self.table2.heading('name', text='العنصر')
        self.table2.heading('price', text='المبلغ')
        

        self.table2.bind('<Motion>', 'break')
        self.table2.grid(row=1,column=1,padx=15,pady=30)
        self.md_total_label = ck.CTkLabel(self.tables_frame , text="")
        self.md_total_label.grid(row=2,column=1)

        self.intMD()
        self.intD()
        self.total_dm = ck.CTkLabel(self.main , text=f" صافي :   ({self.d_total}     -     {self.m_total}     =     {self.d_total-self.m_total})" , text_color="red",font=ck.CTkFont(size=20,weight="bold"))
        self.total_dm.pack()


    def intMD(self):
        for row in self.table2.get_children():
            self.table2.delete(row)
        self.m_total = 0
        mycursor.execute("SELECT SUM(eb.amount) FROM emp_bills AS eb WHERE eb.date >= %s AND eb.date <= %s;", (self.from_cal.get_date(), self.to_cal.get_date()))
        result = mycursor.fetchone()
        self.table2.insert("","end",values=("رواتب الموظفين",result[0] if result[0] is not None else "0"))

        if result and result[0] !=None :
            self.m_total+=float(result[0])

        mycursor.execute("select sum(elb.amount) from elc_bills as elb WHERE elb.date >= %s AND elb.date <= %s;", (self.from_cal.get_date(), self.to_cal.get_date()))
        result = mycursor.fetchone()
        self.table2.insert("","end",values=("كهرباء ",result[0] if result[0] is not None else "0"))
        if result and result[0] !=None :
            self.m_total+=float(result[0])


        mycursor.execute("SELECT SUM(wb.amount) FROM wat_bills AS wb WHERE wb.date >= %s AND wb.date <= %s;", (self.from_cal.get_date(), self.to_cal.get_date()))
        result = mycursor.fetchone()
        self.table2.insert("","end",values=(" ماء",result[0] if result[0] is not None else "0"))
        if result and result[0] !=None :
            self.m_total+=float(result[0])

        mycursor.execute("select sum(tb.amount) from tr_bills as tb WHERE tb.date >= %s AND tb.date <= %s;", (self.from_cal.get_date(), self.to_cal.get_date()))
        result = mycursor.fetchone()
        self.table2.insert("","end",values=(" نقل",result[0] if result[0] is not None else "0"))
        if result and result[0] !=None :
            self.m_total+=float(result[0])

        mycursor.execute("select title , amount from ot_bills as ob WHERE ob.date >= %s AND ob.date <= %s;", (self.from_cal.get_date(), self.to_cal.get_date()))
        res = mycursor.fetchall()
        for resul in res :
            self.m_total+=float(resul[1])
            self.table2.insert("","end",values=(resul))

        self.md_total_label.configure(text=self.m_total)    


    def intD(self):
        for row in self.table.get_children():
            self.table.delete(row)
        self.d_total = 0
        mycursor.execute("select sum(od.Subtotal) from orderdetails as od , orders as o where od.OrderID = o.OrderID and o.OrderDate >= %s AND o.OrderDate <= %s;", (self.from_cal.get_date(), self.to_cal.get_date()))
        result = mycursor.fetchone()
        self.table.insert("","end",values=("بيع ",result[0] if result[0] is not None else "0"))
        if result and result[0] !=None :
            self.d_total+=float(result[0])

        self.d_total_label.configure(text=self.d_total)    

    def search(self):
        self.intMD()
        self.intD()
        self.total_dm.configure( text=f" صافي({self.d_total}     -     {self.m_total}     =     {self.d_total-self.m_total})")





        
