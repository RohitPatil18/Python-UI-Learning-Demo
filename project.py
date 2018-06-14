#Project --> Student Management system

from tkinter import *
import cx_Oracle
from tkinter import scrolledtext
from tkinter import messagebox
import time
import Weather
import Validate
import pygame.mixer
import time


#-----------------------Play success notification------------------------
def success() :
    pygame.mixer.init()
    pygame.mixer.music.load("success_notification.mp3")
    pygame.mixer.music.play()

#----------------------- Refresh data info ------------------------------
def refreshinfo() :
    con = None
    cursor = None
    try :
        con = cx_Oracle.connect("system/abc123")
        cursor = con.cursor()
        print("Connected.")

        sql = "select * from student order by Rno"
        cursor.execute(sql)
        data = cursor.fetchall()

        info = ''

        for d in data :
            info = info + "Roll No : "+str(d[0])+"    Name : "+d[1]+"\n"

        scText.insert(INSERT,info)

    except cx_Oracle.DatabaseError as e :
            print("Issue : "+str(e))
            messagebox.showerror("Issue",str(e))
            con.rollback()

    finally :
        if cursor is not None  :
            cursor.close()
        if con is not None :
            con.close()
            print("Disconnect.")
#---------------------------------------------------------------------------



width = 400
height = 350


#-----------------------Flashscreen--------------------------------------
flash = Tk()
x = (flash.winfo_screenwidth() // 2) - (width // 2)
y = (flash.winfo_screenheight() // 2) - (height // 2)
flash.title("")
flash.geometry('{}x{}+{}+{}'.format(width, height, x, y))



def flash_to_root() :
    root.deiconify()
    flash.withdraw()


lblWelcome = Label(flash,text="WELCOME",font=("ariel", 25, 'bold'))
lblWeather = Label(flash,text="Getting location info...")


lblWelcome.pack(pady=30)
lblWeather.pack(pady=10)

def loc_info() :
    lblWeather.configure(text = Weather.weather())
    flash.after(3000, flash_to_root)

flash.after(100,loc_info)


root = Toplevel(flash)
root.title("Student Management System")
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
root.withdraw()


#------------------ ADD Window ------------------------------------------
addwin = Toplevel(root)
addwin.title("Add Student")
addwin.geometry('{}x{}+{}+{}'.format(width, height, x, y))
addwin.withdraw()

lblRnoAdd = Label(addwin,text="Roll No : ")
enRnoAdd = Entry(addwin,bd=5)
lblNameAdd = Label(addwin,text="Name : ")
enNameAdd = Entry(addwin,bd=5)

def saveAdd() :
    con = None
    cursor = None
    try :
        con = cx_Oracle.connect("system/abc123")
        cursor = con.cursor()
        print("Connected.")

        try :
            rno = int(enRnoAdd.get())

            if rno < 1 :
                messagebox.showerror("Issue","Invalid input : Roll No, Enter positive integers only.")
                enRnoAdd.delete(0,END)
                enRnoAdd.focus()
                return

        except ValueError :
            messagebox.showerror("Issue","Invalid input : Roll No, Enter integers only.")
            enRnoAdd.delete(0,END)
            enRnoAdd.focus()
            return

        rname = enNameAdd.get()

        if Validate.validate(rname) == False :
            messagebox.showerror("Issue","Invalid input : Name")
            enNameAdd.delete(0,END)
            return

        sql = "insert into student values(%d,'%s')"
        args = (rno,rname)
        cursor.execute(sql%args)
        print(cursor.rowcount,"rows inserted.")
        if cursor.rowcount == 1 :
            success()
            messagebox.showinfo("Issue","Student record successfully added.")
            con.commit()
            enRnoAdd.delete(0,END)
            enRnoAdd.focus()
            enNameAdd.delete(0,END)
        else :
            messagebox.showerror("Issue","Something went wrong.")

    except cx_Oracle.DatabaseError as e :
            print("Issue : "+str(e))
            messagebox.showerror("Issue",str(e))
            con.rollback()

    finally :
        if cursor is not None  :
            cursor.close()
        if con is not None :
            con.close()
            print("Disconnect.")

btnSaveAdd = Button(addwin,text="Save",width=10,command=saveAdd)

def backAdd() :
    root.deiconify()
    addwin.withdraw()
btnBackAdd = Button(addwin,text="Back",width=10,command=backAdd)

lblRnoAdd.pack(pady=10)
enRnoAdd.pack(pady=5)
lblNameAdd.pack(pady=5)
enNameAdd.pack(pady=5)
btnSaveAdd.pack(pady=5)
btnBackAdd.pack(pady=5)

#-------------------------------------------------------------------------

#------------------ View Window ------------------------------------------

viwin = Toplevel(root)
viwin.title("View Student")
viwin.geometry('{}x{}+{}+{}'.format(width, height, x, y))
viwin.withdraw()

scText = scrolledtext.ScrolledText(viwin,width=40,height=15)

def backView() :
    root.deiconify()
    viwin.withdraw()
    scText.delete("1.0",END)

btnBackView = Button(viwin,text="Back",width=10,command=backView)

scText.pack(pady=10)
btnBackView.pack(pady=10)
#-------------------------------------------------------------------------


#------------------ Update Window ----------------------------------------
updatewin = Toplevel(root)
updatewin.title("Update Student")
updatewin.geometry('{}x{}+{}+{}'.format(width, height, x, y))
updatewin.withdraw()

lblRnoUpdate = Label(updatewin,text="Roll No : ")
enRnoUpdate = Entry(updatewin,bd=5)
lblNameUpdate = Label(updatewin,text="Name : ")
enNameUpdate = Entry(updatewin,bd=5)

def saveUpdate() :
    con = None
    cursor = None
    try :
        con = cx_Oracle.connect("system/abc123")
        cursor = con.cursor()
        print("Connected.")

        try :
            rno = int(enRnoUpdate.get())

            if rno < 1 :
                messagebox.showerror("Issue","Invalid input : Roll No, Enter positive integers only.")
                enRnoUpdate.delete(0,END)
                enRnoUpdate.focus()
                return

        except ValueError :
            messagebox.showerror("Issue","Invalid input : Roll No, Enter integers only.")
            enRnoUpdate.delete(0,END)
            enRnoUpdate.focus()
            return

        rname = enNameUpdate.get()

        if Validate.validate(rname) == False :
            messagebox.showerror("Issue","Invalid input : Name")
            enRnoUpdate.delete(0,END)
            return

        sql = "update student set rname ='%s' where rno = %d"
        args = (rname,rno)
        cursor.execute(sql%args)
        con.commit()
        print(cursor.rowcount," Updated")

        if cursor.rowcount == 0 :
            messagebox.showerror("Issue","Student record not found.")
        else :
            messagebox.showinfo("Issue","Student record successfully updated.")
            enRnoUpdate.delete(0,END)
            enRnoUpdate.focus()
            enNameUpdate.delete(0,END)

    except cx_Oracle.DatabaseError as e :
            print("Issue : "+str(e))
            messagebox.showerror("Issue",str(e))
            con.rollback()

    finally :
        if cursor is not None  :
            cursor.close()
        if con is not None :
            con.close()
            print("Disconnect.")

btnSaveUpdate = Button(updatewin,text="Save",width=10,command=saveUpdate)

def backUpdate() :
    root.deiconify()
    updatewin.withdraw()
btnBackUpdate = Button(updatewin,text="Back",width=10,command=backUpdate)

lblRnoUpdate.pack(pady=10)
enRnoUpdate.pack(pady=5)
lblNameUpdate.pack(pady=5)
enNameUpdate.pack(pady=5)
btnSaveUpdate.pack(pady=5)
btnBackUpdate.pack(pady=5)
#-------------------------------------------------------------------------


#------------------ Delete Window ----------------------------------------
delwin = Toplevel(root)
delwin.title("View Student")
delwin.geometry('{}x{}+{}+{}'.format(width, height, x, y))
delwin.withdraw()

lblRnoDelete = Label(delwin,text="Roll No : ")
enRnoDelete = Entry(delwin,bd=5)

def saveDelete() :
    con = None
    cursor = None
    try :
        con = cx_Oracle.connect("system/abc123")
        cursor = con.cursor()
        print("Connected.")

        try :
            rno = int(enRnoDelete.get())

            if rno < 1 :
                messagebox.showerror("Issue","Invalid imput : Roll No, Enter positive integers only.")
                enRnoDelete.delete(0,END)
                enRnoDelete.focus()
                return

        except ValueError :
            messagebox.showerror("Issue","Invalid input : Roll No, Enter integers only.")
            enRnoDelete.delete(0,END)
            enRnoDelete.focus()
            return

        sql = "delete from student where rno = %d"
        args = (rno)
        cursor.execute(sql%args)
        con.commit()
        print(cursor.rowcount," Deleted.")
        if cursor.rowcount == 0 :
            messagebox.showerror("Issue","Student record not found.")
        else :
            messagebox.showinfo("Issue","Student record successfully deleted.")
            enRnoDelete.delete(0,END)
            enRnoDelete.focus()

    except cx_Oracle.DatabaseError as e :
            print("Issue : "+str(e))
            messagebox.showerror("Issue",str(e))
            con.rollback()

    finally :
        if cursor is not None  :
            cursor.close()
        if con is not None :
            con.close()
            print("Disconnect.")

btnSaveDelete = Button(delwin,text="Delete",width=10,command=saveDelete)

def backDelete() :
    root.deiconify()
    delwin.withdraw()
btnBackDelete = Button(delwin,text="Back",width=10,command=backDelete)

lblRnoDelete.pack(pady=10)
enRnoDelete.pack(pady=5)
btnSaveDelete.pack(pady=5)
btnBackDelete.pack(pady=5)

#-------------------------------------------------------------------------


def to_add() :
    addwin.deiconify()
    root.withdraw()

def to_view() :
    refreshinfo()
    viwin.deiconify()
    root.withdraw()

def to_update() :
    updatewin.deiconify()
    root.withdraw()

def to_delete() :
    delwin.deiconify()
    root.withdraw()

btnAdd = Button(root,text="Add",width=10,height=2,command=to_add)
btnView = Button(root,text="View",width=10,height=2,command=to_view)
btnUpdate = Button(root,text="Update",width=10,height=2,command=to_update)
btnDelete = Button(root,text="Delete",width=10,height=2,command=to_delete)

btnAdd.pack(pady=20)
btnView.pack(pady=10)
btnUpdate.pack(pady = 10)
btnDelete.pack(pady=10)

root.mainloop()
