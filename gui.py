import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from database import create_db, add_password, get_passwords, delete_password, search_password

create_db()

def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if website and username and password:
        add_password(website, username, password)
        messagebox.showinfo("Success", "Password saved successfully!")
        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "All fields are required!")

def view_passwords():
    records = get_passwords()
    listbox.delete(0, tk.END)
    for record in records:
        website = record[0]
        username = record[1]
        password = record[2]
        listbox.insert(tk.END, f"Website: {website}, Username: {username}, Password: {password}")

def delete_selected_password():
    selected_index = listbox.curselection()
    if selected_index:
        selected_password = listbox.get(selected_index)
        website = selected_password.split(',')[0][10:].strip()
        username = selected_password.split(',')[1][11:].strip()
        password = selected_password.split(',')[2][11:].strip()
        
        if website and username and password:
            messagebox.showinfo("Success", "Password deleted successfully!")
            listbox.delete(selected_index)
            try:
                conn = sqlite3.connect("passwords.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM passwords WHERE website = ? AND username = ? AND password = ?", (website, username, password))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Error while clearing the database: {e}")
        else:
            messagebox.showwarning("Warning", "Invalid data. Could not delete password.")
    else:
        messagebox.showwarning("Warning", "Please select a password to delete.")

def search_passwords(event=None):
    website = search_entry.get()
    if website:
        records = search_password(website)  
        listbox.delete(0, tk.END)  
        if records:  
            for record in records:
                website = record[0]
                username = record[1]
                password = record[2]
                listbox.insert(tk.END, f"Website: {website}, Username: {username}, Password: {password}")
        else:
            messagebox.showinfo("No Results", "No passwords found for the given website.")
    else:
        messagebox.showwarning("Warning", "Please enter a website to search.")


def on_closing():

    if messagebox.askokcancel("Quit", "Do you want to clear all passwords and exit?"):
        try:
            conn = sqlite3.connect("passwords.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords")  
            conn.commit()
            conn.close()
            print("All records cleared from passwords.db.")
        except Exception as e:
            print(f"Error while clearing the database: {e}")

        root.destroy()  

root = tk.Tk()
root.title("Bharath's Password Manager")
root.geometry("800x600")

style = ttk.Style()
style.theme_use('aqua')

root.protocol("WM_DELETE_WINDOW", on_closing)

search_label = tk.Label(root, text="Search by Website", font=("Helvetica", 14))
search_label.grid(row=8, column=0, pady=10, padx=10, sticky="e")

search_entry = tk.Entry(root, font=("Helvetica", 14), width=40)
search_entry.grid(row=8, column=1, pady=10, padx=10, columnspan=2)


search_entry.bind("<Return>", search_passwords)


title_label = tk.Label(root, text="Bharath's Password Manager", font=("Helvetica", 18, "bold"), bg="#4CAF50", fg="white", pady=10)
title_label.grid(row=0, column=0, columnspan=3, sticky="nsew")


tk.Label(root, text="Website", font=("Helvetica", 14)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
website_entry = tk.Entry(root, font=("Helvetica", 14), width=40)
website_entry.grid(row=1, column=1, pady=10, padx=10, columnspan=2)

tk.Label(root, text="Username", font=("Helvetica", 14)).grid(row=2, column=0, pady=10, padx=10, sticky="e")
username_entry = tk.Entry(root, font=("Helvetica", 14), width=40)
username_entry.grid(row=2, column=1, pady=10, padx=10, columnspan=2)

tk.Label(root, text="Password", font=("Helvetica", 14)).grid(row=3, column=0, pady=10, padx=10, sticky="e")
password_entry = tk.Entry(root, font=("Helvetica", 14), show='*', width=40)
password_entry.grid(row=3, column=1, pady=10, padx=10, columnspan=2)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14), width=20)
style.map("TButton", background=[('active', '#388E3C')], foreground=[('active', 'white')])


save_button = ttk.Button(root, text="Save Password", command=save_password, style="TButton")
save_button.grid(row=4, column=0, columnspan=3, pady=10)

view_button = ttk.Button(root, text="View Passwords", command=view_passwords, style="TButton")
view_button.grid(row=5, column=0, columnspan=3, pady=10)

delete_button = ttk.Button(root, text="Delete Password", command=delete_selected_password, style="TButton")
delete_button.grid(row=7, column=0, columnspan=3, pady=10)


listbox_frame = tk.Frame(root)
listbox_frame.grid(row=6, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

listbox_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(listbox_frame, font=("Helvetica", 12), width=70, height=15, bd=2, relief="sunken", yscrollcommand=listbox_scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
listbox_scrollbar.config(command=listbox.yview)

root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()