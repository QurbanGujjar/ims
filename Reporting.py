from reportlab.pdfgen.canvas import Canvas
from PollyReports import *
import sqlite3
import os
from tkinter import messagebox
import webbrowser as vb
from datetime import timedelta, date

from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pandas as pd
import numpy as np
# from tkcalendar import Calendar


# pip install pillow
class ReportingClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventry Management System | Developed by Qurban Ali")
        self.root.config(bg="white")
        self.root.focus_force()
#===========label Size for all lable
        self.label_size=30
        self.E1=StringVar()
        self.E2=StringVar()

#==========variables=======
        self.var_category_name=StringVar()     
        self.var_category_id=StringVar()  
        self.var_Run_Report=StringVar() 
        
        self.label_size=20
        self.left_x=170

#=======Title=========
        title=Label(self.root,text="IMS Reporting Module",font=("goudy old style",30),bg="#0f4d7d",fg="white").place(x=5,y=10,relwidth=1)
#============Enter category Name  ==========      
        lbl_category=Label(self.root,text="Select Report Name",font=("goudy old style",self.label_size,"bold"),bg="white").place(x=30,y=90)
#============text field =====
        L1 = Label(self.root, text="Enter Starting Date",font=("goudy old style",self.label_size,"bold"))
        L1.place(x=30,y=200)
        self.E1 = Entry(self.root, bd =2,font=("goudy old style",self.label_size,"bold"))
        self.E1.place(x=260,y=200)
        
        L2 = Label(self.root, text="Enter Ending Date",font=("goudy old style",self.label_size,"bold"))
        L2.place(x=30,y=250)
        self.E2 = Entry(self.root, bd =2,font=("goudy old style",self.label_size,"bold"))
        self.E2.place(x=260,y=250)
        # txt_cat_name=Entry(self.root,textvariable=self.var_category_name,font=("goudy old style",20),bg="lightyellow").place(x=30,y=160)
        cmb_status=ttk.Combobox(self.root,textvariable=self.var_Run_Report,values=("Select Report","Sales Report","Stock Report"),state="readonly",justify=CENTER,font=("goudy old style",self.label_size,"bold"))
        cmb_status.place(x=30,y=160)
        cmb_status.current(0)
        
#====================buttons=======
        btn_add=Button(self.root,text="Run Report",command=self.Run_Report,font=("goudy old style",20),bg="#008000",fg="white",cursor="hand2").place(x=800,y=160,width=150,height=35)
        # btn_add=Button(self.root,text="Delete",font=("goudy old style",20),bg="#FF0000",fg="white",cursor="hand2").place(x=510,y=160,width=150,height=35)
    def daterange(date1,date2):
        for n in range(int ((date2 - date1).days)+1):
             yield date1 + timedelta(n)
            
    def Run_Report(self):
        # print("Report Genrated")
        # os.system("C:/ProgramData/Anaconda3/python.exe d:/project1/Stock_Report.py")
        if self.var_Run_Report.get()=="Sales Report":
                self.SalesReport()
        elif self.var_Run_Report.get()=="Stock Report":
                self.StocksReport()
                # self.SalesReport()
#        pass


    
    def SalesReport(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor() 
        try:
            if self.E1.get()=="" and self.E2.gt()=="":
                    messagebox.showerror("Error","Please Enter Starting and Ending Date First")
            else:        
                cur.execute(f"Select * from salesTable WHERE Date BETWEEN '{self.E1.get()}' AND '{self.E2.get()}'")
                data=cur.fetchall()
                df1 = pd.DataFrame(data,columns=['Date','Invoice No','Product Code', 'Product Name', 'Price', 'Qty'])
        
                list_1=[]
                list_2=[]
                Qty_sum=0
                Price_sum=0
                for x in df1['Qty']:
                        list_1.append(int(x)) 
                        Qty_sum =np.sum(list_1)
                for x in df1['Price']:
                        list_2.append(int(x))
                Price_sum =np.sum(list_2)
                df2=pd.DataFrame({'Date':[''],'Invoice No':[''],'Product Code':[''],'Product Name':['Total Sales = '],'Price':[str(Price_sum)],'Qty':["QTy = "+str(Qty_sum)]})
                df3=df1.append(df2)
                df3.to_csv('data.csv', index = False)
                messagebox.showinfo("Success","Report Genrated Successfully as data.csv")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def StocksReport(self):
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor() 

        try:
            cur.execute("Select * from products")
            data=cur.fetchall()
        #     category text,supplier text,name text,price text,qty text,Tprice text,Pstatus text
            df1 = pd.DataFrame(data,columns=['Product Id','Category','Supplier','Product Name','Unit Price','Qty','Total Price','Status'])
            
            list_1=[]
            list_2=[]
            Qty_sum=0
            Price_sum=0
            for x in df1['Qty']:
                list_1.append(int(x)) 
                Qty_sum =np.sum(list_1)
            for x in df1['Total Price']:
                list_2.append(int(x))
            Price_sum =np.sum(list_2)
                        #       'Product Id','Category','Supplier','Product Name','Unit Price','Qty','Total Price','Status'])
                                                                                        # Product Id,Category,Supplier,Product Name,Unit Price,Qty,Total Price,Status
            
            df2=pd.DataFrame({'Product Id':[''],'Category':[''],'Supplier':[''],'Product Name':[''],'Unit Price':[''],'Qty':["QTy = "+str(Qty_sum)],'Total Price':[str(Price_sum)],'Status':['']})
            df3=df1.append(df2)
            df3.to_csv('StocksReport.csv', index = False)
            messagebox.showinfo("Success","Report Genrated Successfully as data.csv")
        
        
                
        except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    

            
            
            
                    
               
if __name__=="__main__":        
    root=Tk()
    obj=ReportingClass(root)
    root.mainloop()