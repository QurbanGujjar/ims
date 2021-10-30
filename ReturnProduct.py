from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from barcode.writer import ImageWriter
from barcode import Gs1_128
import sqlite3
import tempfile
import time
import os

from cv2 import BackgroundSubtractor
# pip install pillow
class ReturnProductClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1500x700+0+0")
        self.root.title("Inventry Management System | Developed by Qurban Ali")
        self.root.config(bg="white")
        self.root.focus_force()
#===========label Size for all lable
        self.label_size=20

#==========variables=======
        self.cart_list=[]
        self.var_invoice_no=StringVar()     
        self.var_category_id=StringVar()   
        self.var_P_name=StringVar()
        self.var_P_price=StringVar()
        self.var_P_id=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()
        self.var_stock=StringVar()

#=======Title=========
        title=Label(self.root,text="Manage Return Product",font=("goudy old style",30),bg="#0f4d7d",fg="white").place(x=0,y=10,relwidth=1)
#============Enter category Name  ==========      
        lbl_Invoce_no=Label(self.root,text="Enter Or Scane Invoice No",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=0,y=70)
#============text field =====
        txt_invoce_no=Entry(self.root,textvariable=self.var_invoice_no,font=("goudy old style",20),bg="lightyellow").place(x=5,y=120,width=200)
#====================buttons=======
        btn_add=Button(self.root,text="Search",command=self.Search_invoic,font=("goudy old style",20),bg="#008000",fg="white",cursor="hand2").place(x=250,y=120,width=150,height=35)
        # btn_add=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",20),bg="#FF0000",fg="white",cursor="hand2").place(x=510,y=160,width=150,height=35)
                
             
#=========== Invoice  Details-====
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

        sup_frame=Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=0,y=200,width=400,height=400)
        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)
        self.Sales_Table=ttk.Treeview(sup_frame,columns=("Date","invoiceNo","productCode","name","Tprice","Qty",),yscrollcommand=scrolly.set,xscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.Sales_Table.xview)
        scrolly.config(command=self.Sales_Table.yview)
       #====headings ===========================
        self.Sales_Table.heading("Date",text="Date")
        self.Sales_Table.heading("invoiceNo",text="Invoice No")
        self.Sales_Table.heading("productCode",text="Product Code")
        self.Sales_Table.heading("name",text="Product Name")
        self.Sales_Table.heading("Tprice",text="Price")
        self.Sales_Table.heading("Qty",text="Qty")
        # self.Sales_Table.heading("name",text="Name")
        #========colom width ====================
        self.Sales_Table.column("Date",width=60)
        self.Sales_Table.column("invoiceNo",width=60)
        self.Sales_Table.column("productCode",width=60)
        self.Sales_Table.column("name",width=60)
        self.Sales_Table.column("Tprice",width=60)
        self.Sales_Table.column("Qty",width=60)

        self.Sales_Table["show"]="headings"
        self.Sales_Table.pack(fill=BOTH,expand=1)
                     
                     
        # self.im1=Image.open("images/menu_im.jpg")
        # self.im1=self.im1.resize((550,280),Image.ANTIALIAS)
        # self.im1=ImageTk.PhotoImage(self.im1)
        # lbl_image1=Label(self.root,image=self.im1)
        # lbl_image1.place(x=600,y=200)
        
        # self.im2=Image.open("images/im1.jpg")
        # self.im2=self.im2.resize((550,280),Image.ANTIALIAS)
        # self.im2=ImageTk.PhotoImage(self.im2)
        # lbl_image2=Label(self.root,image=self.im2)
        # lbl_image2.place(x=10,y=200)   
        self.Sales_Table.bind("<ButtonRelease-1>",self.get_data)
        
        self.var_C_name=StringVar()
        self.var_C_no=StringVar()
        
        customer_fram=Frame(self.root,bd=1,relief=RIDGE,bg="white")
        customer_fram.place(x=405,y=65,width=540,height=540)
        
        customer_Detail_fram=Frame(customer_fram,bd=1,relief=RIDGE,bg="white")
        customer_Detail_fram.place(x=1,y=1,width=538,height=80)
        title=Label(customer_Detail_fram,text="Customer Details",font=("goudy old style",20,"bold"),bg="gray",fg="black").pack(side=TOP,fill=X)
        lbl_invoice=Label(customer_Detail_fram,text="Customer Name.",font=("goudy old style",15,"bold"),bg="white").place(x=1,y=40)
        txt_C_name=Entry(customer_Detail_fram,textvariable=self.var_C_name,font=("goudy old style",15),bg="lightyellow").place(x=145,y=40,width=140,height=30)
        lbl_invoice=Label(customer_Detail_fram,text="Contact No.",font=("goudy old style",15,"bold"),bg="white").place(x=288,y=40)
        txt_C_no=Entry(customer_Detail_fram,textvariable=self.var_C_no,font=("goudy old style",15),bg="lightyellow").place(x=392,y=40,width=140,height=30)
        
        Cust_Pro_frame=Frame(customer_fram,bd=2,relief=RIDGE,bg="white")
        Cust_Pro_frame.place(x=1,y=90,width=535,height=250)
        
        
        Cart_frame=Frame(Cust_Pro_frame,bd=2,relief=GROOVE,bg="white")
        Cart_frame.place(x=0,y=1,width=530,height=245)
        self.title_cart=Label(Cart_frame,text="Cart\tTotal Products [0]",font=("goudy old style",16),bg="gray",fg="black")
        self.title_cart.pack(side=TOP,fill=X)
    #     #=========== Category Details-====
        C_P_frame=Frame(Cart_frame,bd=3,relief=RIDGE)
        C_P_frame.place(x=0,y=33,width=525,height=207)
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
        
        
        Instock_frame=Frame(customer_fram,bd=2,relief=RIDGE,bg="white")
        Instock_frame.place(x=2,y=340,width=535,height=197)
        lbl_invoice=Label(Instock_frame,text="Product Name",font=("goudy old style",15,"bold"),bg="white").place(x=1,y=1)
        txt_C_name=Entry(Instock_frame,textvariable=self.var_P_name,state="readonly",font=("goudy old style",15),bg="lightyellow").place(x=1,y=30,width=160,height=30)
        lbl_invoice=Label(Instock_frame,text="Price Per QTY.",font=("goudy old style",15,"bold"),bg="white").place(x=180,y=1)
        txt_C_name=Entry(Instock_frame,textvariable=self.var_P_price,font=("goudy old style",15),bg="lightyellow").place(x=180,y=30,width=160,height=30)
        lbl_invoice=Label(Instock_frame,text="Quantity.",font=("goudy old style",15,"bold"),bg="white").place(x=360,y=1)
        txt_qty=Entry(Instock_frame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow").place(x=360,y=30,width=160,height=30)
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
        
        # self.show()
#-----===================================Functons-=--0-===================
#===============Search Invoice function======================
    def Search_invoic(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        try:
            if self.var_invoice_no.get()=="":
                messagebox.showerror("Error","Invoce No Must be Required",parent=self.root)
            else:
                cur.execute("Select * from salesTable where InvoiceNo=?",(self.var_invoice_no.get(),))
                rows=cur.fetchall()
                if rows==None:
                    messagebox.showerror("Error","ther is No Invoice find for this match",parent=self.root)   
                    # print(self.var_sup_invoice_no.get()) 
                else:
                    
                    self.Sales_Table.delete(*self.Sales_Table.get_children())
                   
                    for row in rows:
                        self.Sales_Table.insert('',END,values=row)
                   
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
#=================== Show data in trewview ==================
    def show_Cart(self):
       
        try:
            self.C_P_Table.delete(*self.C_P_Table.get_children())
            for row in self.cart_list:
                self.C_P_Table.insert('',END,values=row)
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
            
            cart_data=[self.var_P_id.get(),self.var_P_name.get(),self.var_P_price.get(),self.var_qty.get(),self.var_stock.get()]
            # print("Cart Data up")
            print(cart_data)
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
                
    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.net_pay=self.bill_amnt-((self.bill_amnt*5)/100)
        self.Discount=self.bill_amnt-self.net_pay
        self.lbl_Bill_amount.config(text=f"Bill Amount \n{str(self.bill_amnt)}")
        self.lbl_Net_pay.config(text=f"Net Pay \n{str(self.net_pay)}")
        self.title_cart.config(text=f"Cart \t Total Product {str(len(self.cart_list))}")                    
            
#=================== Show data in trewview ==================

    def show(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from category")
            rows=cur.fetchall()
            self.Sales_Table.delete(*self.Sales_Table.get_children())
            for row in rows:
                self.Sales_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to {str(ex)}",parent=self.root)
 #===================== Get data back to fields=================================
    def get_data(self,ev):
        f=self.Sales_Table.focus()
        content=(self.Sales_Table.item(f))
        row=content['values']
        print(row)
        self.var_P_id.set(row[2])
        self.var_P_name.set(row[3])
        price=str(int((row[4])/int(row[5])))
        self.var_P_price.set(price)
        self.var_qty.set(row[5])
        # self.var_qty.set("")
        self.var_stock.set(row[5])
        self.lbl_Instock.config(text=f"In Stock {str(row[5])}")
 # =====get data from Cart table and set in input fields-================= 
    def get_data_cart(self,ev):
        f=self.C_P_Table.focus()
        content=(self.C_P_Table.item(f))
        row=content['values']
        self.var_P_id.set(row[0])
        self.var_P_name.set(row[1])
        self.var_P_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_Instock.config(text=f"In Stock {str(row[4])}")
        self.var_stock.set(row[4])

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
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor() 
        try:
            sql_insert='''insert into salesTable values(:1,:2,:3,:4,:5,:6)'''
            cur.executemany(sql_insert,self.sales_list)
            con.commit()
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
                qty=int(row[4])-int(row[3])
                cur.execute(f"Select price from products where pid='{pid}'")
                SockPrice=cur.fetchone()
                # print(SockPrice[0])
                # print("Stock Price relevent Product"+)
                UpdatedSockPrice=str(qty*int(SockPrice[0]))
                
                if int(row[3])==int(row[4]):
                    status="Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"
                price=str(float(row[2])*int(row[3]))
                
                self.txt_bill_area.insert(END,"\n"+name.ljust(12)+"  "+row[3]+"   RS."+price)
                
                #======Update QTY in Product Table
                cur.execute("update products set qty=?,Tprice=?,status=? where pid=?",(
                    qty,
                    UpdatedSockPrice,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to {str(ex)}",parent=self.root)    
            
            
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please While Printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get("1.0",END))
            os.startfile(new_file,'print')
            
        else:
            messagebox.showerror("Error","Please Generate bill First",parent=self.root)
        self.chk_print=0  
                        
                # ================Clear Cart Fields================
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
        self.chk_print=0


if __name__=="__main__":        
    root=Tk()
    obj=ReturnProductClass(root)
    root.mainloop()