import tkinter as tk
from tkinter import scrolledtext
import sys
import interpretCommand

# ── Variables ────────────────────────────────────────────────────────────────
sendingToServer = False
connected = False
getKeyCommand = ""
lastline = ""
serverhassentatext = False

# ── Status Checker ────────────────────────────────────────────────────────────────
def update_visibility(*args):
    try:
        keyField.pack_forget()
        encodeFrame.pack_forget()
        encodeTask.pack_forget()
        modField.pack_forget()
        contentField.pack_forget()
        encETdec.pack_forget()
        decodeFrame.pack_forget()
        genBtn.pack_forget()
        decodeTask.pack_forget()
        eField.pack_forget()
        dField.pack_forget()
        getDifHelTask.pack_forget()
        difHelGenSpace.pack_forget()
        pField.pack_forget()
        gField.pack_forget()
        keyField.pack_forget()
        difHelHalfKey.pack_forget()
        privKeyField.pack_forget()
        publKeyField.pack_forget()
        difSendSecret.pack_forget()
        taskhash.pack_forget()
        taskhashverify.pack_forget()


        selected_mode = mode_var.get()

        if selected_mode == "Single Shift":
            keyField.pack(fill="x", pady=10, after=modeTab)
            encodeTask.pack(fill="x", pady=10, after=keyField)
            encodeFrame.pack(fill="x", pady=10, after=encodeTask)
            decodeTask.pack(fill="x", pady=10, after=encodeFrame)
            decodeFrame.pack(fill="x", pady=10, after=decodeTask)
            last_widget = decodeFrame

        
        elif selected_mode == "DiffieHellman":
            getDifHelTask.pack(fill="x", pady=10, after=modeTab)
            difHelGenSpace.pack(fill="x", pady=10, after=getDifHelTask)
            pField.pack(fill="x", pady=10, after=difHelGenSpace)
            gField.pack(fill="x", pady=10, after=pField)
            difHelHalfKey.pack(fill="x", pady=10, after=gField)
            privKeyField.pack(fill="x", pady=10, after=difHelHalfKey)
            publKeyField.pack(fill="x", pady=10, after=privKeyField)
            difSendSecret.pack(fill="x", pady=10, after=publKeyField)
            last_widget = difSendSecret

        elif selected_mode == "Hashing":
            taskhash.pack(fill="x", pady=10, after=modeTab)
            taskhashverify.pack(fill="x", pady=10, after=taskhash)
            last_widget = taskhashverify

        elif selected_mode == "RSA":
            encETdec.pack(fill="x", pady=5, after=modeTab)
            last_widget = encETdec

            selected_mode2 = sub_mode1.get()

            if selected_mode2 == "Encode":
                encodeTask.pack(fill="x", pady=10, after=last_widget)
                modField.pack(fill="x", pady=10, after=encodeTask)
                eField.pack(fill="x", pady=10, after=modField)
                encodeFrame.pack(fill="x", pady=10, after=eField)

            if selected_mode2 == "Decode":
                decodeTask.pack(fill="x", pady=5, after=last_widget)
                genBtn.pack(fill="x", pady=10, after=decodeTask)
                modField.pack(fill="x", pady=10, after=genBtn)
                dField.pack(fill="x", pady=10, after=modField)

                contentField.pack(fill="x", pady=10, after=dField)
                decodeFrame.pack(fill="x", pady=10, after=contentField)


        elif selected_mode == "Vigenere":
            keyField.pack(fill="x", pady=10, after=modeTab)
            encodeTask.pack(fill="x", pady=10, after=keyField)
            encodeFrame.pack(fill="x", pady=10, after=encodeTask)
            decodeTask.pack(fill="x", pady=10, after=encodeFrame)
            decodeFrame.pack(fill="x", pady=10, after=decodeTask)
            last_widget = decodeFrame

    except Exception as e:
        return

def clearbutton():
    global getKeyCommand
    global sendingToServer
    try:
        if not sendingToServer:
            getKeyCommand = f"/send {inputtext.get()}"
            interpretCommand.interpret(getKeyCommand)
            inputtext.set("")
            input_box.delete(0, tk.END)
        else:
            getKeyCommand = f"/send -s {inputtext.get()}"
            interpretCommand.interpret(getKeyCommand)
            inputtext.set("")
            input_box.delete(0, tk.END)
    except Exception as e:
        print(f"Error: {e}")

def sendtoserver():
    global sendingToServer
    try:
        if sendingToServer:
            sendingToServer = False
        else:
            sendingToServer = True
    except Exception as e:
        print(f"Error: {e}")

def encodeTaskButton():
    global mode_var
    try:
        match mode_var.get():
            case "Single Shift":
                are_You_Stupid('i')
                interpretCommand.interpret("/task shift encode " + inputtext.get())
            case "Vigenere":
                are_You_Stupid('i')
                interpretCommand.interpret("/task vigenere encode " + inputtext.get())
            case "RSA":
                are_You_Stupid('i')
                interpretCommand.interpret("/task RSA encode " + inputtext.get())
            case "DiffieHellman":
                interpretCommand.interpret("/task DifHel")
            case "Hashing":
                interpretCommand.interpret("/task hash hash")
        empty_values()
    except Exception as e:
        print(f"Error: {e}")

def decodeTaskButton():
    global mode_var
    are_You_Stupid('i')
    try:
        match mode_var.get():
            case "Single Shift":
                interpretCommand.interpret("/task shift decode " + inputtext.get())
            case "Vigenere":
                interpretCommand.interpret("/task vigenere decode " + inputtext.get())
            case "RSA":
                interpretCommand.interpret("/task RSA decode " + inputtext.get())
            case "DiffieHellman":
                interpretCommand.interpret("/task diffiehellman decode " + inputtext.get())
            case "Hashing":
                interpretCommand.interpret("/task hashing decode " + inputtext.get())
        empty_values()
    except Exception as e:
        print(f"Error: {e}")


def getDifHelTaskButton():
    try :
        interpretCommand.interpret("/task DifHel")
        empty_values()
    except Exception as e:
        print(f"Error: {e}")

def difHelGenSpaceButton():
    try :
        interpretCommand.interpret("/generate dh")
        empty_values()
    except Exception as e:
        print(f"Error: {e}")

def difHelHalfKeyButton():
    try :
        interpretCommand.interpret(f"/generate dh-hk {pValue.get()} {gValue.get()}")
        empty_values()
    except Exception as e:
        print(f"Error: {e}")

def difHelSecretButton():
    try :
        #print(f"/generate dh-secret {pValue.get()} {privKeyValue.get()} {publKeyValue.get()}")
        interpretCommand.interpret(f"/generate dh-secret {pValue.get()} {privKeyValue.get()} {publKeyValue.get()}")
        empty_values()
    except Exception as e:
        print(f"Error: {e}")

def taskhashButton():
    try :
        interpretCommand.interpret(f"/task hash hash")
        empty_values()
    except Exception as e:
        print(f"Error: {e}")

def taskhashverifyButton():
    try :
        interpretCommand.interpret(f"/task hash verify")
        empty_values()
    except Exception as e:
        print(f"Error: {e}")


def generateButton():
    global mode_var
    try:
        match mode_var.get():
            case "RSA":
                interpretCommand.interpret("/generate rsa")
            case "DiffieHellman":
                interpretCommand.interpret("/generate dh")
        empty_values()
    except Exception as e:
        print(f"Error: {e}")

def encodeButton():
    global mode_var
    are_You_Stupid('k')
    temp = keyValue.get()
    try:
        match mode_var.get():
            case "Single Shift":
                output = f"/encode shift {temp}"
                interpretCommand.interpret(output)
            case "Vigenere":
                output = f"/encode vigenere {temp}"
                interpretCommand.interpret(output)
            case "RSA":
                output = f"/encode RSA {modValue.get()} {eValue.get()}"
                interpretCommand.interpret(output)
            case "DiffieHellman":
                output = f"/encode diffiehellman {temp}"
                interpretCommand.interpret(output)
            case "Hashing":
                output = f"/encode hashing {temp}"
                interpretCommand.interpret(output)
        empty_values()
    except Exception as e:
        print(f"Error: {e}")

def decodeButton():
    global mode_var
    try:
        match mode_var.get():
            case "Single Shift":
                getKeyCommand = f"/decode shift"
                interpretCommand.interpret(getKeyCommand)
            case "Vigenere":
                getKeyCommand = f"/decode vigenere {keyValue.get()}"
                interpretCommand.interpret(getKeyCommand)
            case "RSA":
                are_You_Stupid('k')
                getKeyCommand = f"/decode rsa {modValue.get()} {dValue.get()} {contentValue.get()}"
                interpretCommand.interpret(getKeyCommand)
            case "DiffieHellman":
                getKeyCommand = f"/decode diffiehellman {keyValue.get()}"
                interpretCommand.interpret(getKeyCommand)
            case "Hashing":
                getKeyCommand = f"/decode hashing {keyValue.get()}"
                interpretCommand.interpret(getKeyCommand)
        empty_values()
    except Exception as e:
        print(f"Error: {e}")

def empty_values() :
    keyValue.set("")
    modValue.set("")
    eValue.set("")
    dValue.set("")
    contentValue.set("")

def are_You_Stupid(mode):
    if (inputtext.get() == "" and mode == 'i'):
        print("\nYou might want to decide a length, maybe ?\n")
    if (keyValue.get() == "" and mode == 'k'):
        print("\nYou might want to give me a key, maybe ?\n")

# ── GUI ────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Secret Communication Channel")
icon_img = tk.PhotoImage(file="icon.png")
root.iconphoto(True, icon_img)
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

# Mode tabs
modeTab = tk.Frame(right, bg="#ececec")
modeTab.pack(pady=4)
mode_var = tk.StringVar(value="Single Shift")
for m in ("Single Shift", "Vigenere", "RSA", "DiffieHellman", "Hashing"):
    tk.Radiobutton(modeTab, text=m, variable=mode_var, value=m,
                   indicatoron=False, width=11, bg="#ddd", fg="black",
                   selectcolor="white", relief="raised", command=update_visibility).pack(side="left", padx=2)

encETdec = tk.Frame(right, bg="#ececec")
encETdec.pack(pady=4)
sub_mode1 = tk.StringVar(value="Encode")
for m2 in ("Encode", "Decode"):
    tk.Radiobutton(encETdec, text=m2, variable=sub_mode1, value=m2,
                   indicatoron=False, width=11, bg="#ddd", fg="black",
                   selectcolor="white", relief="raised", command=update_visibility).pack(side="left", padx=2)

# Key field
keyValue = tk.StringVar()
keyField = tk.Frame(right, bg="#ececec")
keyField.pack(fill="x", pady=10)
tk.Label(keyField, text="Key :", bg="#ececec", fg="black").pack(side="left")
tk.Entry(keyField, relief="solid", bg="white", fg="black", bd=1, textvariable=keyValue).pack(side="left", fill="x", expand=True)

# Modular field
modValue = tk.StringVar()
modField = tk.Frame(right, bg="#ececec")
modField.pack(fill="x", pady=10)
tk.Label(modField, text="Modular :", bg="#ececec", fg="black").pack(side="left")
tk.Entry(modField, relief="solid", bg="white", fg="black", bd=1, textvariable=modValue).pack(side="left", fill="x", expand=True)

# public key field d
dValue = tk.StringVar()
dField = tk.Frame(right, bg="#ececec")
dField.pack(fill="x", pady=10)
tk.Label(dField, text="d :", bg="#ececec", fg="black").pack(side="left")
tk.Entry(dField, relief="solid", bg="white", fg="black", bd=1, textvariable=dValue).pack(side="left", fill="x", expand=True)


# e field
eValue = tk.StringVar()
eField = tk.Frame(right, bg="#ececec")
eField.pack(fill="x", pady=10)
tk.Label(eField, text="e :", bg="#ececec", fg="black").pack(side="left")
tk.Entry(eField, relief="solid", bg="white", fg="black", bd=1, textvariable=eValue).pack(side="left", fill="x", expand=True)

# Content field
contentValue = tk.StringVar()
contentField = tk.Frame(right, bg="#ececec")
contentField.pack(fill="x", pady=10)
tk.Label(contentField, text="Content :", bg="#ececec", fg="black").pack(side="left")
tk.Entry(contentField, relief="solid", bg="white", fg="black", bd=1, textvariable=contentValue).pack(side="left", fill="x", expand=True)

# Task Encode
encodeTask = tk.Frame(right, bg="#ececec")
encodeTask.pack(fill="x", pady=4)
tk.Button(encodeTask, text="Get Encode Task", bg="#ececec", relief="groove", width=15, command=encodeTaskButton).pack(side="left", padx=5)

# Task Decode
decodeTask = tk.Frame(right, bg="#ececec")
decodeTask.pack(fill="x", pady=4)
tk.Button(decodeTask, text="Get Decode Task", bg="#ececec", relief="groove", width=15, command=decodeTaskButton).pack(side="left", padx=5)

# Get DifHel Task
getDifHelTask = tk.Frame(right, bg="#ececec")
getDifHelTask.pack(fill="x", pady=4)
tk.Button(getDifHelTask, text="Get Diffie Hell Task", bg="#ececec", relief="groove", width=15, command=getDifHelTaskButton).pack(side="left", padx=5)

# DifHel generate space
difHelGenSpace = tk.Frame(right, bg="#ececec")
difHelGenSpace.pack(fill="x", pady=4)
tk.Button(difHelGenSpace, text="Generate Space", bg="#ececec", relief="groove", width=15, command=difHelGenSpaceButton).pack(side="left", padx=5)

# modular p field
pValue = tk.StringVar()
pField = tk.Frame(right, bg="#ececec")
pField.pack(fill="x", pady=10)
tk.Label(pField, text="Modular p:", bg="#ececec", fg="black").pack(side="left")
tk.Entry(pField, relief="solid", bg="white", fg="black", bd=1, textvariable=pValue).pack(side="left", fill="x", expand=True)

# modular point g field
gValue = tk.StringVar()
gField = tk.Frame(right, bg="#ececec")
gField.pack(fill="x", pady=10)
tk.Label(gField, text="DH generator world g:", bg="#ececec", fg="black").pack(side="left")
tk.Entry(gField, relief="solid", bg="white", fg="black", bd=1, textvariable=gValue).pack(side="left", fill="x", expand=True)

# DifHel half key
difHelHalfKey = tk.Frame(right, bg="#ececec")
difHelHalfKey.pack(fill="x", pady=4)
tk.Button(difHelHalfKey, text="Send Half Key", bg="#ececec", relief="groove", width=15, command=difHelHalfKeyButton).pack(side="left", padx=5)

# Dif Hel private Key field
privKeyValue = tk.StringVar()
privKeyField = tk.Frame(right, bg="#ececec")
privKeyField.pack(fill="x", pady=10)
tk.Label(privKeyField, text="DH private key p1:", bg="#ececec", fg="black").pack(side="left")
tk.Entry(privKeyField, relief="solid", bg="white", fg="black", bd=1, textvariable=privKeyValue).pack(side="left", fill="x", expand=True)

# Dif Hel Server Public Key field
publKeyValue = tk.StringVar()
publKeyField = tk.Frame(right, bg="#ececec")
publKeyField.pack(fill="x", pady=10)
tk.Label(publKeyField, text="[SERVER] public key :", bg="#ececec", fg="black").pack(side="left")
tk.Entry(publKeyField, relief="solid", bg="white", fg="black", bd=1, textvariable=publKeyValue).pack(side="left", fill="x", expand=True)

# DifHel send secret
difSendSecret = tk.Frame(right, bg="#ececec")
difSendSecret.pack(fill="x", pady=4)
tk.Button(difSendSecret, text="Send Secret", bg="#ececec", relief="groove", width=15, command=difHelSecretButton).pack(side="left", padx=5)

# Hashing task button
taskhash = tk.Frame(right, bg="#ececec")
taskhash.pack(fill="x", pady=4)
tk.Button(taskhash, text="Task Hash", bg="#ececec", relief="groove", width=15, command=taskhashButton).pack(side="left", padx=5)

# Hashing task verify button
taskhashverify = tk.Frame(right, bg="#ececec")
taskhashverify.pack(fill="x", pady=4)
tk.Button(taskhashverify, text="Verify Hash", bg="#ececec", relief="groove", width=15, command=taskhashverifyButton).pack(side="left", padx=5)

# Encode
encodeFrame = tk.Frame(right, bg="#ececec")
encodeFrame.pack(fill="x", pady=4)
tk.Button(encodeFrame, text="Encode", bg="#ececec", relief="groove", width=15, command=encodeButton).pack(side="left", padx=4)

# Decode
decodeFrame = tk.Frame(right, bg="#ececec")
decodeFrame.pack(fill="x", pady=4)
tk.Button(decodeFrame, text="Decode", bg="#ececec", relief="groove", width=15, command=decodeButton).pack(side="left", padx=4)

# Generate
genBtn = tk.Frame(right, bg="#ececec")
genBtn.pack(fill="x", pady=4)
tk.Button(genBtn, text="Generate", bg="#ececec", relief="groove", width=15, command=generateButton).pack(side="left", padx=5)

# ── ChatBox / Console Redirection ────────────────────────────────────────────────────────────────

class TextRedirector:
    def __init__(self, widget, original_stream):
        self.widget = widget
        self.original_stream = original_stream

    def write(self, output):
        # GUI update
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

update_visibility()
if __name__ == "__main__":
    root.mainloop()