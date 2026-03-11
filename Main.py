from tkinter import Label, Button

import openai
import tkinter as tk


window = tk.Tk()
window.title("AI Quiz")
window.geometry("600x500")
window.configure(bg="#1e1e1e")
window.resizable(False, False)

points = 0
correct = ""
slash = 0

QuestionLbl = Label(window, text="Password Generator", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="#ffffff", wraplength=500, justify="center" )
QuestionLbl.pack(pady=30)

YesBtn = Button(window, text="Yes", font=("Arial", 24, "bold"),bg="green", fg="#ffffff",command=lambda: points_system("yes"))
YesBtn.place(x=150,y=180)

NoBtn = Button(window, text="No", font=("Arial", 24, "bold"),bg="red", fg="#ffffff",command=lambda: points_system("no"))
NoBtn.place(x=390,y=180)

PointsLbl = Label(window, text="Points: ", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="#ffffff", wraplength=500, justify="center" )
PointsLbl.place(x=240,y=270)

client = openai.OpenAI(api_key = "") # Put your API key here

def generate_question():
    global QuestionLbl, correct, slash
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": (
                "You are an educational quiz generator for students up to 18 years old. "
                "Generate a yes/no question in English about astronomy or astrophysics that is interesting, engaging, and thought-provoking. "
                "The question should be understandable without advanced knowledge but should require some reasoning or understanding of basic concepts, rather than trivial facts. "
                "Return the output strictly in this format: 'Question: <your question here> | Answer: <Yes or No>'"
                "Do not include explanations, extra text, or examples."
            )},
            {"role": "user", "content": "Generate a simple yes/no question."}
        ]
    )
    result = response.choices[0].message.content.strip()
    question_part , answer_part = result.split(" | ")
    question = question_part.replace("Question: ", "").strip()
    correct = answer_part.replace("Answer: ", "").strip().lower()

    QuestionLbl.configure(text=question)

def points_system(correct_asnwer):
    global points,slash
    if correct_asnwer == correct:
        points += 1
    PointsLbl.configure(text=f"Points: {points}/{slash+1}")

    generate_question()

    slash+=1

    max_questions()

def max_questions():
    global points, slash, QuestionLbl, YesBtn, NoBtn, PointsLbl, RestartBtn, CongratsLblb
    if slash>=5:
        QuestionLbl.pack_forget()
        YesBtn.destroy()
        NoBtn.destroy()

        if points == 5:
            congrats = "You are an expert!"
        elif points in [3, 4]:
            congrats = "You know your stuff"
        elif points in [1, 2]:
            congrats = "Decent"
        else:  # points == 0
            congrats = "Bad"

        CongratsLblb = Label(window,text=congrats,font=("Arial", 28, "bold"),bg="#1e1e1e",fg="white")
        CongratsLblb.pack(pady=100)

        RestartBtn = Button(window, text="Restart", font=("Arial", 28, "bold"), bg="#1e1e1e", fg="white",command=restart)
        RestartBtn.place(x=220,y=320)


def restart():
    global points, slash, RestartBtn, CongratsLblb
    points=0
    slash=0

    RestartBtn.destroy()
    CongratsLblb.destroy()

    QuestionLbl.pack(pady=30)

    YesBtn = Button(window, text="Yes", font=("Arial", 24, "bold"), bg="green", fg="#ffffff",
                    command=lambda: points_system("yes"))
    YesBtn.place(x=150, y=180)

    NoBtn = Button(window, text="No", font=("Arial", 24, "bold"), bg="red", fg="#ffffff",
                   command=lambda: points_system("no"))
    NoBtn.place(x=390, y=180)

    PointsLbl = Label(window, text="Points: ", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="#ffffff", wraplength=500,
                      justify="center")
    PointsLbl.place(x=240, y=270)

    PointsLbl.config(text=f"Points: {points}")

    generate_question()


generate_question()

window.mainloop()



