import tkinter as tk
from tkinter import scrolledtext
import sys
import interpretCommand
import time

# ── Variables ────────────────────────────────────────────────────────────────
sendingToServer = False
connected = False
getKeyCommand = ""
lastline = ""
serverhassentatext = False

# ── Status Checker ────────────────────────────────────────────────────────────────
def clearbutton():
    global getKeyCommand
    global sendingToServer
    if (sendingToServer==False) :
        getKeyCommand = (f"/send {inputtext.get()}")
        interpretCommand.interpret(getKeyCommand)
        inputtext.set("")
        input_box.delete(0)
    else :
        getKeyCommand = (f"/send -s {inputtext.get()}")
        interpretCommand.interpret(getKeyCommand)
        inputtext.set("")
        input_box.delete(0)

def sendtoserver():
    global sendingToServer
    if (sendingToServer == True):
        sendingToServer = False
    else:
        sendingToServer = True
       
def encodeTaskButton():
    global mode_var
    match mode_var.get():
        case "Single Shift":
            interpretCommand.interpret("/send -s task " + "shift encode " + f"{int(inputtext.get())}")
        case "Vigenere":
            interpretCommand.interpret("/send -s task " + "vigenere encode " + f"{int(inputtext.get())}")
        case "RSA":
            interpretCommand.interpret("/send -s task " + "RSA encode " + f"{int(inputtext.get())}")
        case "DiffieHellman":
            interpretCommand.interpret("/send -s task " + "diffiehellman encode " + f"{int(inputtext.get())}")
        case "Hashing":
            interpretCommand.interpret("/send -s task " + "hashing encode " + f"{int(inputtext.get())}")

def decodeTaskButton():
    global mode_var
    match mode_var.get():
        case "Single Shift":
            interpretCommand.interpret("/send -s task " + "shift decode " + f"{int(inputtext.get())}")
        case "Vigenere":
            interpretCommand.interpret("/send -s task " + "vigenere decode " + f"{int(inputtext.get())}")
        case "RSA":
            interpretCommand.interpret("/task " + "RSA decode " + f"{modValue.get()}" + " " + f"{keyValue.get()}")
        case "DiffieHellman":
            interpretCommand.interpret("/send -s task " + "diffiehellman decode " + f"{int(inputtext.get())}")
        case "Hashing":
            interpretCommand.interpret("/send -s task " + "hashing decode " + f"{int(inputtext.get())}")

def generateButton() :
    interpretCommand.interpret("/generate")

def encodeButton() :
    global mode_var
    temp = keyValue.get()
    match mode_var.get():
        case "Single Shift":
            output = ("/encode shift " + temp)
            interpretCommand.interpret(output)
        case "Vigenere":
            output = ("/encode vigenere " + temp)
            interpretCommand.interpret(output)
        case "RSA":
            output = ("/encode RSA " + f"{modValue.get()}" + " " + f"{keyValue.get()}")
            interpretCommand.interpret(output)
        case "DiffieHellman":
            output = ("/encode diffiehellman " + temp)
            interpretCommand.interpret(output)
        case "Hashing":
            output = ("/encode hashing " + temp)
            interpretCommand.interpret(output)
    keyValue.set("")
    modValue.set("")


def decodeButton():
    global mode_var
    global getKeyCommand
    global keyValue
    match mode_var.get():
        case "Single Shift":
            getKeyCommand = ("/decode " + "shift " + f"{keyValue.get()}")
            interpretCommand.interpret(getKeyCommand)
        case "Vigenere":
            getKeyCommand = ("/decode " + "vigenere " + f"{keyValue.get()}")
            interpretCommand.interpret(getKeyCommand)
        case "RSA":
            getKeyCommand = ("/decode " + "rsa " + f"{keyValue.get()}" + f"{modValue.get()}" + f"{contentValue.get()}")
            interpretCommand.interpret(getKeyCommand)
        case "DiffieHellman":
            getKeyCommand = ("/decode " + "diffiehellman " + f"{keyValue.get()}")
            interpretCommand.interpret(getKeyCommand)
        case "Hashing":
            getKeyCommand = ("/decode " + "hashing " + f"{keyValue.get()}")
            interpretCommand.interpret(getKeyCommand)
        case "None":
            print(keyValue.get())

# ── GUI ────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Secret Communication Channel")
root.geometry("1000x600")
root.attributes('-topmost', True)
root.configure(bg="#ececec")
root.option_add("*Button.highlightBackground", "#ececec")
root.option_add("*Label.highlightBackground", "#ececec")
root.option_add("*RadioButton.highlightBackground", "#ececec")
root.option_add("*Entry.highlightBackground", "#ececec")
root.option_add("*Entry.insertBackground", "Black")

# ── Top bar ────────────────────────────────────────────────────────────────
topbarcolor = tk.StringVar(value="red")
statusbar = tk.Frame(root, bg=topbarcolor.get(), height=4)
statusbar.pack(fill="x")

# ── Layout ─────────────────────────────────────────────────────────────────
left = tk.Frame(root, bg="#ececec", width=350)
left.pack(side="left", fill="y", padx=8, pady=8)
left.pack_propagate(False)

tk.Frame(root, bg="#cccccc", width=1).pack(side="left", fill="y")

right = tk.Frame(root, bg="#ececec")
right.pack(side="left", fill="both", expand=True, padx=10, pady=8)

# ── Left: chat history ──────────────────────────────────────────────────────
chat = scrolledtext.ScrolledText(left, bg="white", relief="flat", state="disabled", fg="black")
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
keyValue = tk.StringVar()
r3 = tk.Frame(right, bg="#ececec")
r3.pack(fill="x", pady=10)
tk.Label(r3, text="Key :", bg="#ececec", fg="black").pack(side="left")
tk.Entry(r3, relief="solid", bg="white", fg="black", bd=1, textvariable=keyValue).pack(side="left", fill="x", expand=True)

# Modular field
modValue = tk.StringVar()
r6 = tk.Frame(right, bg="#ececec")
r6.pack(fill="x", pady=10)
tk.Label(r6, text="Modular :", bg="#ececec", fg="black").pack(side="left")
tk.Entry(r6, relief="solid", bg="white", fg="black", bd=1, textvariable=modValue).pack(side="left", fill="x", expand=True)

# Content field
contentValue = tk.StringVar()
r7 = tk.Frame(right, bg="#ececec")
r7.pack(fill="x", pady=10)
tk.Label(r7, text="Content :", bg="#ececec", fg="black").pack(side="left")
tk.Entry(r7, relief="solid", bg="white", fg="black", bd=1, textvariable=contentValue).pack(side="left", fill="x", expand=True)

# Encode / Decode
r4 = tk.Frame(right, bg="#ececec")
r4.pack(fill="x", pady=4)
tk.Button(r4, text="Encode", bg="#ececec", relief="groove", width=15, command=encodeButton).pack(side="left", padx=4)
tk.Button(r4, text="Decode", bg="#ececec", relief="groove", width=15, command=decodeButton).pack(side="left", padx=4)


# Task Encode / Task Decode / Generate
r5 = tk.Frame(right, bg="#ececec")
r5.pack(fill="x", pady=4)
tk.Button(r5, text="Get Encode Task", bg="#ececec", relief="groove", width=15, command=encodeTaskButton).pack(side="left", padx=5)
tk.Button(r5, text="Get Decode Task", bg="#ececec", relief="groove", width=15, command=decodeTaskButton).pack(side="left", padx=5)
tk.Button(r5, text="Generate", bg="#ececec", relief="groove", width=15, command=generateButton).pack(side="left", padx=5)

# ── ChatBox / Console Redirection ────────────────────────────────────────────────────────────────

class TextRedirector:
    def __init__(self, widget, original_stream):
        self.widget = widget
        self.original_stream = original_stream

    def write(self, output):
        #GUI update
        global lastline
        global connected
        global serverhassentatext
        global topbarcolor
        global statusbar

        if "Connected successfully" in output:
            connected = True
            if connected:
                topbarcolor.set(value="green")
                statusbar.config(bg=topbarcolor.get())
                root.attributes('-topmost', False)


        def append_text():
            self.widget.config(state="normal")
            self.widget.insert(tk.END, output.replace("[K", "").replace(">", ""))
            self.widget.config(state="disabled")
            self.widget.see(tk.END)
        self.widget.after(0, append_text)
        
        # Also write to the original console so input() still works visually in terminal
        self.original_stream.write(output)
        self.original_stream.flush()

    def flush(self):
        self.original_stream.flush()

sys.stdout = TextRedirector(chat, sys.stdout)
sys.stderr = TextRedirector(chat, sys.stderr)

if __name__ == "__main__":
    root.mainloop()