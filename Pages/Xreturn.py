import customtkinter as ck
from PIL import Image
from tkinter import ttk
from db import mycursor,mydb
from tkinter import messagebox
from datetime import datetime


class Return(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

        self.bookmark_image = ck.CTkImage(Image.open("imags/return.png"),size=(40,40))
        self.label = ck.CTkLabel(self, text="ارجاع  ",image=self.bookmark_image,corner_radius=20,compound="right",height=50,font=ck.CTkFont(size=30,weight="bold")) 
        self.label.grid(row=0, column=0, columnspan=2,sticky="nsew")
    
        frame = ck.CTkFrame(self,fg_color="transparent")
        frame.grid(row=1, column=0)

        self.totalPrice=ck.StringVar()
        self.totalPrice.set("name" )

        ####### Right table #############
        columns2 = ('name','price','rem','orderid')
        self.table2 = ttk.Treeview(frame,columns=columns2,height=14,selectmode='browse',show='headings')

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


        self.search_entry = ck.CTkEntry(frame,placeholder_text="search")
        self.search_entry.pack(pady=35)
        # self.search_entry.bind("<KeyRelease>", self.search)
        self.table2.pack(expand=False,padx=0,pady=0)

        add_frame = ck.CTkFrame(frame,fg_color="transparent")
        add_frame.pack(fill=ck.Y,expand=False,padx=15,pady=15)


        self.det_button = ck.CTkButton(add_frame, text="عرض ",height=30,command=self.det,font=ck.CTkFont(size=20,weight="bold"))
        self.det_button.configure(state="disabled")
        self.det_button.grid(row=0, column=0, padx=10,pady=10)


        
        self.intTable()
        
        



    def intTable(self):

        for row in self.table2.get_children():
            self.table2.delete(row)

        mycursor.execute("SELECT OrderId,CustomerID,remainAmount,TotalAmount FROM Orders ORDER BY OrderDate DESC ")
        mysite = mycursor.fetchall()
        for site in mysite:
            mycursor.execute("SELECT CustomerName FROM customers where CustomerID=%s",(site[1],))
            name = mycursor.fetchone()
            if name :
                self.table2.insert('','end',values=(name[0],site[3],site[2],site[0]))
            else:
                self.table2.insert('','end',values=("-",site[3],site[2],site[0]))




    def on_item_select(self,event):
        selected_item = self.table2.focus()
        if selected_item:
                self.det_button.configure(state="normal")
        else :
            self.det_button.configure(state="disabled")
  



    def det(self):
        self.de_win = ck.CTkToplevel(self)

        self.de_win.geometry("440x500+600+100")
        self.de_win.title('الفاتورة')


        columns = ('name','qun','price','producid')
        self.table = ttk.Treeview(self.de_win ,columns=columns,height=14,selectmode='browse',show='headings')

        self.table.column("#1", anchor="c", minwidth=100, width=100)
        self.table.column("#2", anchor="c", minwidth=100, width=100)
        self.table.column("#3", anchor="c", minwidth=100, width=100)
        self.table.column("#4", anchor="c", minwidth=100, width=100)
        

        self.table.heading('name', text='الاسم')
        self.table.heading('qun', text='عدد')
        self.table.heading('price', text='السعر')
        self.table.heading('producid', text='رقم الصنف')
        self.table.pack(padx=30,pady=10)
        self.table.bind("<<TreeviewSelect>>", self.on_item_select2)


        

        self.table.bind('<Motion>', 'break')
        selected_item = self.table2.focus()

        values =  self.table2.item(selected_item, 'values')
        mycursor.execute("SELECT ProductID , Quantity FROM orderdetails where OrderID=%s",(values[3],))
        prs = mycursor.fetchall()
        for pr in prs :
            mycursor.execute("SELECT ProductName , sell_Price FROM products where ProductID=%s",(pr[0],))
            pr_info = mycursor.fetchone()
            self.table.insert('','end',values=(pr_info[0],pr[1],pr_info[1],pr[0]))

        self.num_pro = ck.CTkEntry(self.de_win)
        self.num_pro.pack(pady=10)

        self.re_button = ck.CTkButton(self.de_win, text="ارجاع ",height=30,command=self.re,font=ck.CTkFont(size=20,weight="bold"))
        self.re_button.configure(state="disabled")
        self.re_button.pack(pady=10)

    def re(self):
            selected_it = self.table2.focus()
            valuesO =  self.table2.item(selected_it, 'values')
            selected_item = self.table.focus()
            if selected_item:
                values =  self.table.item(selected_item, 'values')
                if (not self.num_pro.get() or not self.num_pro.get().isdigit() ):
                    messagebox.showwarning("Warning Message","قيم الإدخال غير صحيح",icon="warning")
                    self.num_pro.delete(0,'end')
                    self.num_pro.insert(0, "1")  
                else:
                    if  int(self.num_pro.get()) > int(values[1])  :
                        messagebox.showwarning("Warning Message",f"لا يمكنك ارجاع اكثر من {values[1]}",icon="warning")
                        return
                    update_query = "UPDATE orderdetails SET Quantity=%s WHERE OrderID=%s and ProductID=%s"
                    update_values = (int(values[1])-int(self.num_pro.get()) , valuesO[3],values[3])
                    mycursor.execute(update_query, update_values)
                    mydb.commit()

                    values = list(values)
                    values[1] = int(values[1])-int(self.num_pro.get())
                    # Update the values for the selected item
                    self.table.item(selected_item, values=tuple(values))

                    if values[1] ==0 :
                        update_query = "DELETE FROM orderdetails WHERE OrderID = %s AND ProductID = %s;"
                        update_values = ( valuesO[3],values[3])
                        mycursor.execute(update_query, update_values)
                        mydb.commit()
                        self.table.delete(selected_item)


                    mycursor.execute("SELECT TotalAmount , remainAmount FROM orders where OrderID=%s",(valuesO[3],))
                    ord_info = mycursor.fetchone()

                    if ((float(ord_info[0]) <= (int(self.num_pro.get())*float(values[2])))):
                        update_query = "DELETE FROM orders WHERE OrderID=%s"
                        update_values = ( valuesO[3],)
                        mycursor.execute(update_query, update_values)
                        mydb.commit()
                    else:
                        if ((float(ord_info[1]) <= (int(self.num_pro.get())*float(values[2])))):
                            update_query = "UPDATE orders SET TotalAmount=%s , remainAmount=0,receive =1  WHERE OrderID=%s"
                            update_values = ((float(ord_info[0])-(int(self.num_pro.get())*float(values[2]))), valuesO[3])
                            mycursor.execute(update_query, update_values)
                            mydb.commit()
                            if ((float(ord_info[1]) < (int(self.num_pro.get())*float(values[2])))):
                                re_value=(float(ord_info[1]) - (int(self.num_pro.get())*float(values[2])))
                                insert_pay_query = "INSERT INTO payments (paymentDate,Amount,OrderID) VALUES (%s, %s,%s)"
                                order_data = (datetime.now(), re_value,valuesO[3])  
                                mycursor.execute(insert_pay_query, order_data)
                                mydb.commit() 
                                self.re_label = ck.CTkLabel(self.de_win,text="ارجاع {re_value}", font=ck.CTkFont(family="DecoType Naskh",size=35, weight="bold"))
                                
                                self.re_label.pack(pady=10)


                        else:                           
                            update_query = "UPDATE orders SET TotalAmount=%s , remainAmount=%s WHERE OrderID=%s"
                            update_values = ((float(ord_info[0])-(int(self.num_pro.get())*float(values[2]))),(float(ord_info[1])-(int(self.num_pro.get())*float(values[2]))), valuesO[3])
                            mycursor.execute(update_query, update_values)
                            mydb.commit()


                    mycursor.execute("SELECT StockQuantity FROM products where ProductID=%s",(values[3],))
                    old_qun = mycursor.fetchone()
                    update_query = "UPDATE products SET StockQuantity=%s  WHERE ProductID=%s"
                    update_values = (int(old_qun[0])+int(self.num_pro.get()), values[3])
                    mycursor.execute(update_query, update_values)
                    mydb.commit()
                    self.intTable()


    def on_item_select2(self,event):
        selected_item = self.table.focus()
        if selected_item:
                self.re_button.configure(state="normal")
        else :
            self.re_button.configure(state="disabled")
  
