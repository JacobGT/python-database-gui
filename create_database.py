from tkinter import *
from PIL import ImageTk, Image
import sqlite3

root = Tk()
root.title('Database GUI')
root.geometry('450x600')

# There is all ready a tutorial on SQLite3 in my github profile: https://github.com/JacobGT/SQLite3PythonTutorial

# Create or connect to a database
conn = sqlite3.connect('contacts.db')
# Create cursor
c = conn.cursor()

# We only need to create a table one time / execute only once to create db
# Create table
c.execute("""CREATE TABLE contact_info (
        first_name text,
        last_name text,
        number text,
        age integer,
        address text
)""")

# Commit changes to database
conn.commit()
# Close connection
conn.close()

# Show completion
id_label = Label(root, text="Database Created Succesfully")
id_label.pack()


root.mainloop()
