import pandas as pd
import sqlite3
con=sqlite3.connect(r"ims.db")
cur=con.cursor() 
cur.execute("Select * from products")
data=cur.fetchall()
df = pd.DataFrame(data)
df.to_csv('data.csv', index = False)