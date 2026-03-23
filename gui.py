import tkinter as tk
from tkinter import scrolledtext
import sys
import main
import interpretCommand

# ── Variables ────────────────────────────────────────────────────────────────
sendingToServer = False
connected = True
getKeyCommand = ""
lastline = ""
serverhassentatext = False

# ── Status Checker ────────────────────────────────────────────────────────────────
def clearbutton():
    inputtext.set("")
    input_box.delete(0)

def sendtoserver():
    global sendingToServer
    if (sendingToServer == True):
        sendingToServer = False
    else:
        sendingToServer = True
       
        

def findKey():
    global getKeyCommand
    match mode_var.get():
        case "Single Shift":
            getKeyCommand = ("/send -s task " + "shift encode " + f"{len(inputtext.get())}")
        case "Vigenere":
            getKeyCommand = ("/send -s task " + "vigenere encode " + f"{len(inputtext.get())}")
        case "RSA":
            getKeyCommand = ("/send -s task " + "rsa encode " + f"{len(inputtext.get())}")
        case "DiffieHellman":
            getKeyCommand = ("/send -s task " + "diffiehellman encode " + f"{len(inputtext.get())}")
        case "Hashing":
            getKeyCommand = ("/send -s task " + "hashing encode " + f"{len(inputtext.get())}")
        case "None":
            getKeyCommand = (f"/send {inputtext.get()}")

def findKeyButton():
    findKey()
    global getKeyCommand
    global keyValue
    print(getKeyCommand)
    interpretCommand.interpret(getKeyCommand)
    keyValue.set(len(inputtext.get()))

def encodeButton():
    global keyValue
    temp = str(keyValue.get().encode("utf-8")).replace("b'\\r\\x1b","")[:-3]
    match mode_var.get():
        case "Single Shift":
            print(temp)
            output = ("/encode shift " + temp)
            print(output)
            interpretCommand.interpret(output)


def decodeButton():
    print("Decode")

def sendMessage():
    global sendingToServer
    if sendingToServer:
        text = inputtext.get()
        findKey()
        print(getKeyCommand)
        interpretCommand.interpret(getKeyCommand)

def setBuffer():
    global lastline
    interpretCommand.interpret("/set " + lastline[1:])

def showBuffer():
    interpretCommand.interpret("/show")

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
topbarcolor = "green" if connected else "red"
tk.Frame(root, bg=topbarcolor, height=4).pack(fill="x")

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
for m in ("Single Shift", "Vigenere", "RSA", "DiffieHellman", "Hashing", "None"):
    tk.Radiobutton(r2, text=m, variable=mode_var, value=m,
                   indicatoron=False, width=11, bg="#ddd", fg="black",
                   selectcolor="white", relief="raised", command=findKey).pack(side="left", padx=2)

# Key field
keyValue = tk.StringVar()
r3 = tk.Frame(right, bg="#ececec")
r3.pack(fill="x", pady=10)
tk.Label(r3, text="Key :", bg="#ececec", fg="black").pack(side="left")
tk.Entry(r3, relief="solid", bg="white", fg="black", bd=1, textvariable=keyValue).pack(side="left", fill="x", expand=True)

# Encode / Decode / Find key
r4 = tk.Frame(right, bg="#ececec")
r4.pack(fill="x", pady=4)
tk.Button(r4, text="Encode", bg="#ececec", relief="groove", width=20, command=encodeButton).pack(side="left", padx=4)
tk.Button(r4, text="Decode", bg="#ececec", relief="groove", width=20, command=decodeButton).pack(side="left", padx=4)
tk.Button(r4, text="Find key", bg="#ececec", relief="groove", width=20, command=findKeyButton).pack(side="left", padx=4)


# Output box
output_box = scrolledtext.ScrolledText(right, height=4, bg="white", relief="solid", bd=1)
output_box.pack(fill="x", pady=(12, 4))

# Send Encoded
tk.Button(right, text="Send Encoded", bg="#ececec", relief="groove",
          width=14, command=sendMessage).pack(anchor="e")

# Set Buffer
tk.Button(right, text="Set Buffer", bg="#ececec", relief="groove",
          width=14, command=setBuffer).pack(anchor="e")

# Show Buffer
tk.Button(right, text="Show Buffer", bg="#ececec", relief="groove",
          width=14, command=showBuffer).pack(anchor="e")

# ── ChatBox / Console Redirection ────────────────────────────────────────────────────────────────

class TextRedirector:
    def __init__(self, widget, original_stream):
        self.widget = widget
        self.original_stream = original_stream

    def write(self, output):
        #GUI update
        global lastline
        global serverhassentatext
        if serverhassentatext:
            lastline = output.replace("[SERVER]: ", "")
            serverhassentatext = False
        if "[SERVER]: You are asked to encode the text in the following message with the shift-key" in output:
            keyValue.set((output.replace("[SERVER]: You are asked to encode the text in the following message with the shift-key ", "").replace("[K", "").replace("> ", "")))
            serverhassentatext = True


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