from tkinter import*
from PIL import Image,ImageTk # pip install pillow
from tkinter import ttk,messagebox
import pandas as pd
import sqlite3
import os
import tempfile
import cv2
from pyzbar.pyzbar import decode
from barcode import Gs1_128
from barcode.writer import ImageWriter
from returnProduct1 import*
import time
class billingClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1500x700+0+0")
        self.root.title("Inventry Management System | Developed by Qurban Ali")
        self.root.config(bg="white")
        self.cart_list=[]
        self.sales_list=[]
        self.chk_print=0
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
        
#==================================================================================================================================
        #============= All Product frame
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                        background='silver',
                        forground='black',
                        rowheight=45,
                        font=("goudy old style",20,'bold'),
                        fieldbackground='silver')
        style.map('Treeview',
                  background=[('selected','green')])

        #======Product Variables 
        self.var_Search=StringVar()
        
        product_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_frame.place(x=1,y=110,width=400,height=580)
        title=Label(product_frame,text="All Products",font=("goudy old style",20,"bold"),bg="black",fg="white").pack(side=TOP,fill=X)
        
        Search_product_frane=Frame(product_frame,bd=2,relief=GROOVE,bg="white")
        Search_product_frane.place(x=1,y=40,width=395,height=150)
        
        search_fram=Frame(Search_product_frane,bd=0,relief=RIDGE,bg="white")
        search_fram.place(x=1,y=5,width=390,height=90)
        lbl_Product=Label(search_fram,text="Search Product | By Name",font=("goudy old style",10,"bold"),bg="white").place(x=5,y=5)
        btn_Show_All=Button(search_fram,text="Show All",command=self.show,font=("goudy old style",10,"bold"),bg="lightgray",cursor="hand2").place(x=275,y=5,width=110,height=30)
        btn_Get_Barcode=Button(search_fram,text="Get BarCode",command=self.My_invoice,font=("goudy old style",10,"bold"),bg="lightgray",cursor="hand2").place(x=175,y=5,width=110,height=30)
        
        lbl_Product_Name=Label(search_fram,text="Product Name.",font=("goudy old style",10,"bold"),bg="white").place(x=5,y=40)
        txt_search=Entry(search_fram,textvariable=self.var_Search,font=("goudy old style",10),bg="lightyellow").place(x=110,y=40,width=150,height=30)
        btn_search=Button(search_fram,text="Search",command=self.search ,font=("goudy old style",10,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=275,y=40,width=110,height=30)
        #=================Details frame--====================
        product_Detail_frane=Frame(product_frame,bd=2,relief=GROOVE,bg="white")
        product_Detail_frane.place(x=1,y=130,width=395,height=440)
        title=Label(product_Detail_frane,text="Note:'Enter 0 QTY to remove Product Cart'",font=("goudy old style",15),bg="white",fg="red").pack(side=BOTTOM,fill=X)
        
        #=========== Category Details-====
        sup_frame=Frame(product_Detail_frane,bd=3,relief=RIDGE)
        sup_frame.place(x=1,y=1,width=390,height=405)
        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)
        self.ProductsTable=ttk.Treeview(sup_frame,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrolly.set)
       
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductsTable.xview)
        scrolly.config(command=self.ProductsTable.yview)
       #====headings ===========================
        self.ProductsTable.heading("pid",text="P ID")
        self.ProductsTable.heading("name",text="Name")
        self.ProductsTable.heading("price",text="Price")
        self.ProductsTable.heading("qty",text="QTY")
        self.ProductsTable.heading("status",text="Status")
        #========colom width ====================
        self.ProductsTable.column("pid",width=10)
        self.ProductsTable.column("name",width=40)
        self.ProductsTable.column("price",width=40)
        self.ProductsTable.column("qty",width=40)
        self.ProductsTable.column("status",width=40)
        self.ProductsTable["show"]="headings"
        self.ProductsTable.pack(fill=BOTH,expand=1)
        self.ProductsTable.bind("<ButtonRelease-1>",self.get_data)  
        
#================== Customer Details frame
        #============customer Variables======
        self.var_C_name=StringVar()
        self.var_C_no=StringVar()
        self.C_color="#2196f3"
        self.C_B_Size=8
        self.var_P_name=StringVar()
        self.var_P_price=StringVar()
        self.var_P_id=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()
        self.var_stock=StringVar()
        self.sale_Return=StringVar()
        self.good_Bad=StringVar()
        
        
        customer_fram=Frame(self.root,bd=1,relief=RIDGE,bg="white")
        customer_fram.place(x=405,y=110,width=540,height=580)
        
        customer_Detail_fram=Frame(customer_fram,bd=1,relief=RIDGE,bg="white")
        customer_Detail_fram.place(x=1,y=1,width=538,height=78)
        title=Label(customer_Detail_fram,text="Customer Details",font=("goudy old style",20,"bold"),bg="gray",fg="black").pack(side=TOP,fill=X)
        lbl_invoice=Label(customer_Detail_fram,text="Customer Name.",font=("goudy old style",15,"bold"),bg="white").place(x=1,y=40)
        txt_C_name=Entry(customer_Detail_fram,textvariable=self.var_C_name,font=("goudy old style",15),bg="lightyellow").place(x=145,y=40,width=140,height=30)
        lbl_invoice=Label(customer_Detail_fram,text="Contact No.",font=("goudy old style",15,"bold"),bg="white").place(x=288,y=40)
        txt_C_no=Entry(customer_Detail_fram,textvariable=self.var_C_no,font=("goudy old style",15),bg="lightyellow").place(x=392,y=40,width=140,height=30)
        
        Cust_Pro_frame=Frame(customer_fram,bd=2,relief=GROOVE,bg="white")
        Cust_Pro_frame.place(x=1,y=90,width=535,height=320)
        
#==============Calculater ==========
        self.btn_size=60
        self.var_Cal_input=StringVar()
        # self.lbl_Instock
        
        Calculater_frame=Frame(Cust_Pro_frame,bd=5,relief=GROOVE,bg="white")
        Calculater_frame.place(x=2,y=2,width=258,height=313)
        
        row1_frame=Frame(Calculater_frame,bd=15,relief=GROOVE,bg="red")
        row1_frame.place(x=3,y=1,width=240,height=58)
        self.Cal_window=Entry(row1_frame,textvariable=self.var_Cal_input,font=("goudy old style",15),bg="lightyellow",state="readonly",justify=RIGHT).place(x=0,y=0,width=210,height=30)
        
         # must be n, ne, e, se, s, sw, w, nw, or center
        row2_frame=Frame(Calculater_frame,bd=0,relief="solid",bg="white")
        row2_frame.place(x=3,y=60,width=243,height=60)
        btn_7=Button(row2_frame,text="7",font=("goudy old style",15,"bold"),command=lambda:self.get_input(7),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=1,y=1,width=self.btn_size,height=self.btn_size)
        btn_8=Button(row2_frame,text="8",font=("goudy old style",15,"bold"),command=lambda:self.get_input(8),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=60,y=1,width=self.btn_size,height=self.btn_size)
        btn_9=Button(row2_frame,text="9",font=("goudy old style",15,"bold"),command=lambda:self.get_input(9),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=120,y=1,width=self.btn_size,height=self.btn_size)
        btn_Add=Button(row2_frame,text="+",font=("goudy old style",15,"bold"),command=lambda:self.get_input("+"),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=180,y=1,width=self.btn_size,height=self.btn_size)
        
        row3_frame=Frame(Calculater_frame,bd=0,relief="solid",bg="white")
        row3_frame.place(x=3,y=120,width=243,height=60)
        btn_6=Button(row3_frame,text="6",font=("goudy old style",15,"bold"),command=lambda:self.get_input(6),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=1,y=1,width=self.btn_size,height=self.btn_size)
        btn_5=Button(row3_frame,text="5",font=("goudy old style",15,"bold"),command=lambda:self.get_input(5),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=60,y=1,width=self.btn_size,height=self.btn_size)
        btn_4=Button(row3_frame,text="4",font=("goudy old style",15,"bold"),command=lambda:self.get_input(4),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=120,y=1,width=self.btn_size,height=self.btn_size)
        btn_Sub=Button(row3_frame,text="-",font=("goudy old style",15,"bold"),command=lambda:self.get_input("-"),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=180,width=self.btn_size,height=self.btn_size)
        
        row4_frame=Frame(Calculater_frame,bd=0,relief="solid",bg="white")
        row4_frame.place(x=3,y=180,width=243,height=60)
        btn_3=Button(row4_frame,text="3",font=("goudy old style",15,"bold"),command=lambda:self.get_input(3),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=1,y=1,width=self.btn_size,height=self.btn_size)
        btn_2=Button(row4_frame,text="2",font=("goudy old style",15,"bold"),command=lambda:self.get_input(2),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=60,y=1,width=self.btn_size,height=self.btn_size)
        btn_1=Button(row4_frame,text="1",font=("goudy old style",15,"bold"),command=lambda:self.get_input(1),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=120,y=1,width=self.btn_size,height=self.btn_size)
        btn_Mul=Button(row4_frame,text="*",font=("goudy old style",15,"bold"),command=lambda:self.get_input("*"),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=180,y=1,width=self.btn_size,height=self.btn_size)
        
        row5_frame=Frame(Calculater_frame,bd=0,relief="solid",bg="white")
        row5_frame.place(x=3,y=240,width=243,height=60)
        btn_0=Button(row5_frame,text="0",font=("goudy old style",15,"bold"),command=lambda:self.get_input(0),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=1,y=1,width=self.btn_size,height=self.btn_size)
        btn_Clear=Button(row5_frame,text="C",font=("goudy old style",15,"bold"),command=self.Clear,bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=60,y=1,width=self.btn_size,height=self.btn_size)
        btn_Equal=Button(row5_frame,text="=",font=("goudy old style",15,"bold"),command=self.Perform_Cal,bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=120,y=1,width=self.btn_size,height=self.btn_size)
        btn_Div=Button(row5_frame,text="/",font=("goudy old style",15,"bold"),command=lambda:self.get_input("/"),bg=self.C_color,bd=self.C_B_Size,relief=GROOVE,fg="white",cursor="hand2").place(x=180,y=1,width=self.btn_size,height=self.btn_size)
        
        #=================Pre Recipet=======
        Cart_frame=Frame(Cust_Pro_frame,bd=2,relief=GROOVE,bg="white")
        Cart_frame.place(x=265,y=1,width=265,height=313)
        self.title_cart=Label(Cart_frame,text="Cart\tTotal Products [0]",font=("goudy old style",16),bg="gray",fg="black")
        self.title_cart.pack(side=TOP,fill=X)
        #=========== Category Details-====
        C_P_frame=Frame(Cart_frame,bd=3,relief=RIDGE)
        C_P_frame.place(x=1,y=33,width=260,height=275)
        scrolly=Scrollbar(C_P_frame,orient=VERTICAL)
        scrollx=Scrollbar(C_P_frame,orient=HORIZONTAL)
        self.C_P_Table=ttk.Treeview(C_P_frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.C_P_Table.xview)
        scrolly.config(command=self.C_P_Table.yview)
       #====headings ===========================
        self.C_P_Table.heading("pid",text="P ID")
        self.C_P_Table.heading("name",text="Name")
        self.C_P_Table.heading("price",text="Price")
        self.C_P_Table.heading("qty",text="QTY")
    
        #========colom width ====================
        self.C_P_Table.column("pid",width=30)
        self.C_P_Table.column("name",width=50)
        self.C_P_Table.column("price",width=50)
        self.C_P_Table.column("qty",width=50)
        self.C_P_Table["show"]="headings"
        self.C_P_Table.pack(fill=BOTH,expand=1)
        self.C_P_Table.bind("<ButtonRelease-1>",self.get_data_cart)
        
        #================In stock============
        Instock_frame=Frame(customer_fram,bd=5,relief=GROOVE,bg="white")
        Instock_frame.place(x=2,y=422,width=538,height=115)
        lbl_invoice=Label(Instock_frame,text="Product Name",font=("goudy old style",15,"bold"),bg="white").place(x=1,y=1)
        txt_C_name=Entry(Instock_frame,textvariable=self.var_P_name,state="readonly",font=("goudy old style",15),bg="lightyellow").place(x=1,y=30,width=160,height=30)
        lbl_invoice=Label(Instock_frame,text="P/QTY.",font=("goudy old style",15,"bold"),bg="white").place(x=180,y=1)
        txt_C_name=Entry(Instock_frame,textvariable=self.var_P_price,font=("goudy old style",15),bg="lightyellow").place(x=180,y=30,width=80,height=30)
        lbl_invoice=Label(Instock_frame,text="QTY.",font=("goudy old style",15,"bold"),bg="white").place(x=270,y=1)
        txt_qty=Entry(Instock_frame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow").place(x=270,y=30,width=80,height=30)
        self.cmb_Sale_Return=ttk.Combobox(Instock_frame,textvariable=self.sale_Return,values=("Sale","Return"),state="readonly",justify=CENTER,font=("goudy old style",15))
        self.cmb_Sale_Return.place(x=360,y=30,width=80)
        self.cmb_Sale_Return.current(0)
        self.cmb_Return_type=ttk.Combobox(Instock_frame,textvariable=self.good_Bad,values=("Good","Bad"),state="readonly",justify=CENTER,font=("goudy old style",15))
        self.cmb_Return_type.place(x=445,y=30,width=80)
        self.cmb_Return_type.current(0)
        # txt_qty=Entry(Instock_frame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow").place(x=280,y=30,width=80,height=30)
        self.lbl_Instock=Label(Instock_frame,text="In Stock.",font=("goudy old style",15,"bold"),bg="white")
        self.lbl_Instock.place(x=1,y=70)
        btn_clear_cart=Button(Instock_frame,command=self.Clear_cart,text="Clear",font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=70,width=110,height=30)
        btn_search=Button(Instock_frame,text="Add| Update Cart", command=self.add_update_cart ,font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=330,y=70,width=170,height=30)
        
        #====================billing frame
        C_billing_fram=Frame(self.root,bd=1,relief=RIDGE,bg="white")
        C_billing_fram.place(x=950,y=110,width=400,height=570) 
        title=Label(C_billing_fram,text="Customer Billing Area",font=("goudy old style",20,"bold"),bg="red",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(C_billing_fram,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.txt_bill_area=Text(C_billing_fram,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        Print_bill_fram=Frame(C_billing_fram,bd=1,relief=RIDGE,bg="white")
        Print_bill_fram.place(x=0,y=400,width=400,height=150) 
        self.lbl_Bill_amount=Label(Print_bill_fram,text="Bill Amount \n 0",font=("goudy old style",15,"bold"),bg="#2196f3",bd=5,relief=GROOVE,fg="white",cursor="hand2")
        self.lbl_Bill_amount.place(x=0,y=0,width=130,height=70)
        self.lbl_Discount=Label(Print_bill_fram,text="Discount \n 5%",font=("goudy old style",15,"bold"),bg="#2196f3",bd=5,relief=GROOVE,fg="white",cursor="hand2")
        self.lbl_Discount.place(x=130,y=0,width=130,height=70)
        self.lbl_Net_pay=Label(Print_bill_fram,text="Net Pay \n 0",font=("goudy old style",15,"bold"),bg="#2196f3",bd=5,relief=GROOVE,fg="white",cursor="hand2")
        self.lbl_Net_pay.place(x=260,y=0,width=130,height=70)
        btn_Print=Button(Print_bill_fram,command=self.print_bill,text="Print",font=("goudy old style",15,"bold"),bg="#2196f3",bd=5,relief=GROOVE,fg="white",cursor="hand2").place(x=0,y=70,width=130,height=70)
        btn_Clear_All=Button(Print_bill_fram,command=self.Clear_All,text="Clear All",font=("goudy old style",15,"bold"),bg="#2196f3",bd=5,relief=GROOVE,fg="white",cursor="hand2").place(x=130,y=70,width=130,height=70)
        btn_Generate=Button(Print_bill_fram,command=self.bill_Generate,text="Generate \n Save Bill",font=("goudy old style",15,"bold"),bd=5,relief=GROOVE,bg="#2196f3",fg="white",cursor="hand2").place(x=260,y=70,width=130,height=70)
        
        #=================Footer ========================
        title=Label(self.root,text="IMS-Inventory Managemant System | Developed by Engineer Qurban ali Gujjar \n For any technical Issue Contact:0347xxxxx37 ",justify=CENTER,font=("times new roman",12),bg="#4d636d").pack(side=BOTTOM,fill=X)
        # lbl_footer=Label(self.root,text="IMS-Inventory Managemant System | Developed by Engineer Qurban ali Gujjar \n For any technical Issue Contact:0347xxxxx37 ",font=("times new roman",12),bg="#4d636d").pack(side=BOTTOM,fill=X)
        self.show()
        self.Update_date_time()
    def log_out(self):
        self.root.destroy()
        os.system("C:/ProgramData/Anaconda3/python.exe d:/project1/login.py")
    
#-=====================================All functions------==================================
    def My_invoice(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        self.cmb_Sale_Return.current(1)
        try:
            if self.var_Search.get()=="":
                messagebox.showerror("Error","Invoce No Must be Required",parent=self.root)
            else:
                cur.execute("Select productCode,name,Tprice,qty from salesTable where InvoiceNo=?",(self.var_Search.get(),))
                rows=cur.fetchall()
                if rows==None:
                    messagebox.showerror("Error","ther is No Invoice find for this match",parent=self.root)   
                    # print(self.var_sup_invoice_no.get()) 
                else:
                    
                    self.ProductsTable.delete(*self.ProductsTable.get_children())
                    
                    for row in rows:
                        self.ProductsTable.insert('',END,values=row)
                    
        except Exception as ex:
               messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
        
            #======functon for Calculater=======
    def get_input(self,num):
        xnum=self.var_Cal_input.get()+str(num)      
        self.var_Cal_input.set(xnum)
        
        # =====Clear Calculater fields====== 
    def Clear(self):
        self.var_Cal_input.set("")    
        #=========---Perform Calculation from input fiellds--========
    def Perform_Cal(self):
        result=self.var_Cal_input.get()
        self.var_Cal_input.set(eval(result))    
        
        
#=================== Show data in trewview ==================
    def show(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        self.cmb_Sale_Return.current(0)
        self.cmb_Return_type.current(0)
        try:
            cur.execute("Select pid,name,price,qty,status from products where status='Active'")
            rows=cur.fetchall()
            self.ProductsTable.delete(*self.ProductsTable.get_children())
            for row in rows:
                self.ProductsTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to {str(ex)}",parent=self.root)            
            
#========================  Search Function ======================
    def search(self):
        con=sqlite3.connect(database="ims.db")
        cur=con.cursor()
        try:
            
            if self.var_Search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:        
                cur.execute("select pid,name,price,qty,status from products where name LIKE '%"+self.var_Search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductsTable.delete(*self.ProductsTable.get_children())
                    for row in rows:
                        self.ProductsTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error",f"No Record found",parent=self.root)        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)
#==================Update Function ============================
#=====get data from Product table and set in input fields like QTY  P/QTY elc-=================
    def get_data(self,ev):
        f=self.ProductsTable.focus()
        content=(self.ProductsTable.item(f))
        row=content['values']
        self.var_P_id.set(row[0])
        self.var_P_name.set(row[1])
        if self.sale_Return.get()=="Return":
            price=str(int(row[2])/int(row[3]))
            self.var_P_price.set(price)
        else:
            self.var_P_price.set(row[2])    
        self.lbl_Instock.config(text=f"In Stock {str(row[3])}")
        self.var_stock.set(row[3])
        self.var_qty.set("1")
        print("Gujjar")
# =====get data from Cart table and set in input fields-================= 
    def get_data_cart(self,ev):
        f=self.C_P_Table.focus()
        content=(self.C_P_Table.item(f))
        row=content['values']
        self.var_P_id.set(row[0])
        self.var_P_name.set(row[1])
        self.var_P_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_Instock.config(text=f"In Stock {str(row[6])}")
        self.var_stock.set(row[6])
        print("Amir")
        # ===================Add update Cart ==========================
        
    def add_update_cart(self):
        if self.var_P_id.get()=="":
            messagebox.showerror("Error","Please Select Product from list",parent=self.root)
        elif self.var_qty.get()=="":
            messagebox.showerror("Error","Quantity is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error","Enter Quantity Grater then Stock",parent=self.root)
        
        else:
            # price_cal=int(self.var_qty.get())*float(self.var_P_price.get())
            # price_cal=float(price_cal)
            # print(price_cal)
            # price_cal=str(int(self.var_P_price.get())*int(self.var_qty.get()))
        
            
            cart_data=[self.var_P_id.get(),self.var_P_name.get(),self.var_P_price.get(),self.var_qty.get(),self.sale_Return.get(),self.good_Bad.get(), self.var_stock.get()]
            # print("Cart Data up")
            # print(cart_data)
            # print("Cart Data down")
            #------update Cart-----
            present="no"
            index_=0
            for row in self.cart_list:
                if self.var_P_id.get()==row[0]:
                    present="Yes"
                    break
                index_+=1
            # print(present,index_)    
            if present=="Yes":
                op=messagebox.askyesno("Confirm","Product allready Present\n Do you want to update | remove the product from the cart list",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.var_qty.get()    
            else:            
                self.cart_list.append(cart_data)
            self.show_Cart()
            self.var_P_id.set("")
            self.var_P_name.set("")
            self.var_P_price.set("")
            self.var_qty.set("")
            self.lbl_Instock.config(text=f"In Stock")
            self.var_status.set("")
            self.bill_updates()
            
#=================== Bill Update  ==================
    def imprtdata(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor() 
        cur.execute("Select * from products")
        # data=cur.fetchall()
        # df = pd.DataFrame(self.cart_list)
        # df.to_csv('data.csv', index = False)
        
        
        
        
    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        for row in self.cart_list:
            if row[4]=="Return":
                self.bill_amnt=self.bill_amnt-(float(row[2])*int(row[3]))
            else:
                self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))    
        self.net_pay=self.bill_amnt-((self.bill_amnt*5)/100)
        self.Discount=self.bill_amnt-self.net_pay
        self.lbl_Bill_amount.config(text=f"Bill Amount \n{str(self.bill_amnt)}")
        self.lbl_Net_pay.config(text=f"Net Pay \n{str(self.net_pay)}")
        self.title_cart.config(text=f"Cart \t Total Product {str(len(self.cart_list))}")        
#=================== Show data in trewview ==================
    def show_Cart(self):
       
        try:
            self.C_P_Table.delete(*self.C_P_Table.get_children())
            for row in self.cart_list:
                self.C_P_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to {str(ex)}",parent=self.root)            

#=================== Generate Bill ==================
    def bill_Generate(self):
        if self.var_C_name.get()=="" and self.var_C_no.get()=="":
            messagebox.showerror("Error","Customer details are Required!",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error","Please Add Product to the Cart",parent=self.root)
        else:
            
            # bill_top
            self.bill_top()
            # bill_middle.
            self.bill_middle()
            # bill_bottom
            self.bill_bottom()
            fp=open(f"bill/{str(self.invoice_no)}.txt","w")
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo("Success","Bill has been Genrated and Saved in backed Successfully!")       
            self.chk_print=1 
            # print("cart list")
            # self.print_bill()
            
            self.send_sales_data_into_databse()
            # self.customer_data_list=[self.var_C_name.get(),self.var_C_no.get()]
            
            for row in self.cart_list:
                print(row)
            # self.imprtdata()
           
            # print(row)
            # print(self.sales_list)
            # self.customer_data_list.extend(self.sales_list)
            # print(self.customer_data_list)
    def send_sales_data_into_databse(self):
        for row in self.cart_list:
            row[2]=str(int(row[2])*int(row[3]))
            row.pop(-1)
            row.insert(0,time.strftime("%Y/%m/%d"))
            row.insert(1,self.invoice_no)
            self.sales_list.append(row)
        for row in self.cart_list:
            print(row)    
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor() 
        try:
            # sql_insert='''insert into salesTable values(:1,:2,:3,:4,:5,:6)'''
            # cur.executemany(sql_insert,self.sales_list)
            # con.commit()
            pass
            # df = pd.DataFrame(data)
            # df.to_csv('data.csv', index = False)  
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
                
    def bill_top(self):
        self.invoice_no=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%y"))
        bill_top_temp=f'''
\tXYZ Inventory
phone No.04211223344
\tLHR-54401
{str("="*33)}
Name:   {self.var_C_name.get()}
Cell No:{self.var_C_no.get()}
Bill No.{str(self.invoice_no)}
Date:   {str(time.strftime("%d/%m/%y"))}
{str("="*33)}
Product Name Qty Price
{str("="*33)}
         '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert("1.0",bill_top_temp)
        
        
    def bill_bottom(self):
        number="0432"+str(self.invoice_no)
        my_code = Gs1_128(number, writer=ImageWriter())
        abc1=my_code.save("new_code3")
        bill_bottom_temp=f'''
{str("="*33)}
Bill Amount RS.{self.bill_amnt}
Discount    RS.{self.Discount}
Net pay     RS.{self.net_pay}        
{str("="*33)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)
        # self.txt_bill_area.insert(END,abc1)   
    # ==========bill Middle======= 
    def bill_middle(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        try:
            
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                cur.execute(f"Select price,qty from products where pid='{pid}'")
                StockPrice=cur.fetchone()
                
                if row[4]=="Return":
                    qty=int(StockPrice[1])+int(row[3]) 
                    status="Active"
                    UpdatedStockPrice=str(qty*int(StockPrice[0]))
                else:
                    UpdatedStockPrice=str(qty*int(StockPrice[0]))
                    qty=int(StockPrice[1])-int(row[6])
                    if int(row[3])==int(row[6]):
                        status="Inactive"
                    if int(row[3])!=int(row[6]):
                        status="Active"
                
               
                   
                       
                # cur.execute(f"Select price,qty from products where pid='{pid}'")
                # StockPrice=cur.fetchone()
                # UpdatedStockPrice=str(qty*int(StockPrice[0]))
                # qty=int(StockPrice[1])-int(row[6])
                
                # if int(row[3])==int(row[6]):
                #     status="Inactive"
                # if int(row[3])!=int(row[6]):
                #     status="Active"
                price=str(float(row[2])*int(row[3]))
                
                self.txt_bill_area.insert(END,"\n"+name.ljust(12)+"  "+row[3]+"   RS."+price)
                
                #======Update QTY in Product Table
                cur.execute("update products set qty=?,Tprice=?,status=? where pid=?",(
                    qty,
                    UpdatedStockPrice,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to {str(ex)}",parent=self.root)            
                # ================Clear Cart Fields================
    def Clear_cart(self):
        self.var_P_id.set("")
        self.var_P_name.set("")
        self.var_P_price.set("")
        self.var_qty.set("")
        self.lbl_Instock.config(text=f"In Stock")
        self.var_stock.set("")
                #  ===============Clear All fields function================== 
    def Clear_All(self):
        del self.cart_list[:]
        self.var_C_name.set("")
        self.var_C_no.set("")
        self.txt_bill_area.delete("1.0",END)
        self.show()
        self.show_Cart()
        self.Clear_cart()
        self.bill_updates()
        self.cmb_Sale_Return.current(0)
        self.cmb_Return_type.current(0)
        self.chk_print=0
#====================date and time update=====
    def Update_date_time(self):
        time_=time.strftime("%H:%M:%S")
        date_=time.strftime("%d/%m/%y")
        self.lbl_clock.config(text=f"Welcome to Inventry Management System\t\t Date: {str(date_)} \t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.Update_date_time)
           
    
    # =============Print bill==============
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please While Printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get("1.0",END))
            os.startfile(new_file,'print')
            
        else:
            messagebox.showerror("Error","Please Generate bill First",parent=self.root)
        self.chk_print=0  
        self.Clear_All()
        
        
        
          
        #=============== update stock after transections============
    def update(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please Select Product from the list",parent=self.root)
            else:
                cur.execute("Select * from products where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    self.var_Tprice=str(int(self.var_price.get())*int(self.var_qty.get())),
                    # print(self.var_Tprice)
                    cur.execute("update products set category=?,supplier=?,name=?,price=?,qty=?,Tprice=?,status=? where pid=?",(
                                        
                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),
                                        self.var_Tprice[0],
                                        self.var_status.get(),
                                        self.var_pid.get(),
                    ))    
                    con.commit()
                    messagebox.showinfo("Success","Product Updated Successfully !",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def RecognizBarcode(self):
        cap =cv2.VideoCapture(0)
        cap.set(3,340)  #3= width
        cap.set(4,280)  # 4= height
        used_codes=[]
        try:
                
            camera =True
            while camera ==True:
                success,frame =cap.read()
                for code in decode(frame):
                    if code.data.decode('utf-8') not  in used_codes:
                        print('Approved.You can Enter')
                        # print(code.data.decode('utf-8'))
                        self.var_Search.set(code.data.decode('utf-8'))
                        used_codes.append(code.data.decode('utf-8'))
                        time.sleep(1)
                        camera =False
                        self.search()
                    # elif code.data.decode('utf-8') in used_codes:
                    #     print('Sorry it is in')
                    #     time.sleep(1)
                    # else:
                    #     pass        
                    # print(code.type)
                    # print(code.data.decode('utf-8'))
                cv2.imshow('Testing code scan',frame)
                cv2.waitKey(1)
        except Exception as Ex:
            pass        
        print("Exit")            
                
    
    
        
if __name__=="__main__":        
    root=Tk()
    obj=billingClass(root)
    root.mainloop()