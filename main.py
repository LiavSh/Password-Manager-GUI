from data import letters, capital_letters, symbols, nums
from random import choice
import json
from tkinter import *

FONT = ('ariel', 15, 'bold')
BG = "whitesmoke"
PASSLENGTH = 18

# ------------------------------ POP-UP MESSAGES --------------------------------- #


# Creating method for pop-up windows
def pop_up(message, typo):
    # top-level window
    pop_up_window = Toplevel(window)
    pop_up_window.title(typo)
    pop_up_window.config(width=500, height=300, pady=15, padx=15, bg=BG)

    # uploading photo
    pop_img = PhotoImage(file="pngs/"+typo+".png")
    pop_up_image_pres = Label(pop_up_window, image=pop_img, bg=BG, padx=30, pady=30)
    pop_up_image_pres.grid(column=0, row=0, rowspan=2)

    # label (warning text)
    pop_up_label = Label(pop_up_window)
    pop_up_label.config(text=message, bg=BG, font=FONT, pady=5, padx=10)
    pop_up_label.grid(row=0, column=1)

    # Button pop-up
    pop_up_button = Button(pop_up_window)
    pop_up_button.config(text="OK", bd=0, command=pop_up_window.destroy, width=8, highlightthickness=0)
    pop_up_button.grid(column=1, row=1, padx=5, pady=5)

    pop_up_window.mainloop()


# ------------------------------ SEARCH PASSWORD --------------------------------- #


def search_pass():
    try:
        # try open file (if exist)
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    # if file not exist
    except FileNotFoundError:
        pop_up(message="There are no saved passwords!", typo="Warning")
    else:
        # file exist
        website_name = website_input.get()
        try:
            key = data[website_name]
        except KeyError:
            # no saved password for the website
            pop_up(message="There are no saved passwords for this website!", typo="Warning")
        else:
            pop_up(message=f"Website: {website_name}\nUser Name: {key['email']}\nPassword: {key['Password']}",
                   typo="Search password")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_pass():
    password_input.delete(0, END)
    data = [letters, capital_letters, symbols, nums]
    pass_list = []

    for i in range(PASSLENGTH):
        pass_list.append(choice(choice(data)))

    password_input.insert(0, ''.join(pass_list))


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_pass():
    website = website_input.get()
    mail = email_input.get()
    password = password_input.get()

    new_data = {
        website: {
            "email": mail,
            "Password": password,
        }
    }

    if not website or not mail or not password:
        pop_up(message="One or more parameter missing!", typo="Warning")
    else:
        try:
            # try open file (if exist)
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        # if file not exist
        except:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        # file from 'try' found - updating JSON
        else:
            data.update(new_data)

            # writing back
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        # anyway clear entries and pop-up message to the user
        finally:
            website_input.delete(0, END)
            email_input.delete(0, END)
            password_input.delete(0, END)
            pop_up(message="Password added successfully!", typo="Password added")


# ---------------------------- UI SETUP ------------------------------- #


# window
window = Tk()
window.title("Password Manager")
window.config(width=200, height=200, padx=50, pady=50, bg=BG)


# canvas (lock photo)
canvas = Canvas(window, width=200, height=200, highlightthickness=0, bg=BG)
lock_img = PhotoImage(file="pngs/logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)


# website feature
# website label
website_label = Label()
website_label.config(text="Website: ", font=FONT, bg=BG)
website_label.grid(column=0, row=1, pady=5)
# website entry
website_input = Entry()
website_input.config(width=21, highlightthickness=0)
website_input.focus()
website_input.grid(column=1, row=1, pady=5)


# Email/Username feature
# Email/Username label
email_label = Label()
email_label.config(text="Email / Username: ", font=FONT, bg=BG)
email_label.grid(column=0, row=2, pady=5)
# Email/Username entry
email_input = Entry()
email_input.config(width=35, highlightthickness=0)
email_input.grid(column=1, row=2, columnspan=2, pady=5)


# Password feature
# password label
password_label = Label()
password_label.config(text="Password: ", font=FONT, bg=BG)
password_label.grid(column=0, row=3, pady=5)
# Password entry
password_input = Entry()
password_input.config(width=21, highlightthickness=0)
password_input.grid(column=1, row=3, pady=5)
# password button
password_button = Button()
password_button.config(text="Generate Password", fg="firebrick", bd=0, command=generate_pass)
password_button.grid(column=2, row=3, pady=5)


# Add feature
add_button = Button()
add_button.config(text="Add", width=35, fg="firebrick", bd=0, highlightthickness=1, command=save_pass)
add_button.grid(column=1, row=4, columnspan=2, padx=5, pady=15)


# Search button
search_button = Button()
search_button.config(text="Search", fg="firebrick", bd=0, command=search_pass, width=13)
search_button.grid(column=2, row=1, padx=5, pady=5)

window.mainloop()
