import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# === DATABASE SETUP ===
conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")

# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    student_class TEXT NOT NULL
)
""")

# Insert default admin if not exists
cursor.execute("SELECT * FROM users WHERE username = 'admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin"))
    conn.commit()

# === MAIN APPLICATION ===
class SchoolSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - School Management System")
        self.root.geometry("300x200")
        self.login_screen()

    def login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        if cursor.fetchone():
            self.main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def main_screen(self):
        self.clear_screen()
        self.root.geometry("700x400")
        self.root.title("School Management System")

        # Variables
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.class_var = tk.StringVar()

        # Input Form
        tk.Button(self.root, text="Logout", command=self.logout).grid(row=0, column=2, padx=10, pady=10, sticky='e')

        tk.Label(self.root, text="Name").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(self.root, textvariable=self.name_var).grid(row=0, column=1, pady=5)

        tk.Label(self.root, text="Age").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(self.root, textvariable=self.age_var).grid(row=1, column=1, pady=5)

        tk.Label(self.root, text="Class").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(self.root, textvariable=self.class_var).grid(row=2, column=1, pady=5)

        tk.Button(self.root, text="Add Student", command=self.add_student).grid(row=3, column=0, pady=10)
        tk.Button(self.root, text="Delete Selected", command=self.delete_student).grid(row=3, column=1, pady=10)

        # Student List
        columns = ('ID', 'Name', 'Age', 'Class')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

        self.display_students()

    def add_student(self):
        name = self.name_var.get()
        age = self.age_var.get()
        student_class = self.class_var.get()

        if not name or not age or not student_class:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Input Error", "Age must be a number")
            return

        cursor.execute("INSERT INTO students (name, age, student_class) VALUES (?, ?, ?)",
                       (name, age, student_class))
        conn.commit()
        self.clear_fields()
        self.display_students()
        messagebox.showinfo("Success", "Student added")

    def display_students(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor.execute("SELECT * FROM students")
        for row in cursor.fetchall():
            self.tree.insert('', tk.END, values=row)

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No student selected")
            return

        student_id = self.tree.item(selected_item[0])['values'][0]
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        self.tree.delete(selected_item)
        messagebox.showinfo("Deleted", "Student record deleted")

    def clear_fields(self):
        self.name_var.set('')
        self.age_var.set('')
        self.class_var.set('')

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def logout(self):
        self.clear_screen()
        self.root.geometry("300x200")
        self.root.title("Login - School Management System")
        self.login_screen()


# === Run App ===
if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolSystem(root)
    root.mainloop()
