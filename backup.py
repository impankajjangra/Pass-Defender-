import tkinter as tk
from tkinter import messagebox, ttk
from cryptography.fernet import Fernet
import os
import random
import string
import pyperclip
from PIL import Image, ImageTk
import sqlite3

class CyberSafeApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Hide the main window initially

        self.key = self.load_key()
        self.cipher_suite = Fernet(self.key)

        # Setup database
        self.setup_database()

        # Splash Screen
        self.splash_root = tk.Toplevel()
        self.splash_root.title("PassDefender - Defend Your Digital World")
        self.splash_root.geometry("800x600")
        self.splash_root.configure(bg="#0a0a0a")

        try:
            image = Image.open("d:/Python/pass.png")
            image = image.resize((800, 600), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(image)
            splash_label = tk.Label(self.splash_root, image=self.tk_image, bg="#0a0a0a")
            splash_label.image = self.tk_image  # Keep a reference to the PhotoImage object
            splash_label.pack()
        except Exception as e:
            print(f"Error loading image: {e}")

        splash_text = tk.Label(self.splash_root, text="PassDefender - Defend Your Digital World", font=("Helvetica", 24, "bold"), fg="#00FF00", bg="#0a0a0a")
        splash_text.pack(pady=20)

        self.splash_root.after(3000, self.show_main_window)

    def load_key(self):
        if not os.path.exists("key.key"):
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)
        else:
            with open("key.key", "rb") as key_file:
                key = key_file.read()
        return key

    def setup_database(self):
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

    def show_main_window(self):
        self.root.deiconify()  # Show the main app window
        self.splash_root.destroy()  # Destroy the splash screen

        self.root.title("PassDefender - Defend Your Digital World")
        self.root.geometry("1024x768")  # Set the window size to 1024x768
        self.root.configure(bg="#FFFFFF")  # Set background to white

        # Load and set the background image
        try:
            bg_image = Image.open("d:/Python/bg_image.png")
            bg_image = bg_image.resize((1280, 800), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(bg_image)  # Save the image as an attribute of the app
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")

        # Create UI elements
        self.create_ui()

    def create_ui(self):
        frame = tk.Frame(self.root, bg="#000000", bd=10, highlightthickness=0, highlightbackground="#FFFFFF")  # Set frame background to black
        frame.place(relx=0.5, rely=0.5, anchor='center')

        title_label = tk.Label(frame, text="Defend Your Digital World", font=("Montserrat", 20, "bold", "italic"), fg="#FFFFFF", bg="#000000")
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        label_font = ("Montserrat", 14, "bold")
        entry_font = ("Times New Roman", 12, "bold")

        label_website = tk.Label(frame, text="Website:", font=label_font, bg="#000000", fg="#FFFFFF")
        label_website.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_website = tk.Entry(frame, width=30, font=entry_font, highlightthickness=0, highlightbackground="#00FF00")
        self.entry_website.grid(row=1, column=1, padx=10, pady=10)

        label_username = tk.Label(frame, text="Username:", font=label_font, bg="#000000", fg="#FFFFFF")
        label_username.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_username = tk.Entry(frame, width=30, font=entry_font, highlightthickness=0, highlightbackground="#00FF00")
        self.entry_username.grid(row=2, column=1, padx=10, pady=10)

        label_password = tk.Label(frame, text="Password:", font=label_font, bg="#000000", fg="#FFFFFF")
        label_password.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entry_password = tk.Entry(frame, width=30, show="*", font=entry_font, highlightthickness=0, highlightbackground="#00FF00")
        self.entry_password.grid(row=3, column=1, padx=10, pady=10)

        style = ttk.Style()
        style.configure("TButton", font=("Montserrat", 12, "bold"), padding=6, borderwidth=0, relief='groove')
        style.map("TButton", background=[('active', '#007bff'), ('!active', '#FFFFFF')], foreground=[('active', 'white'), ('!active', 'black')])

        button_generate = ttk.Button(frame, text="Generate Password", command=self.generate_password, style="TButton")
        button_generate.grid(row=4, column=0, padx=10, pady=10)
        button_save = ttk.Button(frame, text="Save Password", command=self.save_password, style="TButton")
        button_save.grid(row=4, column=1, padx=10, pady=10)
        button_retrieve = ttk.Button(frame, text="Retrieve Passwords", command=self.retrieve_passwords, style="TButton")
        button_retrieve.grid(row=5, column=0, padx=10, pady=10)
        button_search = ttk.Button(frame, text="Search Password", command=self.search_password, style="TButton")
        button_search.grid(row=5, column=1, padx=10, pady=10)
        button_copy = ttk.Button(frame, text="Copy Password", command=self.copy_password, style="TButton")
        button_copy.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.root.bind("<Configure>", self.resize_elements)

    def save_password(self):
        website = self.entry_website.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        if website and username and password:
            encrypted_password = self.cipher_suite.encrypt(password.encode()).decode()
            conn = sqlite3.connect("password_manager.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                           (website, username, encrypted_password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Password saved successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill out all fields.")

    def retrieve_passwords(self):
        conn = sqlite3.connect("password_manager.db")
        cursor = conn.cursor()
        cursor.execute("SELECT website, username, password FROM passwords")
        passwords = cursor.fetchall()
        conn.close()

        if passwords:
            password_list = ""
            for website, username, encrypted_password in passwords:
                decrypted_password = self.cipher_suite.decrypt(encrypted_password.encode()).decode()
                password_list += f"Website: {website}, Username: {username}, Password: {decrypted_password}\n"
            messagebox.showinfo("Stored Passwords", password_list)
        else:
            messagebox.showinfo("No Passwords", "No passwords stored yet!")

    def search_password(self):
        website = self.entry_website.get()
        conn = sqlite3.connect("password_manager.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM passwords WHERE website = ?", (website,))
        result = cursor.fetchone()
        conn.close()

        if result:
            username, encrypted_password = result
            decrypted_password = self.cipher_suite.decrypt(encrypted_password.encode()).decode()
            messagebox.showinfo("Password Found", f"Website: {website}\nUsername: {username}\nPassword: {decrypted_password}")
        else:
            messagebox.showinfo("Not Found", "No password found for this website.")

    def generate_password(self):
        length = 16
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, password)

    def copy_password(self):
        password = self.entry_password.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy.")

    def resize_elements(self, event):
        new_width = event.width
        new_height = event.height
        font_size = max(12, int(min(new_width, new_height) / 35))
        label_font = ("Roboto", font_size, "bold")
        entry_font = ("Poppins", font_size)
        button_font = ("Lato", font_size, "bold")

        # Update font sizes
        for widget in self.root.winfo_children():
            widget_type = widget.winfo_class()
            if widget_type == 'Label':
                widget.config(font=label_font)
            elif widget_type == 'Entry':
                widget.config(font=entry_font)
            elif widget_type == 'TButton':
                widget.config(font=button_font)

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberSafeApp(root)
    root.mainloop()
