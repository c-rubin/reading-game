import os
import ctypes

from tkinter import *

if __name__ == '__main__':
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

chapter = 1
part = 0
data = []
questionIndex = 0
questions = []
answers = []

items = {
    'item_one': 'negative score from one question is zeroed once',
    'item_two': 'bonus one hundred points once',
    'item_three': 'bad answers give less negative score'
}

item_usage = 0

current_item = 0
score = 0
rightAnswerCount = 0
wrongAnswerCount = 0

root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (w, h))

label = Label(root, font=('Castellar', 16, 'bold'), pady=10)
label.pack()

text = Text(
    root,
    height=12,
    wrap=WORD,
    font=('Castellar', 16),
    spacing1=10,
    spacing2=10,
    spacing3=10
)

text.tag_configure('center', justify='center')
text.pack(padx=150, pady=20)

area = Frame(root, height=1.5, width=8)

photoNext = PhotoImage(file=r'' + os.path.dirname(__file__) + '/assets/right.png')
photoPrev = PhotoImage(file=r'' + os.path.dirname(__file__) + '/assets/outline_reply_black_24dp.png')

quiz = Frame(root)

item_frame = Frame(root)
item_frame.pack()


def load_part():
    quiz.pack_forget()

    text.configure(state='normal')
    text.delete(1.0, END)
    text.insert(END, data[part])
    text.configure(state='disabled')
    text.tag_add('center', '1.0', 'end')
    text.pack(padx=150, pady=20)
    area.pack_forget()
    area.pack()


def load_chapter(number):
    global data, part

    label.config(text='Chapter ' + str(number))
    part = 0
    file = open('chapters/chapter' + str(number) + '/chapter' + str(number) + '.txt', 'r')
    data = file.read().split('\n')
    file.close()
    prev.config(state='disabled', cursor='iron_cross')

    load_part()


def load_quiz():
    global answers, questions, questionIndex

    label.config(text='Quiz ' + str(chapter))

    area.pack_forget()
    text.pack_forget()

    for child in item_frame.winfo_children():
        child.destroy()

    questionIndex = 0
    file = open('chapters/chapter' + str(chapter) + '/questions.txt', 'r')
    questions = file.read().split('\n')
    file.close()

    file = open('chapters/chapter' + str(chapter) + '/answers.txt', 'r')
    answers = file.read().split('\n')
    file.close()

    load_question()


def load_results():
    quiz.destroy()

    Label(root, text='Score: ' + str(score)).pack()
    Label(root, text='Wrong Answers: ' + str(wrongAnswerCount)).pack()
    Label(root, text='Right Answers: ' + str(rightAnswerCount)).pack()


def select(alternative):
    global questionIndex, chapter
    global score, rightAnswerCount, wrongAnswerCount
    global item_usage

    if alternative == answers[questionIndex]:
        score += 100
        rightAnswerCount += 1
    else:
        if current_item == items['item_three']:
            score -= 70
        elif current_item == items['item_one'] and item_usage == 0:
            item_usage += 1
        else:
            score -= 100
        wrongAnswerCount += 1

    if questionIndex == len(questions) - 1:
        if chapter == 3:
            load_results()
        else:
            chapter += 1
            load_chapter(chapter)
    else:
        questionIndex += 1
        load_question()


def load_question():
    global questionIndex
    quiz.pack_forget()
    for child in quiz.winfo_children():
        child.destroy()

    question = Label(quiz, text=questions[questionIndex])
    question.pack()

    number = str(questionIndex + 1)
    file = open('chapters/chapter' + str(chapter) + '/alternatives_' + number + '.txt', 'r')
    alternatives = file.read().split('\n')
    file.close()

    area_a = Frame(quiz, height=1.5, width=8)
    option_a_select = Button(area_a, text='A', command=lambda: select('A'))
    option_a = Label(area_a, text=alternatives[0])
    option_a_select.pack(side=LEFT)
    option_a.pack(side=RIGHT)
    area_a.pack()

    area_b = Frame(quiz, height=1.5, width=8)
    option_b_select = Button(area_b, text='B', command=lambda: select('B'))
    option_b = Label(area_b, text=alternatives[1])
    option_b_select.pack(side=LEFT)
    option_b.pack(side=RIGHT)
    area_b.pack()

    area_c = Frame(quiz, height=1.5, width=8)
    option_c_select = Button(area_c, text='C', command=lambda: select('C'))
    option_c = Label(area_c, text=alternatives[2])
    option_c_select.pack(side=LEFT)
    option_c.pack(side=RIGHT)
    area_c.pack()

    area_d = Frame(quiz, height=1.5, width=8)
    option_d_select = Button(area_d, text='D', command=lambda: select('D'))
    option_d = Label(area_d, text=alternatives[3])
    option_d_select.pack(side=LEFT)
    option_d.pack(side=RIGHT)
    area_d.pack()

    quiz.pack()


def select_item(key):
    global current_item, item_usage, score
    current_item = items[key]
    item_usage = 0
    if current_item == items['item_two']:
        score += 100
    load_quiz()


def load_item_pool():
    label.config(text='Select an item')

    for key in items:
        Button(item_frame, text=items[key], command=lambda: select_item(key)).pack()

    area.pack_forget()
    text.pack_forget()
    text.configure(state='normal')
    text.delete(1.0, END)
    text.insert(END, '')
    text.configure(state='disabled')


def navigate_next():
    global part

    if part == len(data) - 1:
        load_item_pool()
    else:
        part += 1
        load_part()
        prev.config(state='normal', cursor='hand1')


def navigate_back():
    global part

    if part > 0:
        if part == 1:
            prev.config(state='disabled', cursor='iron_cross')
        part -= 1
        load_part()


next = Button(
    area,
    text='Next Page',
    image=photoNext,
    cursor='hand1',
    highlightthickness=0,
    bd=0,
    command=navigate_next
)

prev = Button(
    area,
    text='Previous Page',
    image=photoPrev,
    cursor='hand1',
    highlightthickness=0,
    bd=0,
    command=navigate_back
)

next.pack(side=RIGHT)
prev.pack(side=LEFT)
area.pack()


def go_left(event):
    if text.compare("end-1c", "!=", "1.0"):
        navigate_back()


def go_right(event):
    if text.compare("end-1c", "!=", "1.0"):
        navigate_next()


root.bind('<Left>', go_left)
root.bind('<Right>', go_right)

load_chapter(1)

root.mainloop()
