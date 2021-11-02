from Reporting import ReportingClass
from supplier import supplierClass
from tkinter import*
from tkinter import messagebox
# from PIL import Image,ImageTk# pip install pillow
import sqlite3
import time
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

# import class of different pages

from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from products import productsClass
from sales import salesClass
new_win=''

class IMS:
    global new_win
    def __init__(self,root):
        
        self.root=root
        self.root.geometry("1500x700+0+0")
        self.root.title("Inventry Management System | Developed by Engineer Qurban Ali Gujjar")
        self.root.iconbitmap("images/myicon.ico")
        self.bg_color="#ECF0F5"
        self.menuColor='#222D32'
        # self.bg_color="#03fcf4"
        self.root.config(bg=self.bg_color)
        #=====title=====
        self.image = Image.open('images/logo2.png')
        self.image = self.image.resize((70,70), Image.ANTIALIAS)
        self.icon_title= ImageTk.PhotoImage(self.image)
        
        title=Label(self.root,text="Inventry Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx="20").place(x=0,y=0,relwidth=1,height=70)
        #========btn_logout
        btn_logout=Button(self.root,text="logout",command=self.log_out,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1100,y=10,width=150,height=50)
        
        #=========Clock========
        self.lbl_clock=Label(self.root,text="Welcome to Inventry Management System\t\t Date: DD-MM-YYYY \t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        #======left Men=====
        self.MenuLogo=Image.open("images/menu_im.jpg")
        self.MenuLogo=self.MenuLogo.resize((200,150),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE)
        LeftMenu.place(x=0,y=102,width=200,height=565)
        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)
        
        # self.icon_side=PhotoImage(file="images/side_im.png")
        
        
        # drawing = svg2rlg('images/icons/dashboard.svg')
        # renderPM.drawToFile(drawing, 'images/icons/ice.png', fmt='PNG')
        self.icon_side= Image.open('images/icons/3.png')
        self.icon_side = self.icon_side.resize((25,25), Image.ANTIALIAS)
        self.icon_side= ImageTk.PhotoImage(self.icon_side)
        
    #--------------supplier icons-------------------
        self.icon_supplier = Image.open('images/icons/product_icon.png')
        self.icon_supplier = self.icon_supplier.resize((25,25), Image.ANTIALIAS)
        self.icon_supplier = ImageTk.PhotoImage(self.icon_supplier)
        
        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",15),bg="#009688").pack(side=TOP,fill=X)
        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg=self.menuColor,fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_supplier,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg=self.menuColor,fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg=self.menuColor,bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_products=Button(LeftMenu,text="Products",command=self.products,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg=self.menuColor,bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg=self.menuColor,bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",command=self.root.quit, image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg=self.menuColor,bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_Reporting=Button(LeftMenu,text="Reports",command=self.Reporting,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg=self.menuColor,bd=3,cursor="hand2").pack(side=TOP,fill=X)
        #==============
        
        def change_back(e):
            self.icon_Emp = Image.open('images/icons/product_icon1.png')
            self.icon_Emp = self.icon_Emp.resize((125,125), Image.ANTIALIAS)
            self.icon_Emp = ImageTk.PhotoImage(self.icon_Emp)
            self.lbl_employee.config(image=self.icon_Emp)
            
        def change(e):
            self.icon_Emp = Image.open('images/icons/product_icon1.png')
            self.icon_Emp = self.icon_Emp.resize((130,130), Image.ANTIALIAS)
            self.icon_Emp = ImageTk.PhotoImage(self.icon_Emp)
            self.lbl_employee.config(image=self.icon_Emp)    
            
        self.icon_Emp = Image.open('images/icons/product_icon1.png')
        self.icon_Emp = self.icon_Emp.resize((125,125), Image.ANTIALIAS)
        self.icon_Emp = ImageTk.PhotoImage(self.icon_Emp)
        # image=self.icon_supplier
        #=============Content=====================
        self.Employee_frame=Frame(self.root,bd=2,relief=RIDGE,bg="#ff5722")
        self.Employee_frame.place(x=300,y=120,height=150,width=300)
        self.lbl_employee=Label(self.Employee_frame,image=self.icon_Emp,bg="#ff5722",fg="white")
        self.lbl_employee.pack(side=LEFT)
        self.txt_employee=Label(self.Employee_frame,text="Total Employee \n[ 0 ]",bg="#ff5722",fg="white",font=("goudy old style",15,"bold",))
        self.txt_employee.pack(side=LEFT)
        self.Employee_frame.bind("<Enter>",change)
        self.Employee_frame.bind("<Leave>",change_back)
        
        # self.lbl_employee=Label(self.root,text="Total Employee \n[ 0 ]",bg="#33bbf9",fg="white",font=("goudy old style",20,"bold",))
        # self.lbl_employee.place(x=300,y=120,height=150,width=300)
        
        # self.lbl_employee=Label(self.root,image=self.icon_supplier)
        # self.lbl_employee.place(x=350,y=150,height=30,width=30)

        
        self.lbl_supplier=Label(self.root,text="Total Supplier \n[ 0 ]",bg="#ff5722",fg="white",font=("goudy old style",20,"bold",))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)
        self.lbl_supp_txt=Label(self.root,text="Total Supplier \n[ 0 ]",bg="#ff5722",fg="white",font=("goudy old style",10,"bold",))
        self.lbl_supp_txt.place(x=650,y=120,height=50,width=150)
        
        self.lbl_category=Label(self.root,text="Category \n[ 0 ]",bg="#009668",fg="white",font=("goudy old style",20,"bold",))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)
        
        self.lbl_sales=Label(self.root,text="Total Sale \n[ 0 ]",bg="#00ff40",fg="white",font=("goudy old style",20,"bold",))
        self.lbl_sales.place(x=300,y=300,height=150,width=300)
        
        self.lbl_products=Label(self.root,text="Total Products \n[ 0 ]",bg="#ff0040",fg="white",font=("goudy old style",20,"bold",))
        self.lbl_products.place(x=650,y=300,height=150,width=300)
        #=====Footer=======
        lbl_footer=Label(self.root,text="IMS-Inventory Managemant System | Developed by Engineer Qurban ali Gujjar \n For any technical Issue Contact:0347xxxxx37 ",font=("times new roman",12),bg="#4d636d").pack(side=BOTTOM,fill=X)
        self.contant_update()
        
        #initializing window frame for dashboard""
        self.new_win_emp=Toplevel(self.root)
        self.new_win_sup=Toplevel(self.root)
        self.new_win_cat=Toplevel(self.root)
        self.new_win_pro=Toplevel(self.root)
        self.new_win_sale=Toplevel(self.root)
        self.new_win_Reporting=Toplevel(self.root)
        self.destroy_fun()
        # self.fd=""
        
        # self.argument=0
     #=================================================================================
    def employee(self):
        self.destroy_fun()
        self.new_win_emp=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win_emp)
                
    def supplier(self):
        self.destroy_fun()  
        self.new_win_sup=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win_sup) 

    def category(self):
        self.destroy_fun()  
        self.new_win_cat=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win_cat) 
        
       
    def products(self):
        self.destroy_fun()  
        self.new_win_pro=Toplevel(self.root)
        self.new_obj=productsClass(self.new_win_pro) 
        
    def sales(self):
        self.destroy_fun()  
        self.new_win_sale=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win_sale) 
        # destroy function 
    def Reporting(self):
        self.destroy_fun()
        self.new_win_emp=Toplevel(self.root)
        self.new_obj=ReportingClass(self.new_win_emp)
                        
    def destroy_fun(self):
        self.new_win_emp.destroy()
        self.new_win_sup.destroy()
        self.new_win_cat.destroy()
        self.new_win_pro.destroy()
        self.new_win_sale.destroy()
        self.new_win_Reporting.destroy()
                       
        # thisdict[0]
        # os.close(fd)
    # =========Dashboard Update function=================
        
    def contant_update(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from products")
            rows=cur.fetchall()
            self.lbl_products.config(text=f"Total Products \n{str(len(rows))}")
            cur.execute("Select * from employee")
            rows=cur.fetchall()
            self.txt_employee.config(text=f"Total Employee \n{str(len(rows))}")
            cur.execute("Select * from category")
            rows=cur.fetchall()
            self.lbl_category.config(text=f"Total Categorys \n{str(len(rows))}")
            cur.execute("Select * from supplier")
            rows=cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier \n{str(len(rows))}")
            self.lbl_sales.config(text=f"Total Sales \n{str(len(os.listdir('bill')))}")   
            time_=time.strftime("%H:%M:%S")
            date_=time.strftime("%d/%m/%y")
            self.lbl_clock.config(text=f"Welcome to Inventry Management System\t\t Date: {str(date_)} \t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.contant_update)
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to {str(ex)}",parent=self.root)            
    def log_out(self):
        self.root.destroy()
        os.system("C:/ProgramData/Anaconda3/python.exe d:/project1/login.py")
    
        
if __name__=="__main__":   
    root=Tk()
    obj=IMS(root)
    root.mainloop()