from PIL import Image
from tkinter import ttk
from db import mycursor,mydb
<<<<<<< HEAD
from datetime import datetime, timedelta

import tkinter
import tkinter.messagebox
import customtkinter as ck
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

=======
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkcalendar import Calendar
from datetime import datetime, timedelta
>>>>>>> Muj/main

class Stat(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
<<<<<<< HEAD
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
=======
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
        
>>>>>>> Muj/main

        self.table.heading('name', text='العنصر')
        self.table.heading('price', text='المبلغ')
        

<<<<<<< HEAD
        self.entry = ck.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = ck.CTkButton(master=self,text="تصفير الخزنة اليومية", fg_color="red", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = ck.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = ck.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = ck.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = ck.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = ck.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = ck.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # # create radiobutton frame
        # self.radiobutton_frame = ck.CTkFrame(self)
        # self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # self.radio_var = tkinter.IntVar(value=0)
        # self.label_radio_group = ck.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        # self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        # self.radio_button_1 = ck.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        # self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        # self.radio_button_2 = ck.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        # self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        # self.radio_button_3 = ck.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        # self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = ck.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = ck.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = ck.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = ck.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = ck.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = ck.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = ck.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # create scrollable frame
        self.scrollable_frame = ck.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = ck.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # # create checkbox and switch frame
        # self.checkbox_slider_frame = ck.CTkFrame(self)
        # self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # self.checkbox_1 = ck.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        # self.checkbox_2 = ck.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        # self.checkbox_3 = ck.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        # self.checkbox_3.configure(state="disabled")
        # self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        # self.radio_button_3.configure(state="disabled")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

    def open_input_dialog_event(self):
        dialog = ck.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ck.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ck.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
=======
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





        
>>>>>>> Muj/main
