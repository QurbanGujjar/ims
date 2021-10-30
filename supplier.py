from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

# pip install pillow
class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventry Management System | Developed by Qurban Ali")
        self.root.config(bg="white")
        self.root.focus_force()
        self.label_size=15
        #All variables    
        self.var_sup_invoice_no=StringVar()
        self.var_sup_name=StringVar()
        self.var_sup_contact=StringVar()
        self.var_sup_invoice_no_Search=StringVar()
        
        
        #=================Left Frame=================
        left_fram=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        left_fram.place(x=10,y=5,width=580,height=480)
        
        #=======Title=========
        title=Label(left_fram,text="Manage Supplier Details",font=("goudy old style",20),bg="#0f4d7d",fg="white").place(x=0,y=10,relwidth=1)
        
        #========Column 1 ========
        
        lbl_sup_invoice=Label(left_fram,text="Invoice No.",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=5,y=60)
        lbl_sup_name=Label(left_fram,text="Supplier Name",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=5,y=100)
        lbl_sup_contact=Label(left_fram,text="Contact",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=5,y=140)
        lbl_sup_disc=Label(left_fram,text="Discription",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=5,y=180)
        #========Column 1 ========
        txt_invoice_no=Entry(left_fram,textvariable=self.var_sup_invoice_no,font=("goudy old style",self.label_size),bg="lightyellow").place(x=140,y=60,width=180)
        txt_SP_name=Entry(left_fram,textvariable=self.var_sup_name,font=("goudy old style",self.label_size),bg="lightyellow").place(x=140,y=100,width=180)
        txt_SP_contact=Entry(left_fram,textvariable=self.var_sup_contact,font=("goudy old style",self.label_size),bg="lightyellow").place(x=140,y=140,width=180)
        
        self.txt_sup_description=Text(left_fram,font=("goudy old style",self.label_size,""),bg="lightyellow")
        self.txt_sup_description.place(x=140,y=180,width=420,height=120)
        
        #====================buttons=======
        btn_add=Button(left_fram,text="Save",command=self.add,font=("goudy old style",self.label_size),bg="#2196f3",fg="white",cursor="hand2").place(x=140,y=305,width=90,height=28)
        btn_update=Button(left_fram,text="Update",command=self.update,font=("goudy old style",self.label_size),bg="#4caf50",fg="white",cursor="hand2").place(x=240,y=305,width=90,height=28)
        btn_delete=Button(left_fram,text="Delete",command=self.delete,font=("goudy old style",self.label_size),bg="#f44336",fg="white",cursor="hand2").place(x=340,y=305,width=90,height=28)
        btn_clear=Button(left_fram,text="Clear",command=self.clear,font=("goudy old style",self.label_size),bg="#607d8b",fg="white",cursor="hand2").place(x=440,y=305,width=90,height=28)
        #====================== Right Frame====================
        right_fram=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        right_fram.place(x=590,y=5,width=500,height=480)
        
        lbl_supplier_invoice_no=Label(right_fram,text="Invoice No.",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=10,y=20)
        txt_invoice_no=Entry(right_fram,textvariable=self.var_sup_invoice_no_Search,font=("goudy old style",self.label_size),bg="lightyellow").place(x=150,y=20,width=180)
        btn_Seach=Button(right_fram,text="Search",command=self.search,font=("goudy old style",self.label_size),bg="#4caf50",fg="white",cursor="hand2").place(x=350,y=20,width=90,height=28)
        
        #=========== Suppliers Details-====
        sup_frame=Frame(right_fram,bd=3,relief=RIDGE)
        sup_frame.place(x=10,y=55,width=480,height=420)
        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)
        self.SupplierTable=ttk.Treeview(sup_frame,columns=("invoice","name","contact","desc",),yscrollcommand=scrolly.set,xscrollcommand=scrolly.set)
       
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)
       #====headings ===========================
        self.SupplierTable.heading("invoice",text="Invoice ID")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable.heading("desc",text="Description")
        #========colom width ====================
        self.SupplierTable.column("invoice",width=60)
        self.SupplierTable.column("name",width=60)
        self.SupplierTable.column("contact",width=60)
        self.SupplierTable.column("desc",width=60)
        self.SupplierTable["show"]="headings"
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
#================================================Functions =============================================
    def add(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        try:
            if self.var_sup_invoice_no.get()=="":
                messagebox.showerror("Error","Invoice N0 Must be Required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice_no.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Invoice ID already Assigned")   
                    # print(self.var_sup_invoice_no.get()) 
                else:
                    cur.execute("insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                                self.var_sup_invoice_no.get(),
                                self.var_sup_name.get(),
                                self.var_sup_contact.get(),
                                self.txt_sup_description.get('1.0',END)
                                                                
                    ))    
                    con.commit()
                    messagebox.showinfo("Success","Invoice Added Successfully")
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    #=================== Show data in trewview ==================
    def show(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to {str(ex)}",parent=self.root)
    #===================== Get data back to fields=================================
    def get_data(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        # print(row)
        self.var_sup_invoice_no.set(row[0]),
        self.var_sup_name.set(row[1]),
        self.var_sup_contact.set(row[2]),
        self.txt_sup_description.delete('1.0',END)
        self.txt_sup_description.insert(END,row[3]),
    #====================== Update data function ============================
    def update(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.var_sup_invoice_no.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice_no.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Supplier invoice No ",parent=self.root)
                else:
                    cur.execute("update supplier set name=?,contact=?,desc=? where invoice=?",(
                                        
                                        self.var_sup_name.get(),
                                        self.var_sup_contact.get(),
                                        self.txt_sup_description.get("1.0",END),
                                        self.var_sup_invoice_no.get()
                                    
                    ))    
                    con.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully !",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
#===================== Delete Supplier from table function===============================
    def delete(self):
        con=sqlite3.connect(database="ims.db")
        cur=con.cursor()
        try:
            if self.var_sup_invoice_no.get()=="":
                messagebox.showerror("Error","Invoice No must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice_no.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Invoic No ",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice_no.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)  
            
            
    #==================== Clear all the fields function===============
    def clear(self):
        self.var_sup_invoice_no.set("")
        self.var_sup_name.set("")
        self.var_sup_contact.set("")
        self.txt_sup_description.delete("1.0",END)
        self.show()        

    #=================Search function ========================
    
    def search(self):
        con=sqlite3.connect(database="ims.db")
        cur=con.cursor()
        try:
           if self.var_sup_invoice_no_Search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
           else:        
                cur.execute("select * from supplier where invoice=?",self.var_sup_invoice_no_Search.get())
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    for row in rows:
                        self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error",f"No Record found",parent=self.root)        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)
                

if __name__=="__main__":        
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()