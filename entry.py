from tkinter import *
from tkinter import messagebox
import sqlite3

root = Tk()
root.title('Database GUI')
root.geometry('450x600')

# Create or connect to a database
conn = sqlite3.connect('contacts.db')
# Create cursor
c = conn.cursor()

# GUI
# Create Input Entry Box
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20)
l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)
number = Entry(root, width=30)
number.grid(row=2, column=1)
age = Entry(root, width=30)
age.grid(row=3, column=1)
address = Entry(root, width=30)
address.grid(row=4, column=1)
id = Entry(root, width=30)
id.grid(row=9, column=1, pady=5)

# Create Label
f_name_label = Label(root, text="First Name: ", anchor=W)
f_name_label.grid(row=0, column=0, pady=10, sticky=W+E)
l_name_label = Label(root, text="Last Name: ", anchor=W)
l_name_label.grid(row=1, column=0, pady=10, sticky=W+E)
number_label = Label(root, text="Phone Number: ", anchor=W)
number_label.grid(row=2, column=0, pady=10, sticky=W+E)
age_label = Label(root, text="Age: ", anchor=W)
age_label.grid(row=3, column=0, pady=10, sticky=W+E)
address_label = Label(root, text="Address: ", anchor=W)
address_label.grid(row=4, column=0, sticky=W+E)
id_label = Label(root, text="Select ID")
id_label.grid(row=9, column=0, pady=5)

# Functions for buttons
def submit():
    # Check for valid info
    if (f_name.get() == "" and l_name.get() == ""):
        messagebox.showerror("Invalid Information", "There is nothing in First and/or Last Name.")
    else:
        # Create or connect to a database
        conn = sqlite3.connect('contacts.db')
        # Create cursor
        c = conn.cursor()
        # Insert into table
        c.execute("INSERT INTO contact_info VALUES (:f_name, :l_name, :number, :age, :address)",
                {
                    'f_name': f_name.get(),
                    'l_name': l_name.get(),
                    'number': number.get(),
                    'age': age.get(),
                    'address': address.get()
                })
        # Commit changes to database
        conn.commit()
        # Close connection
        conn.close()
        # Clear the entry boxes
        f_name.delete(0, END)
        l_name.delete(0, END)
        number.delete(0, END)
        age.delete(0, END)
        address.delete(0, END)

def query():
    # Create or connect to a database
    conn = sqlite3.connect('contacts.db')
    # Create cursor
    c = conn.cursor()
    # Query DB
    c.execute("SELECT *, rowid from contact_info")
    # Clear the entry boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    number.delete(0, END)
    age.delete(0, END)
    address.delete(0, END)
    # Loop through results
    records = c.fetchall()
    print_records = ''
    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + " " + "\t" + str(record[5]) + "\n"
    try:
        global query_label
        query_label.config(text=print_records)
    except:
        query_label = Label(root, text=print_records)
        query_label.grid(row=12, column=0, columnspan=2)

    # Ignore~~~
    """results = c.fetchall()
    for result in results:
        f_name.insert(0, result[0])
        l_name.insert(0, result[1])
        number.insert(0, result[2])
        age.insert(0, result[3])
        address.insert(0, result[4])"""
    # ~~~

    # Commit changes to database
    conn.commit()
    # Close connection
    conn.close()

# Delete a Record
def delete():
    # Create a database or connect to one
    conn = sqlite3.connect('contacts.db')
    # Create cursor
    c = conn.cursor()
    # Delete a record
    c.execute("DELETE from contact_info WHERE oid = " + id.get())
    id.delete(0, END)
    # Commit Changes
    conn.commit()
    # Close Connection
    conn.close()

# Update a record I
def update():
    # Create a database or connect to one
    conn = sqlite3.connect('contacts.db')
    # Create cursor
    c = conn.cursor()
    record_id = id.get()

    c.execute("""UPDATE contact_info SET
		first_name = :first,
		last_name = :last,
		number = :number,
		age = :age,
		address = :address
	    WHERE oid = :oid""",
		{
		'first': f_name_editor.get(),
		'last': l_name_editor.get(),
        'number': number_editor.get(),
        'age': age_editor.get(),
        'address': address_editor.get(),
		'oid': record_id
		})
    #Commit Changes
    conn.commit()
    # Close Connection
    conn.close()
    editor.destroy()
    root.deiconify()

# Update a record II
def edit():
    root.withdraw()
    global editor
    editor = Tk()
    editor.title('Update A Record')
    editor.geometry("400x300")
    # Create a database or connect to one
    conn = sqlite3.connect('contacts.db')
    # Create cursor
    c = conn.cursor()
    record_id = id.get()
    # Query the database
    c.execute("SELECT * FROM contact_info WHERE oid = " + record_id)
    records = c.fetchall()

    # Create Global Variables for text box names
    global f_name_editor
    global l_name_editor
    global address_editor
    global number_editor
    global age_editor

    # Create Text Boxes
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1)
    number_editor = Entry(editor, width=30)
    number_editor.grid(row=2, column=1)
    age_editor = Entry(editor, width=30)
    age_editor.grid(row=3, column=1)
    address_editor = Entry(editor, width=30)
    address_editor.grid(row=4, column=1)

    # Create Text Box Labels
    f_name_label = Label(editor, text="First Name")
    f_name_label.grid(row=0, column=0, pady=(10, 0))
    l_name_label = Label(editor, text="Last Name")
    l_name_label.grid(row=1, column=0)
    number_label = Label(editor, text="Number")
    number_label.grid(row=2, column=0)
    age_label = Label(editor, text="Age")
    age_label.grid(row=3, column=0)
    address_label = Label(editor, text="Address")
    address_label.grid(row=4, column=0)

    # Loop though results
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        number_editor.insert(0, record[2])
        age_editor.insert(0, record[3])
        address_editor.insert(0, record[4])

    # Create a Save Button To Save edited record
    edit_btn = Button(editor, text="Save Record", command=update)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

# Create buttons
submit_btn = Button (root, text="Add Contact Info", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
query_btn = Button(root, text="Show Contacts", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=140)
delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=140)
edit_btn = Button(root, text="Edit Record", command=edit)
edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=140)

# Commit changes to database
conn.commit()
# Close connection
conn.close()

root.mainloop()
