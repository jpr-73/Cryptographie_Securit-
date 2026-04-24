import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext # On garde ça juste au cas où, mais on va utiliser CTkTextbox
import sys
import interpretCommand

ctk.set_appearance_mode("light") # ou "dark"
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    print("\033[91m {}\033[00m".format("Error: Run main.py instead."))
    sys.exit(1)

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
        hashETverify.pack_forget()
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
        verifyhashbutton.pack_forget()
        sendhashbutton.pack_forget()
        clearValuesBtn.pack_forget()


        selected_mode = mode_var.get()

        if selected_mode == "Single Shift":
            encETdec.pack(fill="x", pady=5, after=modeTab)
            keyField.pack(fill="x", pady=10, after=encETdec)

            last_widget = keyField

            selected_mode4 = sub_mode1.get()

            if selected_mode4 == "Encode" :
                encodeTask.pack(fill="x", pady=10, after=last_widget)
                encodeFrame.pack(fill="x", pady=10, after=encodeTask)
                last_widget = encodeFrame

            if selected_mode4 == "Decode":
                decodeTask.pack(fill="x", pady=10, after=last_widget)
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
            hashETverify.pack(fill="x", pady=10, after=modeTab)
            last_widget = hashETverify
            selected_mode3 = sub_mode2.get()

            if selected_mode3 == "Hash":
                taskhash.pack(fill="x", pady=10, after=last_widget)
                sendhashbutton.pack(fill="x", pady=10, after=taskhash)
                last_widget = sendhashbutton

            if selected_mode3 == "Verify":
                taskhashverify.pack(fill="x", pady=10, after=last_widget)
                verifyhashbutton.pack(fill="x", pady=10, after=taskhashverify)
                last_widget = verifyhashbutton

        elif selected_mode == "RSA":
            encETdec.pack(fill="x", pady=5, after=modeTab)
            last_widget = encETdec

            selected_mode2 = sub_mode1.get()

            if selected_mode2 == "Encode":
                encodeTask.pack(fill="x", pady=10, after=last_widget)
                modField.pack(fill="x", pady=10, after=encodeTask)
                eField.pack(fill="x", pady=10, after=modField)
                encodeFrame.pack(fill="x", pady=10, after=eField)
                last_widget = encodeFrame

            if selected_mode2 == "Decode":
                decodeTask.pack(fill="x", pady=5, after=last_widget)
                genBtn.pack(fill="x", pady=10, after=decodeTask)
                modField.pack(fill="x", pady=10, after=genBtn)
                dField.pack(fill="x", pady=10, after=modField)

                contentField.pack(fill="x", pady=10, after=dField)
                decodeFrame.pack(fill="x", pady=10, after=contentField)
                last_widget = decodeFrame


        elif selected_mode == "Vigenere":
            keyField.pack(fill="x", pady=10, after=modeTab)
            encodeTask.pack(fill="x", pady=10, after=keyField)
            encodeFrame.pack(fill="x", pady=10, after=encodeTask)
            #decodeTask.pack(fill="x", pady=10, after=encodeFrame)
            #decodeFrame.pack(fill="x", pady=10, after=decodeTask)
            last_widget = encodeFrame #change to "decodeFrame" if they are done 
    
        clearValuesBtn.pack(side="bottom", anchor="e", pady=10)

        root.update_idletasks()

    except Exception as e:
        print(e)
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
    except Exception as e:
        print(f"Error: {e}")


def getDifHelTaskButton():
    try :
        interpretCommand.interpret("/task DifHel")
    except Exception as e:
        print(f"Error: {e}")

def difHelGenSpaceButton():
    try :
        interpretCommand.interpret("/generate dh")
    except Exception as e:
        print(f"Error: {e}")

def difHelHalfKeyButton():
    try :
        interpretCommand.interpret(f"/generate dh-hk {pValue.get()} {gValue.get()}")
    except Exception as e:
        print(f"Error: {e}")

def difHelSecretButton():
    try :
        #print(f"/generate dh-secret {pValue.get()} {privKeyValue.get()} {publKeyValue.get()}")
        interpretCommand.interpret(f"/generate dh-secret {pValue.get()} {privKeyValue.get()} {publKeyValue.get()}")
    except Exception as e:
        print(f"Error: {e}")

def taskhashButton():
    try :
        interpretCommand.interpret(f"/task hash hash")
    except Exception as e:
        print(f"Error: {e}")

def taskhashverifyButton():
    try :
        interpretCommand.interpret(f"/task hash verify")
    except Exception as e:
        print(f"Error: {e}")

def sendhashButton():
    try :
        interpretCommand.interpret(f"/encode hash")
    except Exception as e:
        print(f"Error: {e}")

def verifyhashButton():
    try :
        interpretCommand.interpret(f"/decode hash")
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
    except Exception as e:
        print(f"Error: {e}")

def empty_values() :
    keyValue.set("")
    modValue.set("")
    eValue.set("")
    dValue.set("")
    contentValue.set("")
    gValue.set("")
    pValue.set("")
    privKeyValue.set("")
    publKeyValue.set("")
    inputtext.set("")

def are_You_Stupid(mode):
    if (inputtext.get() == "" and mode == 'i'):
        print("\nYou might want to decide a length, maybe ?\n")
    if (keyValue.get() == "" and mode == 'k'):
        print("\nYou might want to give me a key, maybe ?\n")

# ── GUI ────────────────────────────────────────────────────────────────
root = ctk.CTk()
root.title("Secret Communication Channel")
icon_img = tk.PhotoImage(file="icon.png")
root.wm_iconphoto(True, icon_img)
root.geometry("1000x650")
root.lift()
root.focus_force()
root.configure(fg_color="#ececec")

# ── Top bar ────────────────────────────────────────────────────────────────
topbarcolor = tk.StringVar(value="red")
statusbar = ctk.CTkFrame(root, fg_color=topbarcolor.get(), height=4)
statusbar.pack(fill="x")

# ── Layout ─────────────────────────────────────────────────────────────────
left = ctk.CTkFrame(root, fg_color="#ececec", width=360)
left.pack(side="left", fill="y", padx=8, pady=8)
left.pack_propagate(False)

ctk.CTkFrame(root, fg_color="#cccccc", width=1).pack(side="left", fill="y")

right = ctk.CTkFrame(root, fg_color="#ececec")
right.pack(side="left", fill="both", expand=True, padx=10, pady=8)

# ── Left: chat history ──────────────────────────────────────────────────────
chat = ctk.CTkTextbox(left, fg_color="white", text_color="black")
chat.pack(fill="both", expand=True)

# ── Right: controls ─────────────────────────────────────────────────────────

# Checkbox + Text/Image tabs
r1 = ctk.CTkFrame(right, fg_color="#ececec")
r1.pack(fill="x", pady=(0, 6))
ctk.CTkCheckBox(r1, text="Send to Server only", text_color="black", command=sendtoserver).pack(side="left")
#tab_var = tk.StringVar(value="Text")
#for t in ("Image", "Text"):
#    ctk.CTkRadioButton(r1, text=t, variable=tab_var, value=t, text_color="black").pack(side="right", padx=1)

# Input box
inputtext = tk.StringVar()
input_box = ctk.CTkEntry(right, fg_color="white", text_color="black", textvariable=inputtext)
input_box.pack(fill="x", pady=(0, 6))

# Send Clear
ctk.CTkButton(right, text="Send Clear",  command=clearbutton, fg_color="#ececec", text_color="black", border_width=1,
          width=10).pack(anchor="e", pady=(2, 6))

# Mode tabs
modeTab = ctk.CTkFrame(right, fg_color="#ececec")
modeTab.pack(pady=4)
mode_var = tk.StringVar(value="Single Shift")
mode_segmented = ctk.CTkSegmentedButton(
    modeTab,
    values=["Single Shift", "Vigenere", "RSA", "DiffieHellman", "Hashing"],
    command=update_visibility,
    variable=mode_var,
    fg_color="#ececec",
    border_width=1,
    unselected_color="#444444",
    selected_color="#3B8ED0",
    selected_hover_color="#3B8ED0",
    text_color="white"
)
mode_segmented.pack(pady=10)

sub_mode1 = tk.StringVar(value="Encode")
sub_mode2 = tk.StringVar(value="Hash")

encETdec = ctk.CTkFrame(right, fg_color="#ececec")
encETdec.pack(pady=4)
for m2 in ("Encode", "Decode"):
    ctk.CTkRadioButton(encETdec, text=m2, variable=sub_mode1,value=m2, text_color="black", command=update_visibility).pack(side="left", padx=2)

hashETverify = ctk.CTkFrame(right, fg_color="#ececec")
hashETverify.pack(pady=4)
for m2 in ("Hash", "Verify"):
    ctk.CTkRadioButton(hashETverify, text=m2, variable=sub_mode2,value=m2, text_color="black", command=update_visibility).pack(side="left", padx=2)

# Key field
keyValue = tk.StringVar()
keyField = ctk.CTkFrame(right, fg_color="#ececec")
keyField.pack(fill="x", pady=10)
ctk.CTkLabel(keyField, text="Key :", text_color="black").pack(side="left")
ctk.CTkEntry(keyField, fg_color="white", text_color="black", textvariable=keyValue).pack(side="left", fill="x", expand=True)

# Modular field
modValue = tk.StringVar()
modField = ctk.CTkFrame(right, fg_color="#ececec")
modField.pack(fill="x", pady=10)
ctk.CTkLabel(modField, text="Modular :", text_color="black").pack(side="left")
ctk.CTkEntry(modField, fg_color="white", text_color="black", textvariable=modValue).pack(side="left", fill="x", expand=True)

# public key field d
dValue = tk.StringVar()
dField = ctk.CTkFrame(right, fg_color="#ececec")
dField.pack(fill="x", pady=10)
ctk.CTkLabel( dField, text="d :", text_color="black").pack(side="left")
ctk.CTkEntry( dField, fg_color="white", text_color="black", textvariable=dValue).pack(side="left", fill="x", expand=True)


# e field
eValue = tk.StringVar()
eField = ctk.CTkFrame(right, fg_color="#ececec")
eField.pack(fill="x", pady=10)
ctk.CTkLabel(eField, text="e :", text_color="black").pack(side="left")
ctk.CTkEntry(eField, fg_color="white", text_color="black",textvariable=eValue).pack(side="left", fill="x", expand=True)

# Content field
contentValue = tk.StringVar()
contentField = ctk.CTkFrame(right, fg_color="#ececec")
contentField.pack(fill="x", pady=10)
ctk.CTkLabel(contentField, text="Content :", text_color="black").pack(side="left")
ctk.CTkEntry(contentField, fg_color="white", text_color="black", textvariable=contentValue).pack(side="left", fill="x", expand=True)

# Task Encode
encodeTask = ctk.CTkFrame(right, fg_color="#ececec")
encodeTask.pack(fill="x", pady=4)
ctk.CTkButton(encodeTask, text="Get Encode Task", fg_color="#ececec", text_color="black", border_width=1, width=15, command=encodeTaskButton).pack(side="left", padx=5)

# Task Decode
decodeTask = ctk.CTkFrame(right, fg_color="#ececec")
decodeTask.pack(fill="x", pady=4)
ctk.CTkButton(decodeTask, text="Get Decode Task", fg_color="#ececec", text_color="black", border_width=1, width=15, command=decodeTaskButton).pack(side="left", padx=5)

# Get DifHel Task
getDifHelTask = ctk.CTkFrame(right, fg_color="#ececec")
getDifHelTask.pack(fill="x", pady=4)
ctk.CTkButton(getDifHelTask, text="Get Diffie Hell Task", fg_color="#ececec", text_color="black", border_width=1, width=15, command=getDifHelTaskButton).pack(side="left", padx=5)

# DifHel generate space
difHelGenSpace = ctk.CTkFrame(right, fg_color="#ececec")
difHelGenSpace.pack(fill="x", pady=4)
ctk.CTkButton(difHelGenSpace, text="Generate Space", fg_color="#ececec", text_color="black", border_width=1, width=15, command=difHelGenSpaceButton).pack(side="left", padx=5)

# modular p field
pValue = tk.StringVar()
pField = ctk.CTkFrame(right, fg_color="#ececec")
pField.pack(fill="x", pady=10)
ctk.CTkLabel(pField, text="Modular p:", text_color="black").pack(side="left")
ctk.CTkEntry(pField, fg_color="white", text_color="black",textvariable=pValue).pack(side="left", fill="x", expand=True)

# modular point g field
gValue = tk.StringVar()
gField = ctk.CTkFrame(right, fg_color="#ececec")
gField.pack(fill="x", pady=10)
ctk.CTkLabel(gField, text="DH generator world g:", text_color="black").pack(side="left")
ctk.CTkEntry(gField, fg_color="white", text_color="black",  textvariable=gValue).pack(side="left", fill="x", expand=True)

# DifHel half key
difHelHalfKey = ctk.CTkFrame(right, fg_color="#ececec")
difHelHalfKey.pack(fill="x", pady=4)
ctk.CTkButton(difHelHalfKey, text="Send Half Key", fg_color="#ececec", text_color="black", border_width=1, width=15, command=difHelHalfKeyButton).pack(side="left", padx=5)

# Dif Hel private Key field
privKeyValue = tk.StringVar()
privKeyField = ctk.CTkFrame(right, fg_color="#ececec")
privKeyField.pack(fill="x", pady=10)
ctk.CTkLabel(privKeyField, text="DH private key p1:", text_color="black").pack(side="left")
ctk.CTkEntry(privKeyField, fg_color="white", text_color="black", textvariable=privKeyValue).pack(side="left", fill="x", expand=True)

# Dif Hel Server Public Key field
publKeyValue = tk.StringVar()
publKeyField = ctk.CTkFrame(right, fg_color="#ececec")
publKeyField.pack(fill="x", pady=10)
ctk.CTkLabel(publKeyField, text="[SERVER] public key :", text_color="black").pack(side="left")
ctk.CTkEntry(publKeyField, fg_color="white", text_color="black",textvariable=publKeyValue).pack(side="left", fill="x", expand=True)

# DifHel send secret
difSendSecret = ctk.CTkFrame(right, fg_color="#ececec")
difSendSecret.pack(fill="x", pady=4)
ctk.CTkButton(difSendSecret, text="Send Secret", fg_color="#ececec", text_color="black", border_width=1, width=15, command=difHelSecretButton).pack(side="left", padx=5)

# Hashing task button
taskhash = ctk.CTkFrame(right, fg_color="#ececec")
taskhash.pack(fill="x", pady=4)
ctk.CTkButton(taskhash, text="Get Task", fg_color="#ececec", text_color="black", border_width=1, width=15, command=taskhashButton).pack(side="left", padx=5)

# Hashing task verify button
taskhashverify = ctk.CTkFrame(right, fg_color="#ececec")
taskhashverify.pack(fill="x", pady=4)
ctk.CTkButton(taskhashverify, text="Get Task",  fg_color="#ececec", text_color="black", border_width=1, width=15, command=taskhashverifyButton).pack(side="left", padx=5)

# Hashing send hash button
sendhashbutton = ctk.CTkFrame(right, fg_color="#ececec")
sendhashbutton.pack(fill="x", pady=4)
ctk.CTkButton(sendhashbutton, text="Send Hash", fg_color="#ececec", text_color="black", border_width=1, width=15, command=sendhashButton).pack(side="left", padx=5)

# Hashing verify hash button
verifyhashbutton = ctk.CTkFrame(right, fg_color="#ececec")
verifyhashbutton.pack(fill="x", pady=4)
ctk.CTkButton(verifyhashbutton, text="Verify Hash", fg_color="#ececec", text_color="black", border_width=1, width=15, command=verifyhashButton).pack(side="left", padx=5)

# Encode
encodeFrame = ctk.CTkFrame(right, fg_color="#ececec")
encodeFrame.pack(fill="x", pady=4)
ctk.CTkButton(encodeFrame, text="Encode", fg_color="#ececec", text_color="black", border_width=1, width=15, command=encodeButton).pack(side="left", padx=4)

# Decode
decodeFrame = ctk.CTkFrame(right, fg_color="#ececec")
decodeFrame.pack(fill="x", pady=4)
ctk.CTkButton(decodeFrame, text="Decode",fg_color="#ececec", text_color="black", border_width=1, width=15, command=decodeButton).pack(side="left", padx=4)

# Generate
genBtn = ctk.CTkFrame(right, fg_color="#ececec")
genBtn.pack(fill="x", pady=4)
ctk.CTkButton(genBtn, text="Generate", fg_color="#ececec", text_color="black", border_width=1, width=15, command=generateButton).pack(side="left", padx=5)

# Clear Button
clearValuesBtn = ctk.CTkFrame(right, fg_color="#ececec")
clearValuesBtn.pack(fill="x", pady=4)
ctk.CTkButton(clearValuesBtn, text="Clear Inputs", fg_color="#ececec", text_color="black", border_width=1, width=15, command=empty_values).pack(side="left", padx=5)


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
                statusbar.configure(fg_color=topbarcolor.get())
                root.attributes('-topmost', False)

        def append_text():
            self.widget.configure(state="normal")
            self.widget.insert(tk.END, output.replace("[K", "").replace(">", ""))
            self.widget.configure(state="disabled")
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