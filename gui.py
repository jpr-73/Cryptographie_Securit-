import threading
import time
import tkinter as tk
from tkinter import scrolledtext

# ── Variables ────────────────────────────────────────────────────────────────
sendingToServer = False
encryptingMode = "Single Shift"


# ── Status Checker ────────────────────────────────────────────────────────────────
def clearbutton():
    print("Clearing !")


def sendtoserver():
    global sendingToServer
    if (sendingToServer == True):
        sendingToServer = False
        print("Not sending to Server")
    else:
        sendingToServer = True
        print("Sending to Server")

def encryptingmode():
    global encryptingMode
    encryptingMode = True

# ── GUI ────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Secret Communication Channel")
root.geometry("1000x600")
root.configure(bg="#ececec")
root.option_add("*Button.highlightBackground", "#ececec")
root.option_add("*Label.highlightBackground", "#ececec")
root.option_add("*RadioButton.highlightBackground", "#ececec")
root.option_add("*Entry.highlightBackground", "#ececec")
root.option_add("*Entry.insertBackground", "Black")

# ── Top bar ────────────────────────────────────────────────────────────────
connected = True
topbarcolor = "green" if connected else "red"
tk.Frame(root, bg=topbarcolor, height=4).pack(fill="x")

# ── Layout ─────────────────────────────────────────────────────────────────
left = tk.Frame(root, bg="#ececec", width=300)
left.pack(side="left", fill="y", padx=8, pady=8)
left.pack_propagate(False)

tk.Frame(root, bg="#cccccc", width=1).pack(side="left", fill="y")

right = tk.Frame(root, bg="#ececec")
right.pack(side="left", fill="both", expand=True, padx=10, pady=8)

# ── Left: chat history ──────────────────────────────────────────────────────
chat = scrolledtext.ScrolledText(left, bg="white", relief="flat", state="disabled")
chat.pack(fill="both", expand=True)

# ── Right: controls ─────────────────────────────────────────────────────────

# Checkbox + Text/Image tabs
r1 = tk.Frame(right, bg="#ececec")
r1.pack(fill="x", pady=(0, 6))
tk.Checkbutton(r1, text="Send to Server only", bg="#ececec", fg="black", command=sendtoserver).pack(side="left")
tab_var = tk.StringVar(value="Text")
for t in ("Image", "Text"):
    tk.Radiobutton(r1, text=t, variable=tab_var, value=t,
                   indicatoron=False, width=7, bg="#ddd",
                   selectcolor="white", relief="raised", fg="black").pack(side="right", padx=1)

# Input box
inputtext = tk.StringVar()
input_box = tk.Entry(right, bg="white", fg="black", relief="solid", borderwidth=0, bd=1, textvariable=inputtext)
input_box.pack(fill="x", pady=(0, 6))


# Send Clear

tk.Button(right, text="Send Clear", command=clearbutton, bg="#ececec", fg="black", relief="groove",
          width=10).pack(anchor="e", pady=(2, 6))

# Cipher tabs
r2 = tk.Frame(right, bg="#ececec")
r2.pack(pady=4)
mode_var = tk.StringVar(value="Single Shift")
for m in ("Single Shift", "Vigenere", "RSA", "DiffieHellman", "Hashing"):
    tk.Radiobutton(r2, text=m, variable=mode_var, value=m,
                   indicatoron=False, width=11, bg="#ddd", fg="black",
                   selectcolor="white", relief="raised").pack(side="left", padx=2)

# Key field
r3 = tk.Frame(right, bg="#ececec")
r3.pack(fill="x", pady=10)
tk.Label(r3, text="Key :", bg="#ececec", fg="black").pack(side="left")
tk.Entry(r3, relief="solid", bg="white", fg="black", bd=1).pack(side="left", fill="x", expand=True)

# Encode / Decode / Find key
r4 = tk.Frame(right, bg="#ececec")
r4.pack(fill="x", pady=4)
for label in ("Encode", "Decode", "Find key"):
    tk.Button(r4, text=label, bg="#ececec", relief="groove",
              width=20).pack(side="left", padx=4)

# Output box
output_box = scrolledtext.ScrolledText(right, height=4, bg="white", relief="solid", bd=1)
output_box.pack(fill="x", pady=(12, 4))

# Send Encoded
tk.Button(right, text="Send Encoded", bg="#ececec", relief="groove",
          width=14).pack(anchor="e")


# ── ChatBox ────────────────────────────────────────────────────────────────
def chatBox(message="Test"):
    chat.config(state="normal")
    chat.insert(tk.END, message + "\n")
    chat.config(state="disabled")
    chat.see(tk.END)


t = threading.Thread(target=chatBox, daemon=True)
t.start()

root.mainloop()