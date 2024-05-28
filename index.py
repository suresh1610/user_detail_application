# main.py
import tkinter as tk
from tkinter import ttk
from tkinter import *
import psycopg2
import re
from tkinter import messagebox
from tkinter.messagebox import askokcancel, WARNING
from tkinter import simpledialog

from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

def clear_frame():
    for widgets in user_detail_frame.winfo_children():
        widgets.destroy()

def view_user(id):

    view_window = tk.Tk()
    view_window.title("user detail")
    view_window.geometry("1000x700")
    view_window.resizable(False, False)

    def edit(id, num):
        if num == 1:
            edit_name = tk.simpledialog.askstring("Edit task", "Enter your new task name:")
            if edit_name:
                if validate_name(edit_name):
                    edit_query = "update user_details set first_name=%s where user_id=%s"
                    edit_data = (edit_name, id)
                    pointer.execute(edit_query, edit_data)
                    connection.commit()
                else:
                    messagebox.showerror("Invalid data", "Enter valid name")

        elif num == 2:
                edit_name = tk.simpledialog.askstring("Edit task", "Enter your new task name:")
                if edit_name:
                    if validate_name(edit_name):
                        edit_query = "update user_details set last_name=%s where user_id=%s"
                        edit_data = (edit_name, id)
                        pointer.execute(edit_query, edit_data)
                        connection.commit()
                    else:
                         messagebox.showerror("Invalid data", "Enter valid name")
                         
        elif num == 3:
                edit_name = tk.simpledialog.askstring("Edit task", "Enter your mail:")
                if edit_name:
                    if validate_email(edit_name):
                        edit_query = "update user_details set email_id=%s where user_id=%s"
                        edit_data = (edit_name, id)
                        pointer.execute(edit_query, edit_data)
                        connection.commit()
                        messagebox.showinfo("update msg", "Your data updated successfully")
                    else:
                        messagebox.showerror("Invalid data", "Enter valid mail")
                     
        elif num == 4:
                edit_name = tk.simpledialog.askstring("Edit task", "Enter your new task name:")
                if edit_name:
                    edit_query = "update user_details set dob=%s where user_id=%s"
                    edit_data = (edit_name, id)
                    pointer.execute(edit_query, edit_data)
                    connection.commit()

    # view_details_frame = Frame(view_window)
    # view_details_frame.pack(fill='both', expand=True)

    query = "select * from user_details where user_id = %s"
    data = (id,)
    pointer.execute(query, data)
    user_data = pointer.fetchall()

    for u_data in user_data:

        user_id, first_name, last_name, email_id, dob = u_data

        userid_label = tk.Label(view_window, text="🆔user id:", font=('Consolas', 15))
        userid_label.place(relx=0.29, rely=0.1, anchor="center")

        userid_display = tk.Label(view_window, text=user_id, font=('Consolas', 15))
        userid_display.place(relx=0.535, rely=0.1, anchor='center')

        firstN_label = tk.Label(view_window, text="first name:", font=('Consolas', 15))
        firstN_label.place(relx=0.3, rely=0.2, anchor="center")

        firstN_display = tk.Label(view_window, text=first_name, font=('Consolas', 15))
        firstN_display.place(relx=0.5, rely=0.18)

        firstN_edit = ttk.Button(view_window, text="🖊️", command=lambda id = id, num=1 :edit(id,num))
        firstN_edit.place(relx=0.38, rely=0.18, width=30)

        seperator_line_fname = ttk.Separator(view_window, orient='horizontal')
        seperator_line_fname.place(relx=0, rely=0.32, width='2000')

        lastN_label = tk.Label(view_window, text="last name:", font=('Consolas', 15))
        lastN_label.place(relx=0.3, rely=0.38, anchor="center")

        lastN_display = tk.Label(view_window, text=last_name, font=('Consolas', 15))
        lastN_display.place(relx=0.535, rely=0.38, anchor="center")

        lastN_edit = ttk.Button(view_window, text="🖊️", command=lambda id = id, num= 2 :edit(id, num))
        lastN_edit.place(relx=0.38, rely=0.36, width=30)

        seperator_line_lname = ttk.Separator(view_window, orient='horizontal')
        seperator_line_lname.place(relx=0, rely=0.48, width='2000')

        email_label = tk.Label(view_window, text="📧email:", font=('Consolas', 15))
        email_label.place(relx=0.28, rely=0.53, anchor="center")

        email_display = tk.Label(view_window, text=email_id, font=('Consolas', 15))
        email_display.place(relx=0.62, rely=0.53, anchor="center")

        emailN_edit = ttk.Button(view_window, text="🖊️", command=lambda id = id, num=3 :edit(id, num))
        emailN_edit.place(relx=0.34, rely=0.51, width=30)

        seperator_line_email = ttk.Separator(view_window, orient='horizontal')
        seperator_line_email.place(relx=0, rely=0.66, width='2000')

        dob_label = tk.Label(view_window, text="📅Data of Birth:", font=('Consolas', 15))
        dob_label.place(relx=0.33, rely=0.7, anchor="center")

        dob_display = tk.Label(view_window, text=dob, font=('Consolas', 15))
        dob_display.place(relx=0.6, rely=0.7, anchor="center")

        dob_v_edit = ttk.Button(view_window, text="🖊️", command=lambda id = id, num=3 :edit(id, num))
        dob_v_edit.place(relx=0.45, rely=0.68, width="30")

        seperator_line_dob = ttk.Separator(view_window, orient='horizontal')
        seperator_line_dob.place(relx=0, rely=0.8, width='2000')

    view_window.mainloop()

def delete_user(id):
    ans = askokcancel(title="delete task", message="are you sure?", icon=WARNING)
    if ans:
            delete_query = "delete from user_details where user_id=%s"
            data = (id,)
            pointer.execute(delete_query, data)
            connection.commit()
            clear_frame()
            load_user()
            messagebox.showinfo("delete message", "Data deleted successfully")
    else:
            messagebox.showinfo("delete message", "Data deletion failed")

def validate_name(username):
        return bool(re.match(r'^[A-Za-z]+$', username))

def validate_email(mail):
        return bool(re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', mail))

def add_data():
    # def validate_name(username):
    #     return bool(re.match(r'^[A-Za-z]+$', username))

    # def validate_email(mail):
    #     return bool(re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', mail))
    
    f_name = firstname_entry.get()
    l_name = lastname_entry.get()
    mail = email_entry.get()
    dob = dob_entry.get()

    if not validate_name(f_name) or not validate_name(l_name):
        messagebox.showerror("Invalid data", "Enter valid first name or last name")
        return
    elif not validate_email(mail):
        messagebox.showerror("Invalid data", "Enter valid email address")
        return
    elif validate_name(f_name) and validate_name(l_name) and validate_email(mail):
            try:
                insert_query = 'insert into user_details(first_name, last_name, email_id, dob) values(%s, %s, %s, %s)'
                date = (f_name, l_name, mail,dob)
                pointer.execute(insert_query, date)
                connection.commit()
                messagebox.showinfo("Data Add","your data is successfully registered")
                clear_frame()
                load_user()
                firstname_entry.delete(0, END)
                lastname_entry.delete(0, END)
                email_entry.delete(0, END)
                dob_entry.delete(0, END)
                return
            except psycopg2.errors.DatetimeFieldOverflow as error:
                messagebox.showerror("Invalid Input", "Enter valid data of birth")
                connection.rollback()
    
def load_user():
     
    query = "select user_id,first_name from user_details"
    pointer.execute(query)
    details = pointer.fetchall()


    for data in details:
        user_id, first_name = data
        name_frame = tk.Frame(user_detail_frame)
        name_frame.pack(fill='x', pady=5, padx=5)

        name = first_name.capitalize()

        user_emoji = tk.Label(name_frame, text= "👤", font=('Consolas', 20))
        user_emoji.pack(side="left")

        user_name = tk.Label(name_frame, text= name, font=('Consolas', 20))
        user_name.pack(side="left")

        view_btn = ttk.Button(name_frame, text="view", command=lambda user_id=user_id: view_user(user_id))
        view_btn.pack(side="right")

        delete_btn = ttk.Button(name_frame, text="delete", command=lambda user_id=user_id: delete_user(user_id))
        delete_btn.pack(side="right")
         
main_root = Tk()
main_root.title("user application")
main_root.state("zoomed")
main_root.resizable(True, True)

connection = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="12345",
    port=5432
)

pointer = connection.cursor()
create_query = '''create table if not exists user_details(
                user_id serial primary key,
                first_name text,
                last_name text,
                email_id text,
                dob date
                )'''

pointer.execute(create_query,)
print("table created")

user_frame = tk.Frame(main_root, width=300, height=400, bg='#ffffff')
user_frame.pack(side='left', fill='both', expand=True)

user_detail_frame = Frame(main_root,width=300, height=400, bg='#ffffff')
user_detail_frame.pack(side='right', fill='both', expand=True, padx=5)

login_label = tk.Label(user_frame, text="Enter user details", font=('Consolas', 30),bg='#ffffff')
login_label.place(relx=0.5, rely=0.1, anchor="center")

firstname_label = tk.Label(user_frame, text="👤first name:", font=('Consolas', 20), bg='#ffffff')
firstname_label.place(relx=0.2, rely=0.18, anchor="center")

firstname_entry = ttk.Entry(user_frame, font=('Consolas', 20))
firstname_entry.place(relx=0.6, rely=0.18, anchor="center", width=300)
firstname_entry.focus()

lastname_label = tk.Label(user_frame, text="👤last name:", font=('Consolas', 20), bg='#ffffff')
lastname_label.place(relx=0.19, rely=0.24, anchor="center")

lastname_entry = ttk.Entry(user_frame, font=('Consolas', 20))
lastname_entry.place(relx=0.6, rely=0.24, anchor="center", width=300)

email_label = tk.Label(user_frame, text="📧email:", font=('Consolas', 20), bg='#ffffff')
email_label.place(relx=0.15, rely=0.3, anchor="center")

email_entry = ttk.Entry(user_frame, font=('Consolas', 20))
email_entry.place(relx=0.6, rely=0.3, anchor="center", width=300)

dob_label = tk.Label(user_frame, text="📅data of birth:", font=('Consolas', 20), bg='#ffffff')
dob_label.place(relx=0.22, rely=0.35, anchor="center")

dob_format = tk.Label(user_frame, text='(yyyy/mm/dd)',font=('Consolas', 15), bg='#ffffff')
dob_format.place(relx = 0.2, rely=0.38, anchor="center")

dob_entry = ttk.Entry(user_frame, font=('Consolas', 20))
dob_entry.place(relx=0.6, rely=0.35, anchor='center', width="300")

submit_btn = tk.Button(user_frame, text="submit",font=('Consolas', 15), cursor="hand2",bg='#ffffff', command=add_data)
submit_btn.place(relx=0.3, rely=0.45, width=200)


load_user()

connection.commit()
main_root.mainloop()