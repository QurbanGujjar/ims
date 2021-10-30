from reportlab.pdfgen.canvas import Canvas
from PollyReports import *
from testdata import data
import sqlite3
import os
from tkinter import messagebox
import webbrowser as vb
# ================== Variables=======
Qty_list = []
Price_list = []
Qty_sum=0
Price_sum=0
# ==========SQL connection============
con=sqlite3.connect(r"ims.db")
cur=con.cursor()  

try:
    cur.execute("Select * from products")
    data=cur.fetchall()
    for row in data:
        Qty_list.append(int(row[5]))
        Price_list.append(int(row[6]))
        
    for x in Qty_list:
        Qty_sum=Qty_sum + x
        
    for x in Price_list:
        Price_sum=Price_sum + x
    rpt = Report(data)
# =============== Header ================
    rpt.pageheader = Band([
    Element((36, 0), ("Times-Bold", 20), 
        text = "Page Header"),
    # category text,supplier text,name text,price text,qty text,Pstatus text
    Element((0, 24), ("Helvetica", 12), 
        text = "Category Name"),
    Element((100, 24), ("Helvetica", 12), 
        text = "Supplier Name"),
    Element((200, 24), ("Helvetica", 12), 
        text = "Product Name"),
    Element((300, 24), ("Helvetica", 12), 
        text = "Price"),
    Element((400, 24), ("Helvetica", 12), 
        text = "Qty",),
    Element((500, 24), ("Helvetica", 12), 
        text = "Total Price"),
    Element((600, 24), ("Helvetica", 12), 
        text = "Status",),
    
    Rule((0, 42), 8*80, thickness = 2),])
    rpt.pagefooter = Band([
    Element((72*8, 0), ("Times-Bold", 20), 
        text = "Page Footer", align = "right"),
    Element((36, 16), ("Helvetica-Bold", 12), 
        sysvar = "pagenumber", 
        format = lambda x: "Page %d" % x),
    ])
    
    # ==============Data inserted into Page=============
    rpt.detailband = Band([
        Element((0, 24), ("Helvetica", 12),key=1), 
        # text = "Category Name"),
        Element((100, 24), ("Helvetica", 12),key=2), 
            # text = "Supplier Name"),
        Element((200, 24), ("Helvetica", 12),key=3), 
            # text = "Product Name"),
        Element((300, 24), ("Helvetica", 12),key=4), 
            # text = "Price"),
        Element((400, 24), ("Helvetica", 12), key=5),
            # text = "Qty",),
        Element((500, 24), ("Helvetica", 12),key=6), 
            # text = "Total Price"),
        Element((600, 24), ("Helvetica", 12),key=7), 
        # text = "Status",),
    ])
    # ============Footer==========
    rpt.reportfooter = Band([
    Rule((300, 1), 300),
    Element((300, 4), ("Helvetica-Bold", 12),
        text = "Total Qty = "),
    Element((430, 4), ("Helvetica-Bold", 12),
        text = "Grand Total = "),
    Element((400,5), ("Helvetica-Bold", 12), 
        text = f"{str(Qty_sum)}"),
    Element((510,5), ("Helvetica-Bold", 12), 
        text = f"{str(Price_sum)}"),

])
    
    canvas = Canvas("ReportsFolder/sample02.pdf", (72*11, 72*8.5))
    rpt.generate(canvas)
    canvas.save()
    # vb.open_new("sample02.pdf")
    
    
    
    # if os.path.exists("sample02.pdf"):
    #     # os.close("sample02.pdf")   # error in this line 
    #     os.remove("bill/sample02.pdf")
    #     canvas = Canvas("sample02.pdf", (72*11, 72*8.5))
    #     rpt.generate(canvas)
    #     canvas.save()
    #     vb.open_new("sample02.pdf")
    # else:
    #     print("The file does not exist")
    #     canvas = Canvas("bill/sample02.pdf", (72*11, 72*8.5))
    #     rpt.generate(canvas)
    #     canvas.save()
    #     vb.open_new("bill/sample02.pdf")
except Exception as ex:
    messagebox.showerror("Error",f"Error Due to {str(ex)}")