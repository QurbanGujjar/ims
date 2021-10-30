from tkinter import*
from PIL import Image,ImageTk
# pip install pillow
from tkinter import ttk,messagebox
import os
class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventry Management System | Developed by Qurban Ali")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #=============All variaables====================
        self.bill_list=[]
        self.invoice_no=StringVar()
        self.var_invoice=StringVar()

#=======Title=========
        title=Label(self.root,text="View Customer Bills",font=("goudy old style",20),bd=3,relief=RIDGE, bg="#184a45",fg="white").pack(side=TOP,fill=X)
        


        search_fram=Frame(self.root,bd=0,relief=RIDGE,bg="white")
        search_fram.place(x=10,y=40,width=600,height=45)
        lbl_invoice_no=Label(search_fram,text="Invoice No.",font=("goudy old style",15,"bold"),bg="white").place(x=10,y=5)
    
        txt_search=Entry(search_fram,textvariable=self.var_invoice,font=("goudy old style",15),bg="lightyellow").place(x=120,y=5,width=150,height=30)
        btn_search=Button(search_fram,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=280,y=5,width=110,height=30)
        btn_clear=Button(search_fram,text="Clear",command=self.clear,font=("goudy old style",15,"bold"),bg="lightgray",cursor="hand2").place(x=400,y=5,width=110,height=30)
        
        inv_bill_fram=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        inv_bill_fram.place(x=10,y=80,width=596,height=400)
        #===============Bill List==========
        sales_fram=Frame(inv_bill_fram,bd=2,relief=RIDGE,bg="white")
        sales_fram.place(x=5,y=5,width=200,height=384)
        
        scrolly=Scrollbar(sales_fram,orient=VERTICAL)
        self.Sales_list=Listbox(sales_fram,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_list.yview)
        self.Sales_list.pack(fill=BOTH,expand=1)
        self.Sales_list.bind("<ButtonRelease-1>",self.get_data)
        # #==============Bill Area=========
        title=Label(inv_bill_fram,text="Customer Bill Area ",font=("goudy old style",20),bg="orange").place(x=210,y=0,width=380,height=30)
        
        bill_fram=Frame(inv_bill_fram,bd=2,relief=RIDGE,bg="white")
        bill_fram.place(x=210,y=32,width=380,height=360)
        
        scrolly2=Scrollbar(bill_fram,orient=VERTICAL)
        self.bill_area=Text(bill_fram,font=("goudy old style",10),bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)
        
        
        #====================printer image===========
        self.bill_photo=Image.open("images/abc.jpg")
        self.bill_photo=self.bill_photo.resize((450,300),Image.ANTIALIAS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)
        lbl_image1=Label(self.root,image=self.bill_photo,bd=0)
        lbl_image1.place(x=620,y=100)
        self.show()
        
#=====================================================================================

#===========functions========


    def show(self):
        self.Sales_list.delete(0,END)
        del self.bill_list[:]
        # print(os.listdir("../project1"))
        # print(i.split(".")[-1])    
        for i in  os.listdir("bill"):
            if i.split(".")[-1]=="txt":
                self.Sales_list.insert(END,i) 
                self.bill_list.append(i.split(".")[0])
                
                
    def get_data(self,ev):
        
        index_=self.Sales_list.curselection()
        file_name=self.Sales_list.get(index_)
        # print(file_name)
        self.bill_area.delete("1.0",END)
        fp=open(f"bill/{file_name}","r")
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()
#=================================Search function -===================


    def search(self):
        try:
           if self.var_invoice.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
           else:
            #    print(self.var_invoice.get())
               if self.var_invoice.get() in self.bill_list:
                   self.Sales_list.delete(0,END)
                   self.Sales_list.insert(END,self.var_invoice.get()+".txt")
               else:
                   messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                #    fp=open(f"bill/{self.var_invoice.get()}.txt","r")
                #    self.bill_area.delete("1.0",END)
                #    for i in fp:
                #        self.bill_area.insert(END,i)
                #    fp.close()          
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)
#=================================Clear function -===================
    def clear(self):
        self.show()
        self.bill_area.delete("1.0",END)        
                                       

        
        
if __name__=="__main__":        
    root=Tk()
    obj=salesClass(root)
    root.mainloop()