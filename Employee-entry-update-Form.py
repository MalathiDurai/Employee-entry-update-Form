from tkinter import *
from tkinter import messagebox, ttk
import cx_Oracle
from functools import partial


def insert_details(name, phone_number, aadhar, address, education, salary):
    dsn = cx_Oracle.makedsn('localhost', '1521', sid='xe')
    connection = cx_Oracle.connect(user='hr', password='hr_new2', dsn=dsn)
    cursor = connection.cursor()
    try:
        insert_query = 'insert into bunk_employees (name, phone_number, aadhar, address, education, salary) values( :1, :2, :3, :4, :5, :6)'
        cursor.execute(insert_query, (name, phone_number, aadhar, address, education, salary))
        connection.commit()
        messagebox.showinfo("Success", "Employee details saved successfully.")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f'Database Error Occurred: {error.message}')
        connection.rollback()
        messagebox.showerror("Error", f"Database Error Occurred: {error.message}")
    finally:
        cursor.close()
        connection.close()


def get_details():
    name = name_entry.get()
    phone_number = phone_number_entry.get()
    aadhar = AADHAR_entry.get()
    address = Address_entry.get()
    education = Education_entry.get()
    salary = Current_salary_entry.get()
    insert_details(name, phone_number, aadhar, address, education, salary)
    name_entry.delete(0, END)
    phone_number_entry.delete(0, END)
    AADHAR_entry.delete(0, END)
    Address_entry.delete(0, END)
    Education_entry.delete(0, END)
    Current_salary_entry.delete(0, END)


def update_entry(column_name):
    id_button = Button(update_frame, text="Employee ID")
    id_entry = Entry(update_frame)
    u_old = Label(update_frame, text="Enter Old Detail :")
    u_entry_old = Entry(update_frame)
    u_new = Label(update_frame, text="Enter new Detail :")
    u_entry_new = Entry(update_frame)

    id_button.pack(side=LEFT)
    id_entry.pack(side=LEFT)
    u_old.pack(side=LEFT)
    u_entry_old.pack(side=LEFT)
    u_new.pack(side=LEFT)
    u_entry_new.pack(side=LEFT)
    b_update = Button(master=update_frame, text="Click here to update", font=font, fg=fg, bg=bg,
                      width=20,
                      command=partial(update_data, column_name, id_entry, u_entry_old, u_entry_new))
    b_update.pack(side=LEFT)


def update_data(column_name, id_entry, u_entry_old, u_entry_new):
    id_entry = id_entry.get()
    old_value = u_entry_old.get()
    new_value = u_entry_new.get()
    dsn = cx_Oracle.makedsn('localhost', '1521', sid='xe')
    connection = cx_Oracle.connect(user='hr', password='hr_new2', dsn=dsn)
    cursor = connection.cursor()
    try:
        update_query = f'UPDATE bunk_employees set {column_name} = :new_value WHERE {column_name} = :old_value and ID = : id_entry'
        cursor.execute(update_query, id_entry=id_entry, new_value=new_value, old_value=old_value)
        connection.commit()
        messagebox.showinfo("Success", "Entry updated successfully")
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        connection.close()


def display_entry(id_entry):
    dsn = cx_Oracle.makedsn('localhost', '1521', sid='xe')
    connection = cx_Oracle.connect(user='hr', password='hr_new2', dsn=dsn)
    cursor = connection.cursor()
    try:
        name_display_query = f'''
            SELECT NAME, PHONE_NUMBER, AADHAR, ADDRESS, EDUCATION, SALARY
            FROM bunk_employees 
            WHERE ID = :id
        '''
        cursor.execute(name_display_query, id=id_entry.get())
        result = cursor.fetchone()
        if result:
            name, phone_number, aadhar, address, education, salary = result

            labels_texts = ["Name:", "Phone Number:", "Aadhar:", "Address:", "Education:", "Salary:"]
            entry_values = [name, phone_number, aadhar, address, education, salary]

            for label_text, entry_value in zip(labels_texts, entry_values):
                row_frame = Frame(master=display_frame, bg=bg)
                row_frame.pack(fill='x', pady=5)

                label = Label(master=row_frame, text=label_text, font=font, fg=fg, bg=bg, width=20)
                label.pack(side=LEFT, padx=5)

                entry = Entry(master=row_frame, font="#000066", width=100)
                entry.pack(side=LEFT, padx=5)
                entry.insert(0, entry_value)

            b_display = Button(display_frame, text="Click here to check for another employee", font=font, fg=fg, bg=bg,
                               width=50, command=partial(display_entry, id_entry))
            b_display.pack(pady=10)

            messagebox.showinfo("Success", "Employee details found")
        else:
            messagebox.showinfo("Error", "Employee not found")
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        connection.close()


def create_window1(window):
    center_label = Label(master=window, text="New Employee Entry Form", font=font, fg=fg, bg=bg, width=100)
    center_label.pack()
    center_button = Button(master=window, text="Type your details below & Click here to add your details",
                           font=font, fg=fg, bg=bg, width=50, command=get_details)
    center_button.pack()
    lf = LabelFrame(master=window, text="Employee Information", font=font, padx=50, pady=50)
    lf.pack()
    global name_entry, phone_number_entry, AADHAR_entry, Address_entry, Education_entry, Current_salary_entry
    Name_label = Label(master=lf, text="Enter your name here : ", font=font, fg=fg, bg=bg, width=40, anchor="w")
    Name_label.pack()
    name_entry = Entry(master=lf, font=font)
    name_entry.pack()
    Phone_number_label = Label(master=lf, text="Enter your phone number here :", font=font, fg=fg, bg=bg, width=40,
                               anchor="w")
    Phone_number_label.pack()
    phone_number_entry = Entry(master=lf, font=font)
    phone_number_entry.pack()
    AADHAR_label = Label(master=lf, text="Enter your AADHAR number here : ", font=font, fg=fg, bg=bg, width=40,
                         anchor="w")
    AADHAR_label.pack()
    AADHAR_entry = Entry(master=lf, font=font)
    AADHAR_entry.pack()
    Address_label = Label(master=lf, text="Enter your Address here :", font=font, fg=fg, bg=bg, width=40, anchor="w")
    Address_label.pack()
    Address_entry = Entry(master=lf, font=font)
    Address_entry.pack()
    Education_label = Label(master=lf, text="Enter your Education qualification here : ", font=font, fg=fg, bg=bg,
                            width=40, anchor="w")
    Education_label.pack()
    Education_entry = Entry(master=lf, font=font)
    Education_entry.pack()
    Current_salary_label = Label(master=lf, text="Enter your Current Salary here :", font=font, fg=fg, bg=bg, width=40,
                                 anchor="w")
    Current_salary_label.pack()
    Current_salary_entry = Entry(master=lf, font=font)
    Current_salary_entry.pack()


def create_window2(window):
    global display_frame
    display_frame = Frame(window)
    display_frame.pack(fill='both', expand=True)
    id_label = Label(master=display_frame, text="Employee ID : ", font=font, fg=fg, bg=bg, anchor="w")
    id_label.pack(pady=5)
    id_entry = Entry(master=display_frame, font=font)
    id_entry.pack(pady=5)
    b_display = Button(display_frame, text="Enter your ID and Click here to get your details", font=font, fg=fg, bg=bg,
                       width=50,
                       command=partial(display_entry, id_entry))
    b_display.pack(pady=5)


def create_window3(window):
    global update_frame
    update_frame = Frame(window)
    update_frame.pack(fill='both', expand=True)

    lbl = Label(update_frame, text="Click on below item to update", font=font, fg="black", bg="white", height=2,
                width=50)
    lbl.pack()
    b_update_pn = Button(update_frame, text="Phone Number", font=font, fg=fg, bg=bg, width=20,
                         command=partial(update_entry, column_name="phone_number"))
    b_update_aadhar = Button(update_frame, text="Aadhar", font=font, fg=fg, bg=bg, width=20,
                             command=partial(update_entry, column_name="aadhar"))
    b_update_address = Button(update_frame, text="Address", font=font, fg=fg, bg=bg, width=20,
                              command=partial(update_entry, column_name="address"))
    b_update_edu = Button(update_frame, text="Education", font=font, fg=fg, bg=bg, width=20,
                          command=partial(update_entry, column_name="education"))
    b_update_sal = Button(update_frame, text="Salary", font=font, fg=fg, bg=bg, width=20,
                          command=partial(update_entry, column_name="salary"))

    b_update_pn.pack(pady=5)
    b_update_aadhar.pack(pady=5)
    b_update_address.pack(pady=5)
    b_update_edu.pack(pady=5)
    b_update_sal.pack(pady=5)


window = Tk()
window.configure(bg='#b3ecff')
window.title('Employee Management System')

font = ("Helvetica", 16, "bold")
fg = "#ffffff"
bg = "#000066"

notebook = ttk.Notebook(window)
notebook.pack(fill='both', expand=True)

tab1 = ttk.Frame(notebook)
create_window1(tab1)
notebook.add(tab1, text='New Employee Entry')

tab2 = ttk.Frame(notebook)
create_window2(tab2)
notebook.add(tab2, text='Display Employee Details')

tab3 = ttk.Frame(notebook)
create_window3(tab3)
notebook.add(tab3, text='Update Employee Details')

window.mainloop()
