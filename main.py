import pandas
import random
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"

try:
    words_file = pandas.read_csv("Words_to_learn.csv").to_dict(orient="records")
except FileNotFoundError:
    words_file = pandas.read_csv("data/french_words.csv").to_dict(orient="records")
else:
    word_in_french = ""
    word_in_english = ""
    question_number = 0

    cards_know = []


    def generate_card():
        global word_in_english, word_in_french, question_number
        print(words_file)
        print(len(words_file))
        if question_number > len(words_file) - 1:
            question_number = 0
            window.after_cancel(10000)
            print("Game Over")
        if question_number in cards_know:
            question_number += 1
            generate_card()
        word_in_french = words_file[question_number]['French']
        word_in_english = words_file[question_number]['English']
        canvas.itemconfig(title_label, text="French")

        canvas.itemconfig(canvas_img, image=front_image)
        canvas.itemconfig(word_label, text=word_in_french)


    def show_answer():
        global question_number
        canvas.itemconfig(title_label, text="English")
        canvas.itemconfig(word_label, text=word_in_english)
        canvas.itemconfig(canvas_img, image=back_image)
        question_number += 1
        window.after(3000, generate_card)


    def add_to_know():
        words_file.pop(question_number)
        words_to_learn = words_file
        words_to_learn = pandas.DataFrame(words_file)
        words_to_learn.to_csv("Words_to_learn.csv", index=False)
        generate_card()


    # ------------UI---------------------------
    window = Tk()
    window.title("Flashy")
    window.config(width=1200, height=1000, bg=BACKGROUND_COLOR, padx=40, pady=40)

    canvas = Canvas(highlightthickness=0, bg=BACKGROUND_COLOR)

    right_button_img = PhotoImage(file="images/right.png")
    wrong_button_img = PhotoImage(file="images/wrong.png")

    canvas.config(width=850, height=580)
    canvas.grid(row=1, column=2, columnspan=2)

    front_image = PhotoImage(file="images/card_front.png")
    back_image = PhotoImage(file="images/card_back.png")

    canvas_img = canvas.create_image(400, 270, image=front_image)

    wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=show_answer)
    wrong_button.grid(row=2, column=2)

    right_button = Button(image=right_button_img, highlightthickness=0, command=add_to_know)
    right_button.grid(row=2, column=3)

    title_label = canvas.create_text(400, 135, text="Title", font=("Regular", 40, "italic"), fill="black")

    word_label = canvas.create_text(400, 250, text="Word", font=("Regular", 70, "bold"), fill="black")

    generate_card()
    window.mainloop()
