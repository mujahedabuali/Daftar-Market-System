import customtkinter
from PIL import Image
import tkinter as tk
from Pages.LoginPage import login_page
from Pages.stats import page3
from Pages.sale import page4
from Pages.store import Store
from Pages.record import Record
from Pages.settingPage import Setting_Page
from Pages.sold import Sold
from Pages.orders import Orders
from Pages.dash import Dash
from Pages.suppliers import Suppliers
from Pages.Xreturn import Return
from Pages.obligations import Obligations



class menuFrame(customtkinter.CTkFrame):
    def __init__(self, parent, page3, page4,page5,sold,dash,order,supliers,Xreturn,oblig,setting,record,logout):
        super().__init__(parent, corner_radius=0)
        self.grid_rowconfigure(12, weight=1)

        self.label = customtkinter.CTkLabel(self,text="المخماسي لمواد البناء ", font=customtkinter.CTkFont(family="DecoType Naskh",size=35, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.storeIMG = customtkinter.CTkImage(Image.open("imags/storehouse.png"),size=(40,40))
        self.statsIMG = customtkinter.CTkImage(Image.open("imags/stats.png"),size=(40,40))
        self.recordIMG = customtkinter.CTkImage(Image.open("imags/notes.png"),size=(40,40))
        self.saleIMG = customtkinter.CTkImage(Image.open("imags/cash.png"),size=(40,40))
        self.soldIMG = customtkinter.CTkImage(Image.open("imags/sold.png"),size=(40,40))
        self.ordersIMG = customtkinter.CTkImage(Image.open("imags/order.png"),size=(40,40))
        self.returnIMG = customtkinter.CTkImage(Image.open("imags/return.png"),size=(40,40))
        self.dashIMG = customtkinter.CTkImage(Image.open("imags/menu.png"),size=(40,40))
        self.supliIMG = customtkinter.CTkImage(Image.open("imags/delivery-courier.png"),size=(40,40))
        self.payIMG = customtkinter.CTkImage(Image.open("imags/debitt.png"),size=(40,40))
        self.setting_image = customtkinter.CTkImage(Image.open("imags/settings.png"),size=(30,30))

        self.dash_button = customtkinter.CTkButton(self, corner_radius=0, height=40,font=customtkinter.CTkFont(size=16, weight="bold"), border_spacing=10, text="رئيسي  ",image=self.dashIMG, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#2e8fe7", "#2e8fe7"), anchor="w",command=dash)
        self.dash_button.grid(row=1, column=0, sticky="ew")

        self.page5_button = customtkinter.CTkButton(self, corner_radius=0, height=40,font=customtkinter.CTkFont(size=16, weight="bold"), border_spacing=10, text="المستودع  ",image=self.storeIMG, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=page5)
        self.page5_button.grid(row=2, column=0, sticky="ew")

        self.page4_button = customtkinter.CTkButton(self, corner_radius=0, height=40, font=customtkinter.CTkFont(size=16, weight="bold"),border_spacing=10, text="البيع  ", image=self.saleIMG, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=page4)
        self.page4_button.grid(row=3, column=0, sticky="ew")


        self.sold_button = customtkinter.CTkButton(self, corner_radius=0, height=40, font=customtkinter.CTkFont(size=16, weight="bold"),border_spacing=10, text="مبيعات  ", image=self.soldIMG, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=sold)
        self.sold_button.grid(row=4, column=0, sticky="ew")

        self.record_button = customtkinter.CTkButton(self, corner_radius=0, height=40, font=customtkinter.CTkFont(size=16, weight="bold"),border_spacing=10, text="السجل  ", image=self.recordIMG, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=record)
        self.record_button.grid(row=5, column=0, sticky="ew")

        self.orders_button = customtkinter.CTkButton(self, corner_radius=0, height=40, font=customtkinter.CTkFont(size=16, weight="bold"),border_spacing=10, text="طلبيات  ", image=self.ordersIMG, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=order)
        self.orders_button.grid(row=6, column=0, sticky="ew")

        self.return_button = customtkinter.CTkButton(self, corner_radius=0, height=40, font=customtkinter.CTkFont(size=16, weight="bold"),border_spacing=10, text="ارجاعيات  ", image=self.returnIMG, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=Xreturn)
        self.return_button.grid(row=7, column=0, sticky="ew")

        self.oblig_button = customtkinter.CTkButton(self, corner_radius=0, height=40, font=customtkinter.CTkFont(size=16, weight="bold"),border_spacing=10, text="التزامات  ", image=self.payIMG, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=oblig)
        self.oblig_button.grid(row=8, column=0, sticky="ew")

        self.suppliers_button = customtkinter.CTkButton(self, corner_radius=0, height=40, font=customtkinter.CTkFont(size=16, weight="bold"),border_spacing=10, text="المزودين  ", image=self.supliIMG, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=supliers)
        self.suppliers_button.grid(row=9, column=0, sticky="ew")

        self.page3_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,font=customtkinter.CTkFont(size=16, weight="bold"),text="حسابات", image=self.statsIMG, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=page3)
        self.page3_button.grid(row=10, column=0, sticky="ew")

        self.setting_button = customtkinter.CTkButton(self, corner_radius=0, height=40,font=customtkinter.CTkFont(size=16, weight="bold"), border_spacing=10, text="الاعدادات",image=self.setting_image, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=setting)
        self.setting_button.grid(row=11, column=0, sticky="ew")

        self.logout_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Log out       .Made By J-Group", fg_color="transparent", text_color=("red", "red"), hover_color=("gray70", "gray30"), anchor="w",command=logout)
        self.logout_button.grid(row=13, column=0, sticky="ew")

#Drive class
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("System")

        self.title("Daftar Application")
        self.geometry("1500x900")
        self.iconphoto(True, tk.PhotoImage(file='imags/logo_muj.png'))
        center_x = int(170)
        center_y = int(76)
        self.geometry(f"+{center_x}+{center_y}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.loginPage=login_page(self,self.login)
        self.loginPage.grid(row=0, column=1, sticky="nsew")

        self.navigation_frame = menuFrame(self,self.page3_event, self.page4_event,self.page5_event,self.sold_event,self.dash_event,self.orders_event,self.supli_event,self.return_event,self.oblig_event,self.setting_event,self.record_event,self.logout)
    

    def select_frame_by_name(self, name):
        self.navigation_frame.page3_button.configure(fg_color=("gray75", "gray25") if name == "page3" else "transparent")
        self.navigation_frame.page4_button.configure(fg_color=("gray75", "gray25") if name == "salePage" else "transparent")
        self.navigation_frame.page5_button.configure(fg_color=("gray75", "gray25") if name == "storePage" else "transparent")
        self.navigation_frame.setting_button.configure(fg_color=("gray75", "gray25") if name == "Setting" else "transparent")
        self.navigation_frame.sold_button.configure(fg_color=("gray75", "gray25") if name == "soldPage" else "transparent")
        self.navigation_frame.record_button.configure(fg_color=("gray75", "gray25") if name == "record" else "transparent")
        self.navigation_frame.dash_button.configure(fg_color=("#2e8fe7", "#2e8fe7") if name == "dash" else "transparent")
        self.navigation_frame.orders_button.configure(fg_color=("gray75", "gray25") if name == "ordersPage" else "transparent")
        self.navigation_frame.return_button.configure(fg_color=("gray75", "gray25") if name == "returnPage" else "transparent")
        self.navigation_frame.suppliers_button.configure(fg_color=("gray75", "gray25") if name == "supliPage" else "transparent")
        self.navigation_frame.oblig_button.configure(fg_color=("gray75", "gray25") if name == "obligPage" else "transparent")


        self.page3.grid_remove()
        self.salePage.grid_remove()
        self.storePage.grid_remove()
        self.recordPage.grid_remove()
        self.sett_Page.grid_remove()
        self.soldPage.grid_remove()
        self.oredersPage.grid_remove()
        self.dashPage.grid_remove()
        self.returnPage.grid_remove()
        self.obligPage.grid_forget()
        self.spliPage.grid_forget()

        if name == "page3":
            self.page3.grid(row=0, column=1, sticky="nsew")

        elif name == "salePage":
            self.salePage.grid(row=0, column=1, sticky="nsew")
      
        elif name == "storePage":
            self.storePage.grid(row=0, column=1, sticky="nsew")

        elif name == "soldPage":
            self.soldPage.grid(row=0, column=1, sticky="nsew")    

        elif name == "record":
            self.recordPage.grid(row=0, column=1, sticky="nsew") 

        elif name == "ordersPage":
            self.oredersPage.grid(row=0, column=1, sticky="nsew")

        elif name == "supliPage":
            self.spliPage.grid(row=0, column=1, sticky="nsew")    

        elif name == "dash":
            self.dashPage.grid(row=0, column=1, sticky="nsew")  

        elif name == "returnPage":
            self.returnPage.grid(row=0, column=1, sticky="nsew")    

        elif name == "obligPage":
            self.obligPage.grid(row=0, column=1, sticky="nsew")            

        elif name == "Setting":
            self.sett_Page.grid(row=0, column=1, sticky="nsew")
  
        self.update_idletasks()         


    def login(self):
       self.navigation_frame.grid(row=0, column=0, sticky="nsew")
       self.page3 = page3(self,self.loginPage)
       self.salePage = page4(self,self.loginPage)
       self.storePage = Store(self,self.loginPage)
       self.sett_Page= Setting_Page(self,self.loginPage)
       self.recordPage=Record(self,self.loginPage)
       self.soldPage=Sold(self,self.loginPage)
       self.oredersPage=Orders(self,self.loginPage)
       self.dashPage=Dash(self,self.loginPage)
       self.spliPage=Suppliers(self,self.loginPage)
       self.returnPage=Return(self,self.loginPage)
       self.obligPage=Obligations(self,self.loginPage)
       self.select_frame_by_name("dash")
       self.loginPage.grid_forget()

    def logout(self):
       self.navigation_frame.grid_forget()
       self.salePage.grid_forget()
       self.spliPage.grid_forget()
       self.recordPage.grid_forget()
       self.page3.grid_forget()
       self.returnPage.grid_forget()
       self.obligPage.grid_forget()
       self.storePage.grid_forget()
       self.dashPage.grid_forget()
       self.oredersPage.grid_forget()
       self.sett_Page.grid_forget()
       self.loginPage.grid(row=0, column=1, sticky="nsew")
       self.update_idletasks()         

    def page3_event(self):
        self.select_frame_by_name("page3")

    def page4_event(self):
        self.salePage.clear()
        self.salePage.intTable2()
        self.select_frame_by_name("salePage")    

    def page5_event(self):
        self.storePage.intTable()
        self.select_frame_by_name("storePage") 

    def record_event(self):
        self.recordPage.intTable()
        self.select_frame_by_name("record")        
   
    def sold_event(self):
        self.soldPage.intTable()
        self.select_frame_by_name("soldPage")

    def orders_event(self):
        self.oredersPage.intTable()
        self.select_frame_by_name("ordersPage")    

    def supli_event(self):
        self.spliPage.intTable()
        self.select_frame_by_name("supliPage")  

    def main_event(self):
        self.select_frame_by_name("mainPage")      

    def return_event(self):
        self.select_frame_by_name("returnPage")  

    def setting_event(self):
        self.select_frame_by_name("Setting")    
    
    def dash_event(self):
        self.select_frame_by_name("dash") 

    def oblig_event(self):
        self.select_frame_by_name("obligPage")      




if __name__ == "__main__":
    app = App()
    app.mainloop()
