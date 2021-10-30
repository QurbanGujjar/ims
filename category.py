from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
# pip install pillow
class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventry Management System | Developed by Qurban Ali")
        self.root.config(bg="white")
        self.root.focus_force()
#===========label Size for all lable
        self.label_size=30

#==========variables=======
        self.var_category_name=StringVar()     
        self.var_category_id=StringVar()   

#=======Title=========
        title=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="#0f4d7d",fg="white").place(x=5,y=10,relwidth=1)
#============Enter category Name  ==========      
        lbl_category=Label(self.root,text="Enter Category Name",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=30,y=90)
#============text field =====
        txt_cat_name=Entry(self.root,textvariable=self.var_category_name,font=("goudy old style",20),bg="lightyellow").place(x=30,y=160)
#====================buttons=======
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",20),bg="#008000",fg="white",cursor="hand2").place(x=350,y=160,width=150,height=35)
        btn_add=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",20),bg="#FF0000",fg="white",cursor="hand2").place(x=510,y=160,width=150,height=35)
                
             
#=========== Category Details-====
        sup_frame=Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=700,y=80,width=400,height=120)
        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)
        self.CategoryTable=ttk.Treeview(sup_frame,columns=("cid","name",),yscrollcommand=scrolly.set,xscrollcommand=scrolly.set)
       
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)
       #====headings ===========================
        self.CategoryTable.heading("cid",text="C ID")
        self.CategoryTable.heading("name",text="Name")
        #========colom width ====================
        self.CategoryTable.column("cid",width=60)
        self.CategoryTable.column("name",width=60)

        self.CategoryTable["show"]="headings"
        self.CategoryTable.pack(fill=BOTH,expand=1)
                     
                     
        self.im1=Image.open("images/menu_im.jpg")
        self.im1=self.im1.resize((550,280),Image.ANTIALIAS)
        self.im1=ImageTk.PhotoImage(self.im1)
        lbl_image1=Label(self.root,image=self.im1)
        lbl_image1.place(x=600,y=200)
        
        self.im2=Image.open("images/im1.jpg")
        self.im2=self.im2.resize((550,280),Image.ANTIALIAS)
        self.im2=ImageTk.PhotoImage(self.im2)
        lbl_image2=Label(self.root,image=self.im2)
        lbl_image2.place(x=10,y=200)   
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
#-----===================================Functons-=--0-===================
#===============Add function======================
    def add(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        try:
            if self.var_category_name.get()=="":
                messagebox.showerror("Error","Category name Must be Required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_category_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Category already Present",parent=self.root)   
                    # print(self.var_sup_invoice_no.get()) 
                else:
                    cur.execute("insert into category(name) values(?)",(

                                self.var_category_name.get(),                                                                
                    ))    
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
                    self.show()
                #     self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
#=================== Show data in trewview ==================
    def show(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to {str(ex)}",parent=self.root)
 #===================== Get data back to fields=================================
    def get_data(self,ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        # print(row)
        self.var_category_id.set(row[0]),
        self.var_category_name.set(row[1]),
        


#===================== Delete Supplier from table function===============================
    def delete(self):
        con=sqlite3.connect(database="ims.db")
        cur=con.cursor()
        try:
            if self.var_category_id.get()=="":
                messagebox.showerror("Error","Please Select Category from the list",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_category_id.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Error , Please Try again ",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_category_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.show()
                        self.var_category_name.set("")
                        self.var_category_id.set("")
                
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)  



if __name__=="__main__":        
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()