import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import hashlib

# Database Setup
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, status TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY, name TEXT, contact TEXT)''')
conn.commit()


# Secure Password Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Login System
def login():
    username = entry_username.get()
    password = entry_password.get()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = cursor.fetchone()

    if user:
        login_window.destroy()
        open_library_management()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")


# Register New User
def register():
    username = entry_username.get()
    password = entry_password.get()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
    conn.commit()
    messagebox.showinfo("Success", "User registered successfully!")


# GUI for Library Management
def open_library_management():
    library_window = tk.Tk()
    library_window.title("Library Management System")

    # Book Management Section
    def add_book():
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()
        cursor.execute("INSERT INTO books (title, author, year, status) VALUES (?, ?, ?, ?)",
                       (title, author, year, "Available"))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully!")
        load_books()

    def delete_book():
        book_id = entry_book_id.get()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book deleted successfully!")
        load_books()

    def issue_book():
        book_id = entry_book_id.get()
        cursor.execute("UPDATE books SET status = 'Issued' WHERE id = ?", (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book issued successfully!")
        load_books()

    def return_book():
        book_id = entry_book_id.get()
        cursor.execute("UPDATE books SET status = 'Available' WHERE id = ?", (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book returned successfully!")
        load_books()

    def load_books():
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        book_list.delete(*book_list.get_children())
        for book in books:
            book_list.insert("", "end", values=book)

    # UI Elements
    tk.Label(library_window, text="Title").grid(row=0, column=0)
    entry_title = tk.Entry(library_window)
    entry_title.grid(row=0, column=1)

    tk.Label(library_window, text="Author").grid(row=1, column=0)
    entry_author = tk.Entry(library_window)
    entry_author.grid(row=1, column=1)

    tk.Label(library_window, text="Year").grid(row=2, column=0)
    entry_year = tk.Entry(library_window)
    entry_year.grid(row=2, column=1)

    tk.Button(library_window, text="Add Book", command=add_book).grid(row=3, column=1)

    # Book List Table
    book_list = ttk.Treeview(library_window, columns=("ID", "Title", "Author", "Year", "Status"), show="headings")
    book_list.heading("ID", text="ID")
    book_list.heading("Title", text="Title")
    book_list.heading("Author", text="Author")
    book_list.heading("Year", text="Year")
    book_list.heading("Status", text="Status")
    book_list.grid(row=5, column=0, columnspan=3)
    load_books()

    tk.Label(library_window, text="Book ID").grid(row=6, column=0)
    entry_book_id = tk.Entry(library_window)
    entry_book_id.grid(row=6, column=1)

    tk.Button(library_window, text="Delete", command=delete_book).grid(row=7, column=0)
    tk.Button(library_window, text="Issue", command=issue_book).grid(row=7, column=1)
    tk.Button(library_window, text="Return", command=return_book).grid(row=7, column=2)

    library_window.mainloop()


# Login Window
login_window = tk.Tk()
login_window.title("Login - Secure Library System")

tk.Label(login_window, text="Username").grid(row=0, column=0)
entry_username = tk.Entry(login_window)
entry_username.grid(row=0, column=1)

tk.Label(login_window, text="Password").grid(row=1, column=0)
entry_password = tk.Entry(login_window, show="*")
entry_password.grid(row=1, column=1)

tk.Button(login_window, text="Login", command=login).grid(row=2, column=0)
tk.Button(login_window, text="Register", command=register).grid(row=2, column=1)

login_window.mainloop()
