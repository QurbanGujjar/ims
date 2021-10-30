from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
# pip install pillow
class productsClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventry Management System | Developed by Qurban Ali")
        self.root.config(bg="white")
        self.root.focus_force()
        self.label_size=20
        self.left_x=170
        # All variables
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_Tprice=StringVar()
        self.var_status=StringVar()
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_salary=StringVar()
        
#==================Left Frame for Products Details=========
        left_fram=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        left_fram.place(x=10,y=5,width=500,height=480)
        #=======Title=========
        title=Label(left_fram,text="Manage Product Details",font=("goudy old style",20),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        #=============product details-========
        lbl_category=Label(left_fram,text="Category",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=20,y=50)
        lbl_supplier=Label(left_fram,text="Supplier",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=20,y=100)
       
        lbl_name=Label(left_fram,text="Name",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=20,y=150)
        lbl_price=Label(left_fram,text="Price",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=20,y=200)
        lbl_qty=Label(left_fram,text="QTY",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=20,y=250)
        lbl_status=Label(left_fram,text="Status",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=20,y=300)
        
        cmb_category=ttk.Combobox(left_fram, textvariable=self.var_cat,values=self.cat_list,state="readonly",justify=CENTER,font=("goudy old style",self.label_size))
        cmb_category.place(x=self.left_x,y=50,width=180)
        cmb_category.current(0)
        cmb_supplier=ttk.Combobox(left_fram,textvariable=self.var_sup,values=self.sup_list,state="readonly",justify=CENTER,font=("goudy old style",self.label_size))
        cmb_supplier.place(x=self.left_x,y=100,width=180)
        cmb_supplier.current(0)
        
        txt_name=Entry(left_fram,textvariable=self.var_name,font=("goudy old style",self.label_size,"bold"),bg="lightyellow").place(x=self.left_x,y=150,width=180)
        txt_price=Entry(left_fram,textvariable=self.var_price,font=("goudy old style",self.label_size,"bold"),bg="lightyellow").place(x=self.left_x,y=200,width=180)
        txt_qty=Entry(left_fram,textvariable=self.var_qty,font=("goudy old style",self.label_size,"bold"),bg="lightyellow").place(x=self.left_x,y=250,width=180)
        
        cmb_status=ttk.Combobox(left_fram,textvariable=self.var_status,values=("Active","Inactive"),state="readonly",justify=CENTER,font=("goudy old style",self.label_size))
        cmb_status.place(x=self.left_x,y=300,width=180)
        cmb_status.current(0)
         #====================buttons=======
        btn_add=Button(left_fram,text="Save",command=self.add,font=("goudy old style",self.label_size),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=380,width=100,height=35)
        btn_update=Button(left_fram,text="Update",command=self.update,font=("goudy old style",self.label_size),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=380,width=100,height=35)
        btn_delete=Button(left_fram,text="Delete",command=self.delete,font=("goudy old style",self.label_size),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=380,width=100,height=35)
        btn_clear=Button(left_fram,text="Clear",command=self.clear,font=("goudy old style",self.label_size),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=380,width=100,height=35)
        
#==================Right Frame for Products Details=========
        right_fram=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        right_fram.place(x=530,y=5,width=550,height=480)
        #===============Search Frame==========
        SearchFrame=LabelFrame(right_fram,text="Search Products",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=5,y=5,width=530,height=70)
        #============Options======
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Caegory","Supplier","Name","Price","QTY","Status"),state="readonly",justify=CENTER,font=("goudy old style",12,"bold"))
        cmb_search.place(x=10,y=10,width=150,height=30)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=170,y=10,width=180,height=30)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=10,width=160,height=30)
        # =========================================== table===================
        sup_frame=Frame(right_fram,bd=3,relief=RIDGE)
        sup_frame.place(x=5,y=90,width=530,height=380)
        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)
        self.ProductsTable=ttk.Treeview(sup_frame,columns=("pid","category","supplier","name","price","qty","Tprice","status"),yscrollcommand=scrolly.set,xscrollcommand=scrolly.set)
       
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductsTable.xview)
        scrolly.config(command=self.ProductsTable.yview)
       #====headings ===========================
        self.ProductsTable.heading("pid",text="P ID")
        self.ProductsTable.heading("category",text="Category")
        self.ProductsTable.heading("supplier",text="Supplier")
        self.ProductsTable.heading("name",text="Name")
        self.ProductsTable.heading("price",text="Unit Price")
        self.ProductsTable.heading("qty",text="QTY")
        self.ProductsTable.heading("Tprice",text="Price")
        self.ProductsTable.heading("status",text="Status")
        #========colom width ====================
        self.ProductsTable.column("pid",width=60)
        self.ProductsTable.column("category",width=60)
        self.ProductsTable.column("supplier",width=60)
        self.ProductsTable.column("name",width=60)
        self.ProductsTable.column("price",width=60)
        self.ProductsTable.column("qty",width=60)
        self.ProductsTable.column("Tprice",width=60)
        self.ProductsTable.column("status",width=60)
        self.ProductsTable["show"]="headings"
        self.ProductsTable.pack(fill=BOTH,expand=1)
        self.ProductsTable.bind("<ButtonRelease-1>",self.get_data)  
        self.show()
        
        
#================================Functions=====================================================================================


#===========================fetch category and Suppier function 

    def fetch_cat_sup(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()
            self.cat_list.append("empty") 
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
                
            cur.execute("Select name from supplier")
            sup=cur.fetchall()
            self.sup_list.append("empty") 
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            

#================================Save or add or insert function============================
    def add(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_sup.get()=="Select" or self.var_name.get()=="" or self.var_price.get()=="" or self.var_qty.get()=="":
                messagebox.showerror("Error","All Field Required",parent=self.root)
            else:
                cur.execute("Select * from products where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","Product allready Present, Try Different One ",parent=self.root)
                else:
                    self.var_Tprice=str(int(self.var_price.get())*int(self.var_qty.get())),
                    # print(self.var_Tprice[0])
                    cur.execute("insert into products (category,supplier,name,price,qty,Tprice,status) values(?,?,?,?,?,?,?)",(
                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),
                                        self.var_Tprice[0],
                                        self.var_status.get(),
                    ))    
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfully !",parent=self.root)
                    self.show()
                    # self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
            
#=================== Show data in trewview ==================
    def show(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from products")
            rows=cur.fetchall()
            self.ProductsTable.delete(*self.ProductsTable.get_children())
            for row in rows:
                self.ProductsTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to {str(ex)}",parent=self.root)            

        
#================================Update function =========================
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
     #=======================Delete gfunction==================
    def delete(self):
        con=sqlite3.connect(database="ims.db")
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please Select Product from the list",parent=self.root)
            else:
                cur.execute("Select * from products where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","invalid Product ",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from products where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        # self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)  
        
#==================Update Function ============================
    def get_data(self,ev):
        f=self.ProductsTable.focus()
        content=(self.ProductsTable.item(f))
        row=content['values']
        # print(row)
        self.var_pid.set(row[0]),
        self.var_cat.set(row[1]),
        self.var_sup.set(row[2]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[7]),       
#====================Clear Function ==================
            
    def clear(self):
        self.var_cat.set("Select"),
        self.var_sup.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.var_status.set("Active"),
        self.show()        
#========================  Search Function======================
      
    def search(self):
        con=sqlite3.connect(database="ims.db")
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by Option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:        
                cur.execute("select * from products where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductsTable.delete(*self.ProductsTable.get_children())
                    for row in rows:
                        self.ProductsTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error",f"No Record found",parent=self.root)        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)
 
if __name__=="__main__":        
    root=Tk()
    obj=productsClass(root)
    root.mainloop()