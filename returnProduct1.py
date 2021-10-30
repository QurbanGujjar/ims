from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from barcode.writer import ImageWriter
from barcode import Gs1_128
import sqlite3
import tempfile
import time
import os

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
            