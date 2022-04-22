from tkinter import *
from turtle import back
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
#-----------------------------------------
try:
    data = pandas.read_csv("eng_to_tr.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/eng_to_tr.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn =data.to_dict(orient="records")
def next_card():
    global current_card,flip_timer
    windows.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title,text="English",fill="black")
    canvas.itemconfig(card_word,text=current_card["English"],fill="black")
    canvas.itemconfig(background,image=front_image)
    windows.after(3000,func=flip_the_card)

def flip_the_card():
    canvas.itemconfig(card_title,text="Turkish",fill="white")
    canvas.itemconfig(card_word,text=current_card["Turkish"],fill="white")
    canvas.itemconfig(background,image=card_back)

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv",index=False)
    next_card()

#------USER INTERFACE-------
windows = Tk()
windows.title("Flash Cards")
windows.config(padx=55,pady=55,bg=BACKGROUND_COLOR)

flip_timer = windows.after(3000,func=flip_the_card)


canvas = Canvas(width=800,height=526)
front_image = PhotoImage(file="card_front.png")
card_back = PhotoImage(file="card_back.png")
background = canvas.create_image(400,263,image=front_image)
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
card_title = canvas.create_text(400,150,fill='black',text="",font=("Ariel",40,"italic"))
card_word = canvas.create_text(400,263,fill='black',text="",font=("Ariel",60,"italic"))
canvas.grid(row=0,column=0,columnspan=2)

wrong_image = PhotoImage(file="wrong.png")
dont_know_button = Button(image=wrong_image,border=0,command=next_card,highlightthickness=0)
dont_know_button.grid(column=0,row=1)

true_image = PhotoImage(file="right.png")
check_button = Button(image=true_image,border=0,highlightthickness=0,command=is_known)
check_button.grid(column=1,row=1)

next_card()

windows.mainloop()
