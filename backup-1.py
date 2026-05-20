import tkinter as tk
from tkinter import messagebox, ttk
from cryptography.fernet import Fernet
import os
import random
import string
import pyperclip
from PIL import Image, ImageTk
import sqlite3

# Generate a key if it doesn't exist, or load an existing key
def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    return key

key = load_key()
cipher_suite = Fernet(key)

# Database setup
def setup_database():
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database
setup_database()

def save_password():
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()

    if website and username and password:
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()
        conn = sqlite3.connect("password_manager.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                       (website, username, encrypted_password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password saved successfully!")
    else:
        messagebox.showwarning("Warning", "Please fill out all fields.")

def retrieve_passwords():
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT website, username, password FROM passwords")
    passwords = cursor.fetchall()
    conn.close()

    if passwords:
        password_list = ""
        for website, username, encrypted_password in passwords:
            decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
            password_list += f"Website: {website}, Username: {username}, Password: {decrypted_password}\n"
        messagebox.showinfo("Stored Passwords", password_list)
    else:
        messagebox.showinfo("No Passwords", "No passwords stored yet!")



def generate_password():
    length = 8
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    

def copy_password():
    password = entry_password.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No password to copy.")
        
        
def search_password():
    website = entry_website.get()
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE website = ?", (website,username))
    result = cursor.fetchone()
    conn.close()

    if result:
        username, encrypted_password = result
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        messagebox.showinfo("Password Found", f"Website: {website}\nUsername: {username}\nPassword: {decrypted_password}")
    else:
        messagebox.showinfo("Not Found", "No password found for this website.")
        
        
def show_main_window():
    app.deiconify()  # Show the main app window
    splash_root.destroy()  # Destroy the splash screen

# Splash Screen
splash_root = tk.Tk()
splash_root.title("CyberSafe - Password Manager")
splash_root.geometry("800x600")
splash_root.configure(bg="#0a0a0a")

try:
    image = Image.open("d:/Python/splash.png")
    image = image.resize((800, 600), Image.Resampling.LANCZOS)
    tk_image = ImageTk.PhotoImage(image)
    splash_label = tk.Label(splash_root, image=tk_image, bg="#0a0a0a")
    splash_label.image = tk_image  # Keep a reference to the PhotoImage object
    splash_label.pack()
except Exception as e:
    print(f"Error loading image: {e}")

splash_text = tk.Label(splash_root, text="Welcome to CyberSafe", font=("Helvetica", 24, "bold"), fg="#00FF00", bg="#0a0a0a")
splash_text.pack(pady=20)

# Main Application Window
app = tk.Tk()
app.title("CyberSafe - Password Manager")
app.geometry("1024x768")  # Set the window size to 1024x768
app.configure(bg="#FFFFFF")  # Set background to white
app.withdraw()  # Hide the main window initially

# Load and set the background image
try:
    bg_image = Image.open("d:/Python/bg_image.png")
    bg_image = bg_image.resize((1280, 800), Image.Resampling.LANCZOS)
    app.bg_image = ImageTk.PhotoImage(bg_image)  # Save the image as an attribute of the app
    bg_label = tk.Label(app, image=app.bg_image)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    print(f"Error loading background image: {e}")

# Function to resize elements proportionally
def resize_elements(event):
    new_width = event.width
    new_height = event.height
    font_size = max(12, int(min(new_width, new_height) / 35))
    label_font = ("Roboto", font_size, "bold")
    entry_font = ("Poppins", font_size)
    button_font = ("Lato", font_size, "bold")

    # Update font sizes
    title_label.config(font=("Montserrat", font_size + 10, "bold"))
    for widget in [label_website, label_username, label_password]:
        widget.config(font=label_font)
    for widget in [entry_website, entry_username, entry_password]:
        widget.config(font=entry_font)
    for widget in [button_generate, button_save, button_retrieve, button_search, button_copy]:
        widget.config(style="TButton")

# Modern UI Elements
frame = tk.Frame(app, bg="#FFFFFF", bd=10)  # Set frame background to white
frame.place(relx=0.5, rely=0.5, anchor='center')

title_label = tk.Label(frame, text="CyberSafe - Secure Your Credentials", font=("Montserrat", 20, "bold"), fg="#00FF00", bg="#FFFFFF")
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# Labels and Entry widgets with borders and enhanced fonts
label_font = ("Roboto", 14, "bold")
entry_font = ("Poppins", 12)

label_website = tk.Label(frame, text="Website:", font=label_font, bg="#FFFFFF", fg="#000000")
label_website.grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_website = tk.Entry(frame, width=30, font=entry_font, highlightthickness=2, highlightbackground="#00FF00")
entry_website.grid(row=1, column=1, padx=10, pady=10)

label_username = tk.Label(frame, text="Username:", font=label_font, bg="#FFFFFF", fg="#000000")
label_username.grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_username = tk.Entry(frame, width=30, font=entry_font, highlightthickness=2, highlightbackground="#00FF00")
entry_username.grid(row=2, column=1, padx=10, pady=10)

label_password = tk.Label(frame, text="Password:", font=label_font, bg="#FFFFFF", fg="#000000")
label_password.grid(row=3, column=0, padx=10, pady=10, sticky="e")
entry_password = tk.Entry(frame, width=30, show="*", font=entry_font, highlightthickness=2, highlightbackground="#00FF00")
entry_password.grid(row=3, column=1, padx=10, pady=10)

# Buttons with enhanced styles
style = ttk.Style()
style.configure("TButton", font=("Lato", 12, "bold"), padding=6, borderwidth=0, relief="flat")
style.map("TButton", background=[('active', '#1e90ff'), ('!active', '#007bff')], foreground=[('active', 'white'), ('!active', 'white')])

button_generate = ttk.Button(frame, text="Generate Password", command=generate_password, style="TButton")
button_generate.grid(row=4, column=0, padx=10, pady=10)
button_save = ttk.Button(frame, text="Save Password", command=save_password, style="TButton")
button_save.grid(row=4, column=1, padx=10, pady=10)
button_retrieve = ttk.Button(frame, text="Retrieve Passwords", command=retrieve_passwords, style="TButton")
button_retrieve.grid(row=5, column=0, padx=10, pady=10)
button_search = ttk.Button(frame, text="Search Password", command=search_password, style="TButton")
button_search.grid(row=5, column=1, padx=10, pady=10)
button_copy = ttk.Button(frame, text="Copy Password", command=copy_password, style="TButton")
button_copy.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Bind resize event to the function
app.bind("<Configure>", resize_elements)

# Show main window after splash screen duration
splash_root.after(3000, show_main_window)

splash_root.mainloop()
app.mainloop()
