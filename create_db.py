import sqlite3
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    #================Creating Employee Table=============
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)")
    con.commit()
    #================Creating Supplier Table=============
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    con.commit()
    # print("Done")
    
    #================Creating Supplier Table=============
    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()
    # print("Done")
    
    # "pid","category","supplier","name","price","qty","status"
    
    #================Creating Product Table=============
    cur.execute("CREATE TABLE IF NOT EXISTS products(pid INTEGER PRIMARY KEY AUTOINCREMENT,category text,supplier text,name text,price text,qty text,Tprice text,Pstatus text)")
    con.commit()
    # print("Done")
    
    #================Creating sales Table=============
    cur.execute("CREATE TABLE IF NOT EXISTS salesTable(Sno INTEGER PRIMARY KEY AUTOINCREMENT,productCode text,name text,Tprice text,Qty text)")
    con.commit()
    # print("Done")
    
# CREATE TABLE "salesTable" ("Date"	TEXT,"InvoiceNo"	TEXT,"productCode"	text,"name"	text,"Tprice"	text,"Qty"	TEXT);


create_db()