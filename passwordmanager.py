import os
import ast
import random
import string
from random import randint
import tkinter as tk
import sqlite3
import hashlib
from tkinter import simpledialog
from functools import partial
import rsa_module
import usb_test

# Constants to specify necessary directories
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ROOT_DIR, 'password_manager.db')

# Creating the Database for the Passwords
with sqlite3.connect("password_manager.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usbdetails(
id INTEGER  PRIMARY KEY,
name TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS publickey(
id1 TEXT PRIMARY KEY,
id2 TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwordmanager(
id INTEGER  PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")



# Intermediate functions

# Random password generation
# Returns a randomly generated password of type string.
def random_pass():
    char_types = ["sym", "num", "upper", "lower"]
    pass_len = 20
    password = ""
    # Looping to progressively add symbols to make a password of length 20
    # There is an equal chance of adding an uppercase character, a lowercase character, a number, or a symbol
    for i in range(0, pass_len):
        choice_index = randint(0, 3)
        choice = char_types[choice_index]
        if choice == "sym":
            symbol_list = string.punctuation
            symbol = symbol_list[randint(0, len(symbol_list) - 1)]
            password = password + symbol
        elif choice == "num":
            num = randint(0, 9)
            password = password + str(num)
        elif choice == "upper":
            password = password + (random.choice(string.ascii_uppercase))
        else:
            password = password + (random.choice(string.ascii_lowercase))

    valid = isStrong(password)
    # If the password is invalid, make recursive call.
    if not valid[0]:
        random_pass()
    # Otherwise, return created password
    else:
        return password


# Function ensures attempted password strength.
# It must have an uppercase character, a lowercase character, a number, or a symbol
# It must have a minimum length of 10 characters
# Returns a list of boolean integers, where [0,0,0,0,0,0] Implies that:
# [0]: The password is invalid, [1]: The password is too short [2]: There are no uppercase characters
# [3]: There are no lowercase characters [4]: There are no numbers [5]: There are no symbols.
# If the code returned was [1,1,1,1,1,1], the opposite would be true for each condition.

def isStrong(password):
    return_code = [1, 0, 0, 0, 0, 0]

    if len(password) >= 10:
        return_code[1] = 1

    for i in range(0, len(password)):
        if password[i].isupper():
            return_code[2] = 1
        elif password[i].islower():
            return_code[3] = 1
        elif password[i].isdigit():
            return_code[4] = 1
        elif password[i] in string.punctuation:
            return_code[5] = 1

    # If any of the above conditions are not met, set validity to False
    for i in range(1, len(return_code)):
        if not return_code[i]:
            return_code[0] = 0

    return return_code


def hashing(x):
    hash = hashlib.sha256(x)
    hash = hash.hexdigest()
    return hash


# Main GUI
# Creating the main window
root = tk.Tk()


# for the popup
def popupbox(text):
    answer = simpledialog.askstring("Input String", text)
    return answer


# Creating the GUI for when a new user
def initial_screen():
    root.title("Password Manager")
    root.resizable(False, False)
    canvas = tk.Canvas(root, height=500, width=1000, bg="grey25")
    canvas.pack()
    frame = tk.Frame(root, bg="white")
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    tk.Label(root, text="Welcome to the Password Manager!", font=("Helvetica", 32, "bold"), bg="white",
             foreground="black").place(x=130, y=50)


    # tk.Label(root,
    #          text="Please enter the name.\nPassword Requirements:\nPasswords must:\n- Be 10 characters in length\nPasswords must contain:\n-"
    #               " an uppercase character\n- a lowercase character\n- a number\n- a symbol\n",
    #          font=("Arial", 14), bg="white", foreground="Black", justify="left").place(x=630, y=120)

    tk.Label(root,
             text="Please plug in the USB.\nIf not plugged in,\n1. Please close the Program \n2. Plug in the USB \n3. Relaunch the program",
             font=("Arial", 14), bg="white", foreground="Black", justify="left").place(x=630, y=120)


    tk.Label(root, text="Enter the name of the USB", font=("Arial", 18, "bold"), bg="white", foreground="Blue").place(
        x=155, y=120)
    txt = tk.Entry(border=2, show="*", width=50)
    txt.place(x=155, y=150)
    txt.focus()

    def show_password():
        if (txt.cget("show") == "*"):
            txt.config(show="")
        else:
            txt.config(show="*")

    tk.Checkbutton(root, text="Show Password", command=show_password, bg="white", foreground="black").place(x=155,
                                                                                                            y=180)

    tk.Label(root, text="Re-Enter the name of the USB", font=("Arial", 18, "bold"), bg="white", foreground="Blue").place(x=155,
                                                                                                                  y=210)
    txt2 = tk.Entry(border=2, show="*", width=50)
    txt2.place(x=155, y=245)

    def show_password():
        if (txt2.cget("show") == "*"):
            txt2.config(show="")
        else:
            txt2.config(show="*")

    tk.Checkbutton(root, text="Show Password", command=show_password, bg="white", foreground="black").place(x=155,
                                                                                                            y=275)
    tk.Button(root, text="Close", font=("Bahnschrift 20", 14, "bold"), bg="white", foreground="black", borderwidth=2,
              command=quit).place(x=380, y=390)

    def save_usb_details():
        if txt.get() != txt2.get():
            tk.Label(root, text="Entered names do not match!", font=("Arial", 10, "bold"), bg="white",
                     foreground="Red").place(x=170, y=450)
            
        # elif isStrong(txt.get())[0] == False:
        #     tk.Label(root, text="Password is weak.\n Requirements not met.", font=("Arial", 10, "bold"), bg="white",
        #              foreground="Red").place(x=170, y=450)

        else:
            usb_name = txt.get()

            if usb_test.find_usb_drive(usb_name):
                insert_pass = """INSERT INTO usbdetails(name)
                VALUES(?) """
                cursor.execute(insert_pass, [(usb_name)])
                db.commit()
                keys = rsa_module.keygen()
                e = str(keys[0])
                n = str(keys[1])
                d = str(keys[2])
                insert_key = """INSERT INTO publickey(id1, id2)
                VALUES(?, ?) """
                cursor.execute(insert_key, [e,n])
                db.commit()

                usb_test.store_security_key(usb_test.find_usb_drive(usb_name), d)

                popup = tk.Toplevel(root)
                popup.title("Password Manager Profile Created!")

                # Creating a label in the popup window
                label = tk.Label(popup, text="The USB and the keys were generated successfully!\nTo use the app, relaunch the app with the USB Drive plugged in", font=("Arial", 20, "bold"), foreground="Blue")
                label.pack(pady=10, padx = 10)

                def close_app():
                    popup.destroy()
                    root.destroy()

                # Create a button in the popup window to close the application
                close_button = tk.Button(popup, text="Close", command=close_app)
                close_button.pack(pady=5)

                # Ensure the popup window appears in the center of the screen
                popup.geometry("900x150")
                popup.transient(root)
                popup.grab_set()
                root.wait_window(popup)

            else:
                tk.Label(root, text="The USB drive is not plugged in, please plug in and retry!", font=("Arial", 10, "bold"), bg="white",
                     foreground="Red").place(x=170, y=450)

    tk.Button(root, text="Submit", font=("Bahnschrift 20", 14, "bold"), bg="white", foreground="black", borderwidth=2,
              command=save_usb_details).place(x=205, y=390)
    root.mainloop()


# Creating the GUI of the login screen
def login_screen():
    root.title("Password Manager")
    root.resizable(False, False)
    canvas = tk.Canvas(root, height=250, width=1000, bg="grey25")
    canvas.pack()
    frame = tk.Frame(root, bg="white")
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    tk.Label(root, text="Welcome to the Password Manager!", font=("Arial", 28, "bold"), bg="white",
             foreground="black").place(x=180, y=50)

    tk.Label(root, text="Please make sure to plug in the USB with the key and press the 'Unlock' Button", font=("Arial", 12, "bold"), bg="white", foreground="Red").place(x=190,y=100)

    def password_check():
        try:
            cursor.execute("SELECT * FROM usbdetails")
            det = cursor.fetchall()
            usb_name = det[0][1]
            # print(usb_name)

            if usb_test.find_usb_drive(usb_name):
                priv = usb_test.get_security_key(usb_test.find_usb_drive(usb_name))
                if priv:
                    password_manager(priv)

                else:
                    popup = tk.Toplevel(root)
                    popup.title("Error!")

                    # Creating a label in the popup window
                    label = tk.Label(popup, text="The key stored in the USB is Empty!\nFor security reasons, please create a new profile!", font=("Arial", 20, "bold"), foreground="Blue")
                    label.pack(pady=10, padx = 10)

                    def close_app():
                        popup.destroy()
                        root.destroy()

                    # Create a button in the popup window to close the application
                    close_button = tk.Button(popup, text="Close", command=close_app)
                    close_button.pack(pady=5)

                    # Ensure the popup window appears in the center of the screen
                    popup.geometry("900x150")
                    popup.transient(root)
                    popup.grab_set()
                    root.wait_window(popup)
            
            else:
                popup = tk.Toplevel(root)
                popup.title("No USB Drive Found!")

                # Creating a label in the popup window
                label = tk.Label(popup, text="The Application could not find the USB Drive.\nPlease plug in the correct USB drive\n or Please try unplugging and Plugging it back again ", font=("Arial", 20, "bold"), foreground="Blue")
                label.pack(pady=10, padx = 10)

                def close_app():
                    popup.destroy()

                # Create a button in the popup window to close the application
                close_button = tk.Button(popup, text="Retry", command=close_app)
                close_button.pack(pady=5)

                # Ensure the popup window appears in the center of the screen
                popup.geometry("900x150")
                popup.transient(root)
                popup.grab_set()
                root.wait_window(popup)
        except:
            tk.Label(root, text="Some Error Occurred", font=("Arial", 14, "bold"), bg="white", foreground="red").place(x=140,
                                                                                                                  y=340)

    tk.Button(root, text="Unlock", font=("Bahnschrift 20", 14, "bold"), bg="white", foreground="black",  borderwidth=2, command=password_check).place(x=350, y=150)
    tk.Button(root, text="Close", font=("Bahnschrift 20", 14, "bold"), bg="white", foreground="black", borderwidth=2, command=quit).place(x=450, y=150)

    root.mainloop()


# This lets the USER inside the Password Manager actually
def password_manager(priv):
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Password Manager")

    def add_entry():
        text1 = "Website"
        text2 = "Username"
        text3 = "Password"

        website = popupbox(text1)
        username = popupbox(text2)
        password = popupbox(text3)

        enc_pass = str(rsa_module.encrypt((e,n), password))
        print(enc_pass)

        insert_fields = """INSERT INTO passwordmanager(website,username,password)
        VALUES(?, ?, ?)"""

        cursor.execute(insert_fields, (website, username, enc_pass))

        db.commit()
        password_manager(priv)

    root.geometry("1100x340")
    priv = int(priv)
    cursor.execute("select * from publickey")
    det = cursor.fetchall()
    e = int(det[0][0])
    n = int(det[0][1])

    # print("Private:", priv)
    # print("e:", e)
    # print("n:", n)

    lb = tk.Label(root, text="Welcome to the Password Manager!!", font=("Arial", 18, "bold"), foreground="RED")
    lb.grid(column=1, padx=150)
    but = tk.Button(root, text="ADD", font=("Arial", 13, "bold"), bg="white", foreground="Green", command=add_entry)
    but.grid(column=1, row=2)

    def remove_entry(input):
        cursor.execute("DELETE FROM passwordmanager where id = ?", (input,))
        db.commit()
        password_manager(priv)


    lbl = tk.Label(root, text="WEBSITE", font=("Arial", 13, "bold"), foreground="black")
    lbl.grid(row=3, column=0)
    lbl = tk.Label(root, text="USERNAME", font=("Arial", 13, "bold"), foreground="black")
    lbl.grid(row=3, column=1)
    lbl = tk.Label(root, text="PASSWORD", font=("Arial", 13, "bold"), foreground="black")
    lbl.grid(row=3, column=2)
    cursor.execute("SELECT * FROM passwordmanager")

    try:
        if (cursor.fetchall() != None):
            i = 0
            while True:
                cursor.execute("SELECT * FROM passwordmanager")
                array = cursor.fetchall()

                lbl1 = tk.Label(root, text=(array[i][1]), font=("Arial", 13,), foreground="black")
                lbl1.grid(column=0, row=i + 4)
                print(array[i][1])

                lbl1 = tk.Label(root, text=(array[i][2]), font=("Arial", 13,), foreground="black")
                lbl1.grid(column=1, row=i + 4)
                print(array[i][2])
                print(array[i][3])
                data = ast.literal_eval(array[i][3])
                print(data)
                dec_data = rsa_module.decrypt(priv, (e,n), data)
                print(dec_data)
                lbl1 = tk.Label(root, text=(dec_data), font=("Arial", 13,), foreground="black")
                lbl1.grid(column=2, row=i + 4)

                button = tk.Button(root, text="Delete", command=partial(remove_entry, array[i][0]))
                button.grid(column=3, row=i + 4)
                i = i + 1
                cursor.execute("SELECT * FROM passwordmanager")
                if (len(cursor.fetchall()) <= 1):
                    break
    except:
        print("Keep Calm and Store Passwords")


cursor.execute("SELECT * FROM usbdetails")
if cursor.fetchall():
    login_screen()
else:
    initial_screen()
