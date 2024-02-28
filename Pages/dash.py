from PIL import Image
from tkinter import ttk
from db import mycursor,mydb
from datetime import datetime, timedelta

import tkinter
import tkinter.messagebox
import customtkinter as ck
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


class Dash(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")

        s_frame = ck.CTkFrame(self , fg_color="transparent")

        f2 = ck.CTkFrame(s_frame , fg_color="transparent" )
        f2.grid(row=0,column=0,padx=20)
        l1 = ck.CTkLabel(f2,text="تحذيرات المستودع",text_color="red",corner_radius=20,font=ck.CTkFont(size=20,weight="bold")) 
        l1.pack(pady=5)
        columns = ('id','name', 'cont')

        self.table = ttk.Treeview(f2,
                              columns=columns,
                              height=12,
                              selectmode='browse',
                              show='headings')

        self.table.column("#1", anchor="c", minwidth=100, width=100)
        self.table.column("#2", anchor="c", minwidth=200, width=200)
        self.table.column("#3", anchor="c", minwidth=80, width=80)


        self.table.heading('id', text='رمز الصنف ')
        self.table.heading('name', text='الاسم')
        self.table.heading('cont', text='كمية')

        self.table.bind('<Motion>', 'break')
        self.table.pack(pady=5)

        ###############

        f3 = ck.CTkFrame(s_frame, fg_color="transparent")
        f3.grid(row=0,column=1,padx=20,pady=10)
        l2 = ck.CTkLabel(f3,text="الاكثر مبيعا",corner_radius=20,font=ck.CTkFont(size=20,weight="bold")) 
        l2.pack(pady=5)

        columns2 = ('id','name', 'cont','num')


        self.table2 = ttk.Treeview(f3,
                              columns=columns2,
                              height=12,
                              selectmode='browse',
                              show='headings')

        self.table2.column("#1", anchor="c", minwidth=100, width=100)
        self.table2.column("#2", anchor="c", minwidth=200, width=200)
        self.table2.column("#3", anchor="c", minwidth=180, width=180)
        self.table2.column("#4", anchor="c", minwidth=80, width=80)


        self.table2.heading('id', text='رمز الصنف ')
        self.table2.heading('name', text='الاسم')
        self.table2.heading('cont', text='الكميه في المخزن')
        self.table2.heading('num', text=' عدد ')

        self.table2.bind('<Motion>', 'break')
        self.table2.pack(pady=5)


        ##########

        # f7 = ck.CTkFrame(s_frame , fg_color="#9B9ECE")
        # f7.grid(row=0,column=2,sticky="nsew")
        # f8 = ck.CTkFrame(self , fg_color="black")
        # f8.grid(row=2,column=0,sticky="nsew")
                # create tabview
        self.tabview = ck.CTkTabview(self, width=250)
        self.tabview.pack(fill=ck.BOTH, expand=True)
        self.tabview.add("week")
        self.tabview.add("week cash")
        self.tabview.add("month")
        self.tabview.add("month cash")

        self.tabview.tab("week").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("month").grid_columnconfigure(0, weight=1)
        self.tabview.tab("week cash").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("month cash").grid_columnconfigure(0, weight=1)

        self.f1 = ck.CTkFrame(self.tabview.tab("week") , fg_color="green" )
        self.f1.grid(row=0,column=0,sticky="nsew")
        self.f4 = ck.CTkFrame(self.tabview.tab("month") , fg_color="black")
        self.f4.grid(row=0,column=0,sticky="nsew")
        self.f5 = ck.CTkFrame(self.tabview.tab("week cash") , fg_color="green" )
        self.f5.grid(row=0,column=0,sticky="nsew")
        self.f6 = ck.CTkFrame(self.tabview.tab("month cash") , fg_color="black")
        self.f6.grid(row=0,column=0,sticky="nsew")
        # self.f1.grid(row=0, column=0, padx=20, pady=(20, 10))

        s_frame.pack()
        self.intTable()
        self.intTable2()
        self.month_graph()
        self.week_graph()
        self.month_graph_cash()
        self.week_graph_cash()


    def intTable(self):

            for row in self.table.get_children():
                self.table.delete(row)

            mycursor.execute("SELECT ProductID,ProductName,StockQuantity FROM Products where StockQuantity < 7 ORDER BY ProductID DESC")
            products = mycursor.fetchall()
            self.table.tag_configure('red_tag', background='red')
            for product in products:
                if int(product[2]) < 3 :
                    self.table.insert('', 'end', values=product, tags=('red_tag'))
                else:
                    self.table.insert('', 'end', values=product)
                     
   
   
    def intTable2(self):

            for row in self.table2.get_children():
                self.table2.delete(row)

            mycursor.execute("SELECT ProductID, SUM(Quantity) AS TotalQuantitySold FROM OrderDetails join  orders on OrderDetails.OrderID = orders.OrderID where Orders.OrderDate  GROUP BY ProductID ORDER BY TotalQuantitySold DESC LIMIT 5;")
            products = mycursor.fetchall()
            for product in products:
                mycursor.execute("SELECT ProductName,StockQuantity FROM Products where ProductID=%s",(product[0],))
                info = mycursor.fetchone()
                self.table2.insert('','end',values=(product[0],info[0],info[1],product[1]))

    def month_graph(self):
        current_date = datetime.now()

        date_now = current_date.strftime('%Y-%m-%d')
        current_day = current_date.strftime('%d')
        current_day = int(current_day)
        first_day_of_month = current_date.replace(day=1)


        mycursor.execute("SELECT DATE_FORMAT(OrderDate, '%Y-%m-%d') AS OrderDay, COUNT(OrderID) AS NumberOfOrders FROM Orders WHERE OrderDate >= %s and OrderDate <= %s GROUP BY  OrderDay ORDER BY OrderDay;",(first_day_of_month,date_now))
        result = mycursor.fetchall()
        result_dict = dict(result)

        # Generate a list of dates for the last week
        start_date = datetime.now() - timedelta(days=current_day-1)
        end_date = datetime.now()
        date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        # Extract dates and corresponding number of orders
        dates = [date.strftime('%Y-%m-%d') for date in date_list]

        number_of_orders = [result_dict.get(date, 0) for date in dates]
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        dates = [date.strftime('%d') for date in date_list]
        dates = [day.lstrip('0') for day in dates]



        ax.plot(dates, number_of_orders, marker='o', linestyle='-', color='black' ,linewidth=3)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        

        ax.set_title(" Month orders")
        ax.set_ylabel(" Order Cont")
        ax.set_xlabel("days")
        ax.grid(axis='y')


        canvas = FigureCanvasTkAgg(fig, master=self.f4)
        canvas.draw()
        canvas.get_tk_widget().pack(side=ck.TOP, fill=ck.BOTH, expand=1)
    
    def week_graph(self):
        mycursor.execute("SELECT DATE_FORMAT(OrderDate, '%Y-%m-%d') AS OrderDay,COUNT(OrderID) AS NumberOfOrders FROM  Orders WHERE OrderDate >= CURDATE() - INTERVAL 1 WEEK GROUP BY OrderDay ORDER BY OrderDay;")
        result = mycursor.fetchall()
        result_dict = dict(result)

        # Generate a list of dates for the last week
        start_date = datetime.now() - timedelta(days=6)
        end_date = datetime.now()
        date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        # Extract dates and corresponding number of orders
        dates = [date.strftime('%Y-%m-%d') for date in date_list]

        number_of_orders = [result_dict.get(date, 0) for date in dates]
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        day_names = [date.strftime('%A') for date in date_list]


        # Plot the data on the axes
        ax.plot(day_names, number_of_orders, marker='o', linestyle='-', color='black' ,linewidth=3)
        
        # Customize the plot (optional)
        ax.set_title("Week Order")
        ax.set_xlabel("days")
        ax.set_ylabel("Order Cont")
        ax.grid(axis='y')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        canvas = FigureCanvasTkAgg(fig, master=self.f1)
        canvas.draw()
        canvas.get_tk_widget().pack(side=ck.TOP, fill=ck.BOTH, expand=1)
      
    def month_graph_cash(self):
        current_date = datetime.now()

        date_now = current_date.strftime('%Y-%m-%d')
        current_day = current_date.strftime('%d')
        current_day = int(current_day)
        first_day_of_month = current_date.replace(day=1)


        mycursor.execute("SELECT DATE_FORMAT(OrderDate, '%Y-%m-%d') AS OrderDay, SUM(TotalAmount) AS NumberOfOrders FROM Orders WHERE OrderDate >= %s and OrderDate <= %s GROUP BY  OrderDay ORDER BY OrderDay;",(first_day_of_month,date_now))
        result = mycursor.fetchall()
        result_dict = dict(result)

        # Generate a list of dates for the last week
        start_date = datetime.now() - timedelta(days=current_day-1)
        end_date = datetime.now()
        date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        # Extract dates and corresponding number of orders
        dates = [date.strftime('%Y-%m-%d') for date in date_list]

        number_of_orders = [result_dict.get(date, 0) for date in dates]
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        dates = [date.strftime('%d') for date in date_list]
        dates = [day.lstrip('0') for day in dates]


        ax.plot(dates, number_of_orders, marker='o', linestyle='-', color='black' ,linewidth=3)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))


        ax.set_title(" Month Cash")
        ax.set_ylabel("Total")
        ax.set_xlabel("days")
        ax.grid(axis='y')


        canvas = FigureCanvasTkAgg(fig, master=self.f6)
        canvas.draw()


        
        canvas.get_tk_widget().pack(side=ck.TOP, fill=ck.BOTH, expand=1)
      

         

    def week_graph_cash(self):
        mycursor.execute("SELECT DATE_FORMAT(OrderDate, '%Y-%m-%d') AS OrderDay,SUM(TotalAmount) AS NumberOfOrders FROM  Orders WHERE OrderDate >= CURDATE() - INTERVAL 1 WEEK GROUP BY OrderDay ORDER BY OrderDay;")
        result = mycursor.fetchall()
        result_dict = dict(result)

        # Generate a list of dates for the last week
        start_date = datetime.now() - timedelta(days=6)
        end_date = datetime.now()
        date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        # Extract dates and corresponding number of orders
        dates = [date.strftime('%Y-%m-%d') for date in date_list]

        number_of_orders = [result_dict.get(date, 0) for date in dates]
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        day_names = [date.strftime('%A') for date in date_list]


        # Plot the data on the axes
        ax.plot(day_names, number_of_orders, marker='o', linestyle='-', color='black' ,linewidth=3)
        
        # Customize the plot (optional)
        ax.set_title("Week Cash")
        ax.set_xlabel("days")
        ax.set_ylabel("Total")
        ax.grid(axis='y')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        canvas = FigureCanvasTkAgg(fig, master=self.f5)
        canvas.draw()


        
        canvas.get_tk_widget().pack(side=ck.TOP, fill=ck.BOTH, expand=1)
      

         