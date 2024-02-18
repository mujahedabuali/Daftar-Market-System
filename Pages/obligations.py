
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
        self.elc_img= ck.CTkImage(Image.open("imags/plug.png"),size=(50,50))
        self.wat_img= ck.CTkImage(Image.open("imags/water.png"),size=(50,50))
        self.tr_img= ck.CTkImage(Image.open("imags/delivery-truck.png"),size=(50,50))
        self.emp_img= ck.CTkImage(Image.open("imags/employees.png"),size=(50,50))
        self.other_img= ck.CTkImage(Image.open("imags/bill.png"),size=(50,50))

        self.block_image = ck.CTkImage(Image.open("imags/debitt.png"),size=(40,40))
        self.main_frame = ck.CTkFrame(self,fg_color="transparent")
        self.main_frame.grid(row=0, column=0)
        self.label = ck.CTkLabel(self.main_frame, text="التزامات  ",corner_radius=20,height=50,image=self.block_image,compound="right",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)
        self.menu_frame = ck.CTkFrame(self.main_frame,fg_color="transparent")
        self.menu_frame.pack()

        self.emp_btn = ck.CTkButton(self.menu_frame,image=self.emp_img,width=400, text=" الموظفين",font=ck.CTkFont(size=20,weight="bold") ,command=self.emp_page)
        self.emp_btn.pack(padx=10, pady=5)


        self.elc_btn = ck.CTkButton(self.menu_frame,image=self.elc_img,width=400, text="فواتير الكهرباء",font=ck.CTkFont(size=20,weight="bold"),command=self.elc_page)
        self.elc_btn.pack(padx=10, pady=5)

        self.wat_btn = ck.CTkButton(self.menu_frame,image=self.wat_img,width=400, text="فواتير المياه",font=ck.CTkFont(size=20,weight="bold"))
        self.wat_btn.pack(padx=10, pady=5)

        self.tr_btn = ck.CTkButton(self.menu_frame,image=self.tr_img,width=400, text="فواتير النقل",font=ck.CTkFont(size=20,weight="bold"))
        self.tr_btn.pack(padx=10, pady=5)

        self.other_btn = ck.CTkButton(self.menu_frame,image=self.other_img,width=400, text="فواتير اخرى",font=ck.CTkFont(size=20,weight="bold"))
        self.other_btn.pack(padx=10, pady=5)

    def ret(self):
        if hasattr(self, 'elc_frame'):
            self.elc_frame.grid_forget()
            del self.elc_frame
        if hasattr(self, 'emp_frame'):
            self.emp_frame.grid_forget()
            del self.emp_frame
        # if(self.elc_frame):
        #     self.elc_frame.grid_forget()

        self.main_frame.grid(row=0, column=0)

    def emp_page(self):
        self.main_frame.grid_forget()
        self.emp_frame =ck.CTkFrame(self,fg_color="transparent")
        self.emp_frame.grid(row=0, column=0)
        self.label = ck.CTkLabel(self.emp_frame, text="الموظفين  ",corner_radius=20,height=50,image=self.emp_img,compound="right",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)
        columns = ('id','name', 'salary', 'phone','lastSalary','desc')

        self.emp_table = ttk.Treeview(self.emp_frame,
                              columns=columns,
                              height=19,
                              selectmode='browse',
                              show='headings')

        self.emp_table.column("#1", anchor="c", minwidth=100, width=100)
        self.emp_table.column("#2", anchor="c", minwidth=250, width=250)
        self.emp_table.column("#3", anchor="c", minwidth=100, width=100)
        self.emp_table.column("#4", anchor="c", minwidth=300, width=300)
        self.emp_table.column("#5", anchor="c", minwidth=200, width=200)
        self.emp_table.column("#5", anchor="c", minwidth=200, width=200)

        self.emp_table.heading('id', text='  رقم الموظف ')
        self.emp_table.heading('name', text='الاسم')
        self.emp_table.heading('salary', text=' الراتب')
        self.emp_table.heading('phone', text=' رقم الهاتف')
        self.emp_table.heading('lastSalary', text='  اخر راتب مقبوض')
        self.emp_table.heading('desc', text=' وصف')

        self.emp_table.bind('<Motion>', 'break')
        self.emp_table.bind("<<TreeviewSelect>>", self.on_emp_select)
        self.emp_table.pack()

        button_frame = ck.CTkFrame(self.emp_frame,fg_color="transparent")
        button_frame.pack(fill=ck.Y,expand=True,padx=15,pady=45)

        self.add_button = ck.CTkButton(button_frame, text=" اضافة موظف جديد",height=30,font=ck.CTkFont(size=20,weight="bold"),command=self.add_emp)
        self.add_button.grid(row=0, column=0, padx=10)

        self.delete_button = ck.CTkButton(button_frame, state="disabled", text=" حذف موظف ",height=30,command=self.del_emp,font=ck.CTkFont(size=20,weight="bold"),fg_color="red",)
        self.delete_button.grid(row=0, column=1, padx=10)

        self.edit_button = ck.CTkButton(button_frame,state="disabled", text=" تعديل موظف ",height=30,command=self.edit_emp,font=ck.CTkFont(size=20,weight="bold"))
        self.edit_button.grid(row=0, column=2, padx=10)

        self.pay_button = ck.CTkButton(button_frame,state="disabled", text="دفع راتب",height=30,command=self.pay_emp,fg_color="green",font=ck.CTkFont(size=20,weight="bold") )
        self.pay_button.grid(row=0, column=3, padx=10 )

        s_btn_frame= ck.CTkFrame(self.emp_frame,fg_color="transparent")
        s_btn_frame.pack(fill=ck.Y,expand=True,padx=15,pady=45)

        self.edit_button = ck.CTkButton(s_btn_frame, text="  سجل الرواتب ",height=30,command=self.his_emp,font=ck.CTkFont(size=20,weight="bold"))
        self.edit_button.grid(row=0, column=0, padx=10)

        self.pay_button = ck.CTkButton(s_btn_frame, text=" رجوع",height=30,command=self.ret,fg_color="red",font=ck.CTkFont(size=20,weight="bold") )
        self.pay_button.grid(row=0, column=1, padx=10 )
        self.intempTable()
   
    def add_emp(self):
        def add():
            if (not self.entry.get() or not self.entry2.get() or not self.entry2.get().isdigit() ):
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","قيم الإدخال غير صحيح",icon="warning")
                self.amount.delete(0,'end')
                self.amount.insert(0, "1")
            insert_query = "INSERT INTO employee (name,salary,phone,des ) VALUES (%s, %s,%s,%s)"
            order_data = (self.entry.get(),self.entry2.get(), self.entry3.get(),self.entry4.get())  
            mycursor.execute(insert_query, order_data)
            mydb.commit() 
            self.intempTable()
        
        new_window = tk.Toplevel(self)
        new_window.geometry("440x500")
        new_window.title('اضافة موظف')

        self.label = ck.CTkLabel(new_window, text='اضافة موظف',corner_radius=20,height=50,text_color="red",font=ck.CTkFont(size=30,weight="bold") ) 
        self.label.pack(pady=5)


        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        label1 = ck.CTkLabel(new_window,width=200,text="الاسم:",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)

        label2 = ck.CTkLabel(new_window,width=200,text=" الراتب:",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)

        self.entry2 = ck.CTkEntry(new_window,width=200)
        self.entry2.pack(padx=10, pady=10)

        label3 = ck.CTkLabel(new_window,width=200,text="رقم الهاتف:",font=ck.CTkFont(size=21,weight="bold"))
        label3.pack(padx=10, pady=10)

        self.entry3 = ck.CTkEntry(new_window,width=200)
        self.entry3.pack(padx=10, pady=10)

        label4 = ck.CTkLabel(new_window,width=200,text=" وصف:",font=ck.CTkFont(size=21,weight="bold"))
        label4.pack(padx=10, pady=10)

        self.entry4 = ck.CTkEntry(new_window,width=200)
        self.entry4.pack(padx=10, pady=10)

        ok_button = ck.CTkButton(new_window, text="إضافة", command=add)
        ok_button.pack(padx=10, pady=10)

    def intempTable(self):

        for row in self.emp_table.get_children():
            self.emp_table.delete(row)

        mycursor.execute("SELECT EID,name,salary,phone,lastSalary,des FROM employee")
        mysite = mycursor.fetchall()
        for site in mysite:
            self.emp_table.insert('','end',values=(site))


    def edit_emp(self):
        def update():
            if (not self.entry.get() or not self.entry2.get() or not self.entry2.get().isdigit() ):
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","قيم الإدخال غير صحيح",icon="warning")
                self.amount.delete(0,'end')
                self.amount.insert(0, "1")
            update_query = "UPDATE  employee SET name=%s,salary=%s,phone=%s,des=%s where EID =%s"
            update_data = (self.entry.get(),self.entry2.get(), self.entry3.get(),self.entry4.get(),values[0])  
            mycursor.execute(update_query, update_data)
            mydb.commit() 
            self.intempTable()
        
        new_window = tk.Toplevel(self)
        new_window.geometry("440x500")
        new_window.title('تعديل موظف')

        self.label = ck.CTkLabel(new_window, text='تعديل موظف',corner_radius=20,height=50,text_color="red",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)

        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        label1 = ck.CTkLabel(new_window,width=200,text="الاسم:",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)

        label2 = ck.CTkLabel(new_window,width=200,text=" الراتب:",font=ck.CTkFont(size=21,weight="bold"))
        label2.pack(padx=10, pady=10)

        self.entry2 = ck.CTkEntry(new_window,width=200)
        self.entry2.pack(padx=10, pady=10)

        label3 = ck.CTkLabel(new_window,width=200,text="رقم الهاتف",font=ck.CTkFont(size=21,weight="bold"))
        label3.pack(padx=10, pady=10)

        self.entry3 = ck.CTkEntry(new_window,width=200)
        self.entry3.pack(padx=10, pady=10)

        label4 = ck.CTkLabel(new_window,width=200,text=" الوصف:",font=ck.CTkFont(size=21,weight="bold"))
        label4.pack(padx=10, pady=10)

        self.entry4 = ck.CTkEntry(new_window,width=200)
        self.entry4.pack(padx=10, pady=10)

        selected_item = self.emp_table.focus()

        values =  self.emp_table.item(selected_item, 'values')

        self.entry.delete(0,'end')
        self.entry2.delete(0,'end')
        self.entry3.delete(0,'end')
        self.entry4.delete(0,'end')

        self.entry.insert(0,values[1])
        self.entry2.insert(0,values[2])
        self.entry3.insert(0,values[3])
        self.entry4.insert(0,values[5])

        ok_button = ck.CTkButton(new_window, text="تعديل", command=update)
        ok_button.pack(padx=10, pady=10)   

    def his_emp(self):
        de_win = ck.CTkToplevel(self)

        de_win.geometry("440x500+600+100")
        de_win.title('سجل رواتب الموظفين')

        columns = ('employee','date','amount')
        self.his_emp_table = ttk.Treeview(de_win ,columns=columns,height=14,selectmode='browse',show='headings')

        self.his_emp_table.column("#1", anchor="c", minwidth=300, width=300)
        self.his_emp_table.column("#2", anchor="c", minwidth=200, width=200)
        self.his_emp_table.column("#3", anchor="c", minwidth=100, width=100)
        

        self.his_emp_table.heading('employee', text='الموظف')
        self.his_emp_table.heading('date', text='التاريخ')
        self.his_emp_table.heading('amount', text='المبلغ')
        self.his_emp_table.pack(padx=30,pady=10)

        

        self.his_emp_table.bind('<Motion>', 'break')
        mycursor.execute("SELECT date, amount, EID FROM emp_bills ")
        hiss = mycursor.fetchall()
        for his in hiss:
            mycursor.execute("SELECT name FROM employee where EID=%s ",(his[2],))
            emp = mycursor.fetchone()
            if (emp) :
                self.his_emp_table.insert('','end',values=(emp[0],his[0],his[1]))
            else:
                self.his_emp_table.insert('','end',values=("-",his[0],his[1]))


    def del_emp(self):
        def dele():
            values =  self.emp_table.item(selected_item, 'values')

            update_query = "DELETE FROM employee where EID =%s"
            update_data = (values[0],)  
            mycursor.execute(update_query, update_data)
            mydb.commit() 
            self.intempTable()
            new_window.destroy()
            self.emp_table.selection_remove(self.emp_table.selection())

        
        def canc():
            new_window.destroy()
        new_window = tk.Toplevel(self)
        new_window.geometry("650x300")
        new_window.title('حذف موظف')

        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        label1 = ck.CTkLabel(new_window,width=200,text="متـاكد ؟؟",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)

        selected_item = self.emp_table.focus()


        btn_frame = ck.CTkFrame(new_window ,  fg_color="transparent")
        btn_frame.pack()

        ok_button = ck.CTkButton(btn_frame, text="نعم ", command=dele , fg_color="red")
        ok_button.grid(row=0, column=0,padx=50)
        no_button = ck.CTkButton(btn_frame, text="الغاء ", command=canc)
        no_button.grid(row=0, column=1,padx=50)


    def pay_emp(self):
        def pay():
            values =  self.emp_table.item(selected_item, 'values')
            insert_query = "INSERT INTO emp_bills (date,amount,EID) VALUES (%s,%s,%s)"
            order_data = (datetime.now(),values[2],values[0])  
            mycursor.execute(insert_query, order_data)
            mydb.commit() 
            update_query = "UPDATE employee SET lastSalary=%s WHERE EID=%s"
            update_values = (datetime.now(), values[0])
            mycursor.execute(update_query, update_values)
            mydb.commit()
            values = list(values)
            values[4] = ( datetime.now())
            self.emp_table.item(selected_item, values=tuple(values))
            new_window.destroy()

        
        def canc():
            new_window.destroy()
        new_window = tk.Toplevel(self)
        new_window.geometry("650x300")
        new_window.title(' دفع راتب')

        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        label1 = ck.CTkLabel(new_window,width=200,text="متـاكد ؟؟",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)

        selected_item = self.emp_table.focus()


        btn_frame = ck.CTkFrame(new_window ,  fg_color="transparent")
        btn_frame.pack()

        ok_button = ck.CTkButton(btn_frame, text="نعم ", command=pay , fg_color="green")
        ok_button.grid(row=0, column=0,padx=50)
        no_button = ck.CTkButton(btn_frame, text="الغاء ", command=canc)
        no_button.grid(row=0, column=1,padx=50)


    def on_emp_select(self,event):
        selected_item = self.emp_table.focus()
        if selected_item:
                self.pay_button.configure(state="normal")
                self.delete_button.configure(state="normal")
                self.edit_button.configure(state="normal")
        else :
            self.pay_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")
            self.edit_button.configure(state="disabled")


    def elc_page(self):
        self.main_frame.grid_forget()
        self.elc_frame =ck.CTkFrame(self,fg_color="transparent")
        self.elc_frame.grid(row=0, column=0)
        self.label = ck.CTkLabel(self.elc_frame, text="فواتير الكهرباء  ",corner_radius=20,height=50,image=self.elc_img,compound="right",font=ck.CTkFont(size=30,weight="bold")) 
        self.label.pack(pady=5)


        columns = ('billid','date','amount')
        self.his_elc_table = ttk.Treeview(self.elc_frame ,columns=columns,height=14,selectmode='browse',show='headings')

        self.his_elc_table.column("#1", anchor="c", minwidth=100, width=100)
        self.his_elc_table.column("#2", anchor="c", minwidth=200, width=200)
        self.his_elc_table.column("#3", anchor="c", minwidth=100, width=100)
        

        self.his_elc_table.heading('billid', text='رقم الفاتوره')
        self.his_elc_table.heading('date', text='التاريخ')
        self.his_elc_table.heading('amount', text='المبلغ')
        self.his_elc_table.pack(padx=30,pady=10)

        

        self.his_elc_table.bind('<Motion>', 'break')
        self.intelcTable()
        add_btn = ck.CTkButton(self.elc_frame , text="اضافه فاتوره",command=self.add_elc_bill)
        add_btn.pack(pady=10,padx=10)
        ret_btn = ck.CTkButton(self.elc_frame , text=" رجوع",fg_color="red",command=self.ret)
        ret_btn.pack(pady=10,padx=10)
    
    def add_elc_bill(self):
        def add():
            if (not self.entry.get() or not self.entry.get().isdigit() ):
                mixer.music.load("sounds/error.mp3")
                mixer.music.play()
                messagebox.showwarning("Warning Message","قيم الإدخال غير صحيح",icon="warning")
                self.amount.delete(0,'end')
                self.amount.insert(0, "1")
            insert_query = "INSERT INTO elc_bills (date,amount) VALUES (%s,%s)"
            order_data = (datetime.now(),self.entry.get())  
            mycursor.execute(insert_query, order_data)
            mydb.commit() 
            self.intelcTable()
        
        new_window = tk.Toplevel(self)
        new_window.geometry("340x300")
        new_window.title('اضافة فاتوره')

        self.label = ck.CTkLabel(new_window, text='اضافة فاتوره',corner_radius=20,height=50,text_color="red",font=ck.CTkFont(size=30,weight="bold") ) 
        self.label.pack(pady=5)


        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        label1 = ck.CTkLabel(new_window,width=200,text="المبلغ:",font=ck.CTkFont(size=21,weight="bold"))
        label1.pack(padx=10, pady=10)

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)
        add_btn = ck.CTkButton(new_window, text="اضافه" , command=add)
        add_btn.pack(padx=10,pady=10)

    def intelcTable(self):
        mycursor.execute("SELECT BID ,date, amount FROM elc_bills ")
        hiss = mycursor.fetchall()
        for his in hiss:
                self.his_elc_table.insert('','end',values=(his))


                
