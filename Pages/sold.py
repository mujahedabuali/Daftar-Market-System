
import customtkinter as ck
from PIL import Image
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from db import mycursor,mydb
import mysql.connector
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
        self.detail_button.pack()
        self.detail_button.configure(state="disabled")

        self.printIMG = ck.CTkImage(Image.open("imags/printer.png"),size=(30,30))
        self.print_button = ck.CTkButton(button_frame, text="",image=self.printIMG,compound="left",width=10,fg_color="transparent",command=self.printAssist)
        self.print_button.pack(pady=15)
        self.print_button.configure(state="disabled")
  

        self.intTable()

        ###### customers ######

        self.search_entry2 = ck.CTkEntry(self.tabview.tab("زبائن"),placeholder_text="search")
        self.search_entry2.pack(pady=10)
        self.search_entry2.bind("<KeyRelease>", self.search)
        
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

        self.print_button2 = ck.CTkButton(button_frame2, text="كشف حساب",image=self.printIMG,compound="left",font=ck.CTkFont(size=20,weight="bold"),width=10,command=self.printAssist)
        self.print_button2.pack(pady=15)
        self.print_button2.configure(state="disabled")
  

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

    def search(self, event):
        search_query = self.search_entry.get().lower()
        self.table.selection_remove(self.table.selection())
        
        for item in self.table.get_children():
            name = self.table.item(item)["values"][0]
            name = name.lower()

            if search_query in name:
                self.table.selection_add(item)
                self.table.see(item)

    def delete_item(self):
         selected_item = self.table.focus()
         if selected_item:
            values = self.table.item(selected_item, "values")
            mixer.music.load("sounds/warning.wav")
            mixer.music.play()
            sure = messagebox.askyesno("Confirmation", f"متأكد ؟ \n حذف {values[0]}",icon="warning")
            if sure :
                mixer.music.load("sounds/done.wav")
                mixer.music.play()
                query = "SELECT ProductID FROM Products Where ProductName = %s"
                mycursor.execute(query, (values[0],))
                result = mycursor.fetchone()

                try:
                    mycursor.execute("DELETE FROM Products WHERE ProductID = %s",(result[0],))
                    mydb.commit() 
                    self.intTable()
                except mysql.connector.Error as err:
                    messagebox.showwarning("Warning Message","حركة خاطئة",icon="warning")   
         else:  
            mixer.music.load("sounds/error.mp3")
            mixer.music.play()
            messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")


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
        new_window.title('Daftar Application')
        

        center_x = int(550)
        center_y = int(150)
        new_window.geometry(f"+{center_x}+{center_y}")

        label = ck.CTkLabel(new_window,width=200,text="تفاصيل الفاتورة" ,text_color="#2e8fe7",font=ck.CTkFont(size=22,weight="bold"))
        label.pack(pady=10)
       
        
        selected_item = self.table.focus()
        values =  self.table.item(selected_item, 'values')

        columns = ("id","name","date","remain","total")
        table = ttk.Treeview(new_window,columns=columns,height=15, selectmode='browse',show='headings')

        table.column("id", anchor="center",width=70,minwidth=70)
        table.column("name", anchor="center",width=280,minwidth=280)
        table.column("date", anchor="center",width=70, minwidth=70)
        table.column("remain", anchor="center",width=90, minwidth=90)
        table.column("total", anchor="center",width=90, minwidth=90)
     
        table.heading('id', text='رمز الصنف')
        table.heading('name', text='اسم الصنف')
        table.heading('date', text='السعر')
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
        
        
        table.pack(pady=20)

        for row in table.get_children():
            table.delete(row)

        sql_query = """
                    SELECT Products.ProductID, Products.ProductName, Products.sell_Price ,OrderDetails.Quantity,OrderDetails.Subtotal
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
        else :
                self.print_button.configure(state="disabled")  

    def on_item_select2(self,event):
        selected_item = self.table2.focus()
        if selected_item:
                self.print_button2.configure(state="normal")
        else :
                self.print_button2.configure(state="disabled")    


    def printAssist(self):
         selected_item = self.table.focus()
         if selected_item:

            values = self.table.item(selected_item, "values")

            sql_query = """
                    SELECT Products.ProductName, Products.sell_Price , OrderDetails.Quantity,Products.Unit , OrderDetails.Subtotal, remainAmount, TotalAmount
                    FROM Orders
                    JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
                    JOIN Products ON OrderDetails.ProductID = Products.ProductID
                    WHERE Orders.OrderID = %s;
                """

            mycursor.execute(sql_query, (values[0],))

            results = mycursor.fetchall()


            table_data = [['اسم الصنف', 'السعر', 'الكمية','وحدة', 'المجموع']]

            if results:
                total_amount = results[0][-1] 
                if not results[0][-2] :
                    remain_amount = 0
                else:     remain_amount = results[0][-2]

            for row in results:
                table_row = [row[0], row[1], row[2], row[3],row[4]]
                table_data.append(table_row)
    
            self.print(table_data,values[1],values[3],(total_amount-remain_amount),f"{values[0]}.pdf")
         
         else:  
             mixer.music.load("sounds/error.mp3")
             mixer.music.play()
             messagebox.showwarning("Warning Message","اختر عنصرًا",icon="warning")


    def print(self,schedule_data,name,total,payed,output_filename):
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




        title = "مبيعات"
        pdf_canvas.setFont("Arabic", 27)
        reshaped_text = arabic_reshaper.reshape(title)
        bidi_text4 = get_display(reshaped_text)
        title_width = pdf_canvas.stringWidth(bidi_text4, "Arabic", 19)
        title_x = (letter[0] - title_width) / 2
        pdf_canvas.drawString(title_x, 670, bidi_text4)



        current_date = datetime.now().strftime("%Y-%m-%d")

        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f"{current_date} ")
        bidi_text5 = get_display(reshaped_text)

        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f" الاسم: {name}")
        bidi_text8 = get_display(reshaped_text)


        pdf_canvas.drawString(50, 630, bidi_text5)
        pdf_canvas.drawString(490, 630, bidi_text8)
                
        cell_height = 20

        x_start = 95
        y_start = 540

        pdf_canvas.setFont("Arabic", 12)

        def draw_table_row(row, y):
            pdf_canvas.setFont("Arabic", 12)

            cell_width = 170
            x = x_start + 0 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[0])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(177 - pdf_canvas.stringWidth(bidi_text, "Arabic", 12) / 2 , y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)

            cell_width = 60
            x = x_start + 2.83 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[1])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 10, y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)


            cell_width = 60
            x = x_start + 3.83 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[2])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 10, y + 5, bidi_text)
            pdf_canvas.setStrokeColor(colors.blue)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(x, y + 21, x + cell_width, y + 21)
            pdf_canvas.rect(x, y + 21, cell_width, -cell_height, stroke=1, fill=0)
            
            cell_width = 60
            x = x_start + 4.83 * cell_width
            reshaped_text = arabic_reshaper.reshape(f"{str(row[3])} ")
            bidi_text = get_display(reshaped_text)
            pdf_canvas.drawString(x + 10, y + 5, bidi_text)
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

        label = "المبلغ الاجمالي بالشيكل :"
        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f"{label} ")
        bidi_text6 = get_display(reshaped_text)
        label_width = pdf_canvas.stringWidth(bidi_text6, "Arabic", 19)
        label_width = (letter[0] - label_width) / 2

        pdf_canvas.drawString(label_width, y_prime-100, f"{total} {bidi_text6} ")

        label = "المبلغ المدفوع :"
        pdf_canvas.setFont("Arabic", 13)
        reshaped_text = arabic_reshaper.reshape(f"{label} ")
        bidi_text7 = get_display(reshaped_text)
        label_width2 = pdf_canvas.stringWidth(bidi_text7, "Arabic", 19)
        label_width2 = (letter[0] - label_width2) / 2

        pdf_canvas.drawString(label_width2-10, y_prime-140, f"{payed} {bidi_text7} ")

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
        self.table.selection_remove(self.table.selection())
        
        for item in self.table.get_children():
            name = self.table.item(item)["values"][1]
            name = name.lower()

            if search_query in name:
                self.table.selection_add(item)
                self.table.see(item)
