from tkinter import*
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Login |  Inventory Management System")
        self.root.config(bg="white")

        #===================Images===============
       
        self.im2=Image.open("images/photo.jpg")                #=====main image===========
        self.im2=self.im2.resize((500,500),Image.ANTIALIAS)
        self.im2=ImageTk.PhotoImage(self.im2)
        self.lbl_im2=Label(self.root,image=self.im2,bd=0,relief=RAISED)
        self.lbl_im2.place(x=200,y=50)
       # self.phone_image=ImageTk.PhotoImage(file="images/phon.png")
       # self.lbl_Phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=200,y=50)
        #===============login Frame===========
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=50,relwidth=1)
       

        lbl_user=Label(login_frame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        self.Employee_ID=Entry(login_frame,font=("times new roman",15),bg="#ECECEC")
        self.Employee_ID.place(x=50,y=140,width=250)               
       
        lbl_pass=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        self.txt_pass=Entry(login_frame,font=("times new roman",15),bg="#ECECEC")
        self.txt_pass.place(x=50,y=240,width=250)

        btn_login=Button(login_frame,command=self.login,text="Log In",font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",activeforeground="white",fg="white",cursor="hand2").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",font=("times new roman",15,"bold"),bg="white",fg="lightgray").place(x=150,y=355)
        
        btn_forget=Button(login_frame,text="Forget Password?",font=("times new roman",15),bg="white",fg="#00759E",activebackground="white",activeforeground="#00759E",bd=0).place(x=100,y=390)

        #=============Register Frame=============
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=650,y=570,width=350,height=60)

        lbl_reg=Label(register_frame,text="Like |  Share | Subscribe ",font=("times new roman",15),bg="white").place(x=0,y=20,relwidth=1)
        # btn_signup=Button(register_frame,text="Sign Up",font=("times new roman",15,"bold"),bg="white",fg="#00759E",activebackground="white",activeforeground="#00759E",bd=0).place(x=208,y=17)


#=======================All Functions=================
    def login(self):
         
        con=sqlite3.connect(r"ims.db")
        cur=con.cursor()
        try:
            if self.Employee_ID.get()=="" or self.txt_pass.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.Employee_ID.get(),self.txt_pass.get()))
                user=cur.fetchone()
                print(user[0])
                if user[0]==NONE:
                    messagebox.showerror("Error","Invalid user EmployeeID|Password",parent=self.root)
                elif user[0]=="Admin":
                        self.root.destroy()
                        os.system("C:/ProgramData/Anaconda3/python.exe d:/project1/dashboard.py")
                else:
                    self.root.destroy()
                    os.system("C:/ProgramData/Anaconda3/python.exe d:/project1/billing.py")    
        except Exception as ex:
            messagebox.showerror("Error",f"Error Due to {str(ex)}",parent=self.root)            
          
        


# if __name__=="__main__":
root=Tk()
obj=Login_System(root)
root.mainloop()