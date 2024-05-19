import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3


with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
db.commit()
db.close()

class PasswordGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Password Generator')
        self.master.geometry('660x500')
        self.master.config(bg='#000080')  
        self.master.resizable(False, False)

        self.username = StringVar()
        self.passwordlen = IntVar(value=12)  
        self.generatedpassword = StringVar()

        Label(self.master, text=":PASSWORD GENERATOR:", fg='white', bg='#000080', font='Helvetica 20 bold underline').grid(row=0, column=1, pady=10)

        Label(self.master, text="Enter User Name: ", font='Arial 15 bold', bg='#000080', fg='white').grid(row=1, column=0, pady=10)
        self.username_entry = Entry(self.master, textvariable=self.username, font='Arial 15', bd=6, relief='ridge')
        self.username_entry.grid(row=1, column=1)

        Label(self.master, text="Enter Password Length: ", font='Arial 15 bold', bg='#000080', fg='white').grid(row=2, column=0, pady=10)
        self.length_entry = Entry(self.master, textvariable=self.passwordlen, font='Arial 15', bd=6, relief='ridge')
        self.length_entry.grid(row=2, column=1)

        Label(self.master, text="Generated Password: ", font='Arial 15 bold', bg='#000080', fg='white').grid(row=3, column=0, pady=10)
        self.password_entry = Entry(self.master, textvariable=self.generatedpassword, font='Arial 15', bd=6, relief='ridge', fg='#DC143C')
        self.password_entry.grid(row=3, column=1)

        Button(self.master, text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='Verdana 15 bold', fg='white', bg='#0000CD', command=self.generate_pass).grid(row=4, column=1, pady=20)
        Button(self.master, text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='white', bg='#1E90FF', command=self.accept_fields).grid(row=5, column=1, pady=10)
        Button(self.master, text="RESET", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='white', bg='#4682B4', command=self.reset_fields).grid(row=6, column=1, pady=10)

    def generate_pass(self):
        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        digits = string.digits
        symbols = string.punctuation

        name = self.username.get()
        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for password length")
            return

        if name == "":
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error", "Name must be a string")
            self.username_entry.delete(0, END)
            return

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        self.password_entry.delete(0, END)

        password = (
            random.sample(upper, 1) +
            random.sample(lower, 1) +
            random.sample(digits, 1) +
            random.sample(symbols, 1) +
            random.choices(upper + lower + digits + symbols, k=length-4)
        )
        random.shuffle(password)
        gen_passwd = ''.join(password)
        self.generatedpassword.set(gen_passwd)

    def accept_fields(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = "SELECT * FROM users WHERE Username = ?"
            cursor.execute(find_user, (self.username.get(),))

            if cursor.fetchall():
                messagebox.showerror("Error", "This username already exists! Please use another username")
            else:
                insert = "INSERT INTO users(Username, GeneratedPassword) VALUES(?, ?)"
                cursor.execute(insert, (self.username.get(), self.generatedpassword.get()))
                db.commit()
                messagebox.showinfo("Success", "Password generated successfully")

    def reset_fields(self):
        self.username_entry.delete(0, END)
        self.length_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.passwordlen.set(12)

if __name__ == '__main__':
    root = Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()
