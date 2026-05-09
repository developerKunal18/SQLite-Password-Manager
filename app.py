import tkinter as tk
import sqlite3
import base64

# ---------- Database ----------
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account TEXT,
    password TEXT
)
""")

conn.commit()

# ---------- Utilities ----------
def encode(text):
    return base64.b64encode(text.encode()).decode()

def decode(text):
    return base64.b64decode(text.encode()).decode()

# ---------- Operations ----------
def refresh():
    listbox.delete(0, tk.END)

    cursor.execute("SELECT * FROM passwords")

    for row in cursor.fetchall():
        account = row[1]
        password = decode(row[2])

        listbox.insert(
            tk.END,
            f"{row[0]}. {account} → {password}"
        )

def save_password():
    account = account_entry.get()
    password = password_entry.get()

    if account and password:
        encoded = encode(password)

        cursor.execute(
            "INSERT INTO passwords (account, password) VALUES (?, ?)",
            (account, encoded)
        )

        conn.commit()

        account_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        refresh()

def delete_password():
    selected = listbox.curselection()

    if selected:
        item = listbox.get(selected[0])

        password_id = item.split(".")[0]

        cursor.execute(
            "DELETE FROM passwords WHERE id=?",
            (password_id,)
        )

        conn.commit()

        refresh()

# ---------- GUI ----------
root = tk.Tk()
root.title("SQLite Password Manager")

tk.Label(root, text="Account").pack()

account_entry = tk.Entry(root, width=40)
account_entry.pack()

tk.Label(root, text="Password").pack()

password_entry = tk.Entry(root, width=40, show="*")
password_entry.pack()

tk.Button(
    root,
    text="Save Password",
    command=save_password
).pack(pady=5)

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

tk.Button(
    root,
    text="Delete Selected",
    command=delete_password
).pack()

refresh()

root.mainloop()

conn.close()
