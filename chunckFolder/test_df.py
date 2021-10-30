import pandas as pd

df=pd.read_csv('data.csv')
# df=df[['Date']].sample(frac=1).head(7).reset_index(drop=True)
df=df[['Date']]
df['Date']=pd.to_datetime(df['Date'])
print(df['Date'])
# date1=pd.date_range(start='1/1/2018', end='1/08/2018')
# ab=date1[1]
# print(ab.split(' '))




# from datetime import timedelta, date
# def daterange(date1, date2):
#     for n in range(int ((date2 - date1).days)+1):
#         yield date1 + timedelta(n)

# start_dt = date(2021,8,4)
# end_dt = date(2021,8,6)
# for dt in daterange(start_dt, end_dt):
#     print(dt.strftime("%Y/%m/%d"))











# import sqlite3
# import pandas as pd
# import numpy as np
# def Run_Report():
        
#         con=sqlite3.connect(r"ims.db")
#         cur=con.cursor() 
#         cur.execute("Select * from salesTable")
#         data=cur.fetchall()
#         df1 = pd.DataFrame(data,columns=['Date','Invoice No','Product Code', 'Product Name', 'Price', 'Qty'])

#         list_1=[]
#         list_2=[]
#         for x in df1['Qty']:
#                 list_1.append(int(x)) 
        
#         Qty_sum =np.sum(list_1)
#         for x in df1['Price']:
#                 list_2.append(int(x))
#         Price_sum =np.sum(list_2)

#         df2=pd.DataFrame({'Date':[''],'Invoice No':[''],'Product Code':[''],'Product Name':[''],'Price':['Total Sales = '+str(Price_sum)],'Qty':["Total QTy = "+str(Qty_sum)]})
#         df3=df1.append(df2)
        
#         df3.to_csv('data.csv', index = False)
        
# Run_Report()               