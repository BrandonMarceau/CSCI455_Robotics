import tkinter as tk
from tkinter import *
from abc import ABC, abstractmethod
import time
from controller import Control

cntrl = Control()

class AnimeWindow():
    win = None
    myCan = None

    wink_eyes = None
    open_eyes = None
    
    def init(self):
        self.win = Toplevel()
        self.win.geometry("800x480")
        self.myCan = tk.Canvas(self.win, bg="red", width="800", height="480")
        self.win.attributes("-fullscreen", True)
        open_eyes = PhotoImage(file='eyes_open.png');
        open_id = self.myCan.create_image(0, 0, image=open_eyes, anchor="nw")
        self.open_eyes = open_eyes
        self.myCan.pack()
        self.win.update()


    def close(self):
        self.win.destroy()


    def wink(self):
        wink_eyes = PhotoImage(file='eyes_wink.png');
        wink_id = self.myCan.create_image(0, 0, image=wink_eyes, anchor="nw")
        self.wink_eyes = wink_eyes
        self.myCan.pack()
        self.win.update()
        time.sleep(1)
        self.myCan.delete(wink_id)
        self.myCan.pack()
        self.win.update()

class Action(ABC):

    @abstractmethod
    def edit(self):
        pass

    @abstractmethod
    def render(self, y, c):
        pass

    @abstractmethod
    def run(self):
        pass


class RobotForwardOrBack(Action):

    y = None
    speed = None
    direction = None
    time = None
    ids = None
    widgets = None

    edit_win = None
    edit_can = None

    fwd_dir_btn = None
    bck_dir_btn = None

    speed_slider = None
    time_slider = None

    def __init__(self):
        self.ids = []
        self.widgets = []
        self.direction = 'f'
        self.speed = 2
        self.time = 3

    def assn_fwd(self):
        self.direction = "f"
        self.bck_dir_btn.place(relx=0.5, y=50, anchor='center')
        self.fwd_dir_btn.place_forget()

    def assn_bck(self):
        self.direction = "b"
        self.fwd_dir_btn.place(relx=0.5, y=50, anchor='center')
        self.bck_dir_btn.place_forget()

    def handle_done_btn(self):
        self.speed = self.speed_slider.get()
        self.time = self.time_slider.get()
        self.edit_win.destroy()

    def build_edit(self):
        self.edit_can.create_text(400, 12, text="Robot Direction", font=("Helvetica", 12), fill='black')
        self.fwd_dir_btn = Button(self.edit_win, text="Go Forward", width=50, height=2, bd='1', command=self.assn_fwd)
        self.bck_dir_btn = Button(self.edit_win, text="Go Backwards", width=50, height=2, bd='1', command=self.assn_bck)
        if self.direction == 'b':
            self.fwd_dir_btn.place(relx=0.5, y=50, anchor='center')
        else:
            self.bck_dir_btn.place(relx=0.5, y=50, anchor='center')

        self.edit_can.create_text(400, 90, text="Robot Speed", font=("Helvetica", 12), fill='black')
        self.speed_slider = Scale(self.edit_win, from_=0, to=10, tickinterval=1, orient="horizontal", bg="pink", length="275")
        self.speed_slider.set(self.speed)
        self.speed_slider.place(relx=0.5, y=130, anchor='center')

        self.edit_can.create_text(400, 180, text="Time (secs)", font=("Helvetica", 12), fill='black')
        self.time_slider = Scale(self.edit_win, from_=0, to=10, tickinterval=1, orient="horizontal", bg="pink", length="275")
        self.time_slider.set(self.time)
        self.time_slider.place(relx=0.5, y=220, anchor='center')

        Button(self.edit_win, text="Done", width=50, height=2, bd='1', command=self.handle_done_btn).place(relx=0.5, y=350, anchor='center')


    # implementation
    def edit(self, *args):
        print(self)
        self.edit_win = Tk()
        self.edit_win.geometry("800x480")
        self.edit_can = tk.Canvas(self.edit_win, bg="pink", width="800", height="480")
        self.edit_win.attributes("-fullscreen", True)
        self.build_edit()
        self.edit_can.pack()
        self.edit_win.mainloop()

    # implementation
    def render(self, y, canvas, win):
        self.y = y
        self.ids.append(canvas.create_rectangle(220, y, 700, y+43, fill="#f2f7f4", outline="black"))
        self.ids.append(canvas.create_text(460, y+21, text="Robot Forward or Back", font=("Helvetica", 16), fill='black', tags="click"))
        btn = Button(win, text="Edit", width=4, height=1, bd='1', command=self.edit)
        btn.place(x=630, y=y+7)
        self.widgets.append(btn)
        # canvas.tag_bind(str(y), "<Button-1>", self.edit)
        canvas.pack()

    # implementation
    def run(self):
        if self.direction == 'f':
            print('calling forward()')
            cntrl.forward(self.speed, self.time)
        else:
            cntrl.backward(self.speed, self.time)

class RobotTurnLeft(Action):
    y = None
    time = None
    ids = None
    widgets = None

    edit_win = None
    edit_can = None

    time_slider = None

    def __init__(self):
        self.ids = []
        self.widgets = []
        self.time = 3

    def handle_done_btn(self):
        self.time = self.time_slider.get()
        self.edit_win.destroy()

    def build_edit(self):

        self.edit_can.create_text(400, 30, text="Time (secs)", font=("Helvetica", 12), fill='black')
        self.time_slider = Scale(self.edit_win, from_=0, to=10, tickinterval=1, orient="horizontal", bg="pink", length="275")
        self.time_slider.set(self.time)
        self.time_slider.place(relx=0.5, y=130, anchor='center')

        Button(self.edit_win, text="Done", width=50, height=2, bd='1', command=self.handle_done_btn).place(relx=0.5, y=350, anchor='center')


    # implementation
    def edit(self, *args):
        print(self)
        self.edit_win = Tk()
        self.edit_win.geometry("800x480")
        self.edit_can = tk.Canvas(self.edit_win, bg="pink", width="800", height="480")
        self.edit_win.attributes("-fullscreen", True)
        self.build_edit()
        self.edit_can.pack()
        self.edit_win.mainloop()

    # implementation
    def render(self, y, canvas, win):
        self.root_win = win
        self.root_canvas = canvas
        
        self.y = y
        self.ids.append(canvas.create_rectangle(220, y, 700, y+43, fill="#f2f7f4", outline="black"))
        self.ids.append(canvas.create_text(460, y+21, text="Robot turn left", font=("Helvetica", 16), fill='black', tags="click"))
        btn = Button(win, text="Edit", width=4, height=1, bd='1', command=self.edit)
        btn.place(x=630, y=y+7)
        self.widgets.append(btn)
        # canvas.tag_bind(str(y), "<Button-1>", self.edit)
        canvas.pack()

    # implementation
    def run(self):
        print('calling turn left')
        cntrl.left(self.time)


class RobotTurnRight(Action):
    y = None
    time = None
    ids = None
    widgets = None

    edit_win = None
    edit_can = None

    time_slider = None

    def __init__(self):
        self.ids = []
        self.widgets = []
        self.time = 3

    def handle_done_btn(self):
        self.time = self.time_slider.get()
        self.edit_win.destroy()

    def build_edit(self):

        self.edit_can.create_text(400, 30, text="Time (secs)", font=("Helvetica", 12), fill='black')
        self.time_slider = Scale(self.edit_win, from_=0, to=10, tickinterval=1, orient="horizontal", bg="pink", length="275")
        self.time_slider.set(self.time)
        self.time_slider.place(relx=0.5, y=130, anchor='center')

        Button(self.edit_win, text="Done", width=50, height=2, bd='1', command=self.handle_done_btn).place(relx=0.5, y=350, anchor='center')


    # implementation
    def edit(self, *args):
        print(self)
        self.edit_win = Tk()
        self.edit_win.geometry("800x480")
        self.edit_can = tk.Canvas(self.edit_win, bg="pink", width="800", height="480")
        self.edit_win.attributes("-fullscreen", True)
        self.build_edit()
        self.edit_can.pack()
        self.edit_win.mainloop()

    # implementation
    def render(self, y, canvas, win):
        self.y = y
        self.ids.append(canvas.create_rectangle(220, y, 700, y+43, fill="#f2f7f4", outline="black"))
        self.ids.append(canvas.create_text(460, y+21, text="Robot turn right", font=("Helvetica", 16), fill='black', tags="click"))
        btn = Button(win, text="Edit", width=4, height=1, bd='1', command=self.edit)
        btn.place(x=630, y=y+7)
        self.widgets.append(btn)
        # canvas.tag_bind(str(y), "<Button-1>", self.edit)
        canvas.pack()

    # implementation
    def run(self):
        print('calling turn right')
        cntrl.right(self.time)


class HeadLeftOrRight(Action):

    y = None
    speed = None
    direction = None
    degrees = None
    time = None
    ids = None
    widgets = None

    edit_win = None
    edit_can = None

    fwd_dir_btn = None
    bck_dir_btn = None

    speed_slider = None
    time_slider = None
    degrees_slider = None

    def __init__(self):
        self.ids = []
        self.widgets = []
        self.direction = 'l'
        self.speed = 0
        self.time = 0
        self.degrees = 0

    def assn_right(self):
        self.direction = "r"
        self.left_btn.place(relx=0.5, y=50, anchor='center')
        self.right_btn.place_forget()

    def assn_left(self):
        self.direction = "l"
        self.right_btn.place(relx=0.5, y=50, anchor='center')
        self.left_btn.place_forget()

    def handle_done_btn(self):
        self.degrees = self.degrees_slider.get()
        self.edit_win.destroy()

    def build_edit(self):
        self.edit_can.create_text(400, 12, text="Head Direction", font=("Helvetica", 12), fill='black')
        self.right_btn = Button(self.edit_win, text="Right", width=50, height=2, bd='1', command=self.assn_right)
        self.left_btn = Button(self.edit_win, text="Left", width=50, height=2, bd='1', command=self.assn_left)
        if self.direction == 'l':
            self.right_btn.place(relx=0.5, y=50, anchor='center')
        else:
            self.left_btn.place(relx=0.5, y=50, anchor='center')

        self.edit_can.create_text(400, 90, text="Degrees", font=("Helvetica", 12), fill='black')
        self.degrees_slider = Scale(self.edit_win, from_=5, to=50, tickinterval=5, orient="horizontal", bg="pink", length="275")
        self.degrees_slider.set(self.degrees)
        self.degrees_slider.place(relx=0.5, y=130, anchor='center')

        Button(self.edit_win, text="Done", width=50, height=2, bd='1', command=self.handle_done_btn).place(relx=0.5, y=350, anchor='center')


    # implementation
    def edit(self, *args):
        print(self)
        self.edit_win = Tk()
        self.edit_win.geometry("800x480")
        self.edit_can = tk.Canvas(self.edit_win, bg="pink", width="800", height="480")
        self.edit_win.attributes("-fullscreen", True)
        self.build_edit()
        self.edit_can.pack()
        self.edit_win.mainloop()

    # implementation
    def render(self, y, canvas, win):
        self.y = y
        self.ids.append(canvas.create_rectangle(220, y, 700, y+43, fill="#f2f7f4", outline="black"))
        self.ids.append(canvas.create_text(460, y+21, text="Head Left or Right", font=("Helvetica", 16), fill='black', tags="click"))
        btn = Button(win, text="Edit", width=4, height=1, bd='1', command=self.edit)
        btn.place(x=630, y=y+7)
        self.widgets.append(btn)
        # canvas.tag_bind(str(y), "<Button-1>", self.edit)
        canvas.pack()

    # implementation
    def run(self):
        print('calling head turn')
        if self.direction=='l':
            cntrl.headLeft(self.degrees)
        else:
            cntrl.headRight(self.degrees)


class HeadUpOrDown(Action):

    y = None
    speed = None
    direction = None
    degrees = None
    time = None
    ids = None
    widgets = None

    edit_win = None
    edit_can = None

    fwd_dir_btn = None
    bck_dir_btn = None

    speed_slider = None
    time_slider = None
    degrees_slider = None

    def __init__(self):
        self.ids = []
        self.widgets = []
        self.direction = 'u'
        self.speed = 0
        self.time = 0
        self.degrees = 0

    def assn_up(self):
        self.direction = "u"
        self.down_btn.place(relx=0.5, y=50, anchor='center')
        self.up_btn.place_forget()

    def assn_down(self):
        self.direction = "d"
        self.up_btn.place(relx=0.5, y=50, anchor='center')
        self.down_btn.place_forget()

    def handle_done_btn(self):
        self.degrees = self.degrees_slider.get()
        self.edit_win.destroy()

    def build_edit(self):
        self.edit_can.create_text(400, 12, text="Head Tilt (Up/Down)", font=("Helvetica", 12), fill='black')
        self.up_btn = Button(self.edit_win, text="Up", width=50, height=2, bd='1', command=self.assn_up)
        self.down_btn = Button(self.edit_win, text="Down", width=50, height=2, bd='1', command=self.assn_down)
        if self.direction == 'u':
            self.up_btn.place(relx=0.5, y=50, anchor='center')
        else:
            self.down_btn.place(relx=0.5, y=50, anchor='center')

        self.edit_can.create_text(400, 90, text="Degrees", font=("Helvetica", 12), fill='black')
        self.degrees_slider = Scale(self.edit_win, from_=5, to=50, tickinterval=5, orient="horizontal", bg="pink", length="275")
        self.degrees_slider.set(self.degrees)
        self.degrees_slider.place(relx=0.5, y=130, anchor='center')

        Button(self.edit_win, text="Done", width=50, height=2, bd='1', command=self.handle_done_btn).place(relx=0.5, y=350, anchor='center')


    # implementation
    def edit(self, *args):
        print(self)
        self.edit_win = Tk()
        self.edit_win.geometry("800x480")
        self.edit_can = tk.Canvas(self.edit_win, bg="pink", width="800", height="480")
        self.edit_win.attributes("-fullscreen", True)
        self.build_edit()
        self.edit_can.pack()
        self.edit_win.mainloop()

    # implementation
    def render(self, y, canvas, win):
        self.y = y
        self.ids.append(canvas.create_rectangle(220, y, 700, y+43, fill="#f2f7f4", outline="black"))
        self.ids.append(canvas.create_text(460, y+21, text="Head Up or Down", font=("Helvetica", 16), fill='black', tags="click"))
        btn = Button(win, text="Edit", width=4, height=1, bd='1', command=self.edit)
        btn.place(x=630, y=y+7)
        self.widgets.append(btn)
        # canvas.tag_bind(str(y), "<Button-1>", self.edit)
        canvas.pack()

    # implementation
    def run(self):
        print('calling head tilt')
        if self.direction=='u':
            cntrl.headUp(self.degrees)
        else:
            cntrl.headDown(self.degrees)


class WaistLeftOrRight(Action):

    y = None
    speed = None
    direction = None
    deg = None
    ids = None
    widgets = None

    edit_win = None
    edit_can = None

    left_dir_btn = None
    right_dir_btn = None

    deg_slider = None

    def __init__(self):
        self.ids = []
        self.widgets = []
        self.direction = 'r'
        self.deg = 10

    def assn_left(self):
        self.direction = "l"
        self.right_dir_btn.place(relx=0.5, y=50, anchor='center')
        self.left_dir_btn.place_forget()

    def assn_right(self):
        self.direction = "r"
        self.left_dir_btn.place(relx=0.5, y=50, anchor='center')
        self.right_dir_btn.place_forget()

    def handle_done_btn(self):
        self.deg = self.deg_slider.get()
        self.edit_win.destroy()

    def build_edit(self):
        self.edit_can.create_text(400, 12, text="Robot Direction", font=("Helvetica", 12), fill='black')
        self.left_dir_btn = Button(self.edit_win, text="Go Left", width=50, height=2, bd='1', command=self.assn_left)
        self.right_dir_btn = Button(self.edit_win, text="Go Right", width=50, height=2, bd='1', command=self.assn_right)
        if self.direction == 'r':
            self.left_dir_btn.place(relx=0.5, y=50, anchor='center')
        else:
            self.right_dir_btn.place(relx=0.5, y=50, anchor='center')

        self.edit_can.create_text(400, 90, text="Movement in degrees", font=("Helvetica", 12), fill='black')
        self.deg_slider = Scale(self.edit_win, from_=0, to=55, tickinterval=5, orient="horizontal", bg="pink", length="275")
        self.deg_slider.set(self.deg)
        self.deg_slider.place(relx=0.5, y=130, anchor='center')

        Button(self.edit_win, text="Done", width=50, height=2, bd='1', command=self.handle_done_btn).place(relx=0.5, y=350, anchor='center')


    # implementation
    def edit(self, *args):
        print(self)
        self.edit_win = Tk()
        self.edit_win.geometry("800x480")
        self.edit_can = tk.Canvas(self.edit_win, bg="pink", width="800", height="480")
        self.edit_win.attributes("-fullscreen", True)
        self.build_edit()
        self.edit_can.pack()
        self.edit_win.mainloop()

    # implementation
    def render(self, y, canvas, win):
        self.y = y
        self.ids.append(canvas.create_rectangle(220, y, 700, y+43, fill="#f2f7f4", outline="black"))
        self.ids.append(canvas.create_text(460, y+21, text="Waist Left or Right", font=("Helvetica", 16), fill='black', tags="click"))
        btn = Button(win, text="Edit", width=4, height=1, bd='1', command=self.edit)
        btn.place(x=630, y=y+7)
        self.widgets.append(btn)
        # canvas.tag_bind(str(y), "<Button-1>", self.edit)
        canvas.pack()

    # implementation
    def run(self):
        print('calling waist turn')
        if self.direction=='l':
            cntrl.waistLeft(self.deg)
        else:
            cntrl.waistRight(self.deg)


class Wait(Action):

    y = None
    pass_phrase = None
    mode = None
    time = None
    ids = None
    widgets = None

    edit_win = None
    edit_can = None

    phrase_btn = None
    time_btn = None

    time_slider = None
    time_text_id = None
    phrase_text_id = None
    phrase_text_box = None

    def __init__(self):
        self.ids = []
        self.widgets = []
        self.mode = 'p'
        self.pass_phrase = 'Hello'
        self.time = 5

    def use_phrase(self):
        self.mode = "p"
        self.time_btn.place(relx=0.5, y=80, anchor='center')
        self.phrase_text_id = self.edit_can.create_text(400, 150, text='Listening for the phrase: ', font=("Helvetica", 12),fill='black')
        self.phrase_text_box.place(relx=0.5, y=200, anchor='center')
        self.edit_can.delete(self.time_text_id)
        self.time_slider.place_forget()
        self.phrase_btn.place_forget()

    def use_time(self):
        self.mode = "t"
        self.phrase_btn.place(relx=0.5, y=80, anchor='center')
        self.time_text_id = self.edit_can.create_text(400, 130, text="Wait Duration (seconds)", font=("Helvetica", 12),
                                                      fill='black')
        self.edit_can.delete(self.phrase_text_id)
        self.phrase_text_box.place_forget()
        self.time_slider.place(relx=0.5, y=200, anchor='center')
        self.time_btn.place_forget()

    def handle_done_btn(self):
        self.time = self.time_slider.get()
        self.pass_phrase = self.phrase_text_box.get("1.0", "end-1c")
        self.edit_win.destroy()

    def build_edit(self):
        self.edit_can.create_text(400, 12, text="Wait for trigger phrase or specified amount of time", font=("Helvetica", 12), fill='black')
        self.phrase_btn = Button(self.edit_win, text="Wait for Trigger Phrase", width=50, height=2, bd='1', command=self.use_phrase)
        self.time_btn = Button(self.edit_win, text="Wait for Time", width=50, height=2, bd='1', command=self.use_time)
        if self.mode == 't':
            self.phrase_btn.place(relx=0.5, y=130, anchor='center')
        else:
            self.time_btn.place(relx=0.5, y=130, anchor='center')

        self.phrase_text_id = self.edit_can.create_text(400, 180, text='Listening for the phrase: ', font=("Helvetica", 12), fill='black')
        self.phrase_text_box = Text(self.edit_win, height=2, width=35, bg="white")
        self.phrase_text_box.insert(END, self.pass_phrase)
        self.phrase_text_box.place(relx=0.5, y=220, anchor='center')

        self.time_slider = Scale(self.edit_win, from_=0, to=10, orient="horizontal", bg="pink", length="275")
        self.time_slider.set(self.time)
        if self.mode == 't':
            self.time_slider.place(relx=0.5, y=250, anchor='center')

        Button(self.edit_win, text="Done", width=50, height=2, bd='1', command=self.handle_done_btn).place(relx=0.5, y=350, anchor='center')


    # implementation
    def edit(self, *args):
        print(self)
        self.edit_win = Tk()
        self.edit_win.geometry("800x480")
        self.edit_can = tk.Canvas(self.edit_win, bg="pink", width="800", height="480")
        self.edit_win.attributes("-fullscreen", True)
        self.build_edit()
        self.edit_can.pack()
        self.edit_win.mainloop()

    # implementation
    def render(self, y, canvas, win):
        self.y = y
        self.ids.append(canvas.create_rectangle(220, y, 700, y+43, fill="#f2f7f4", outline="black"))
        self.ids.append(canvas.create_text(460, y+21, text="Wait", font=("Helvetica", 16), fill='black', tags="click"))
        btn = Button(win, text="Edit", width=4, height=1, bd='1', command=self.edit)
        btn.place(x=630, y=y+7)
        self.widgets.append(btn)
        # canvas.tag_bind(str(y), "<Button-1>", self.edit)
        canvas.pack()

    # implementation
    def run(self):
        if self.mode=='t':
            print('waiting for ' + str(self.time) + 'seconds')
            cntrl.waitWithSeconds(self.time)
        else:
            print('waiting for user to say: ' + str(self.pass_phrase))
            cntrl.waitWithSpeech(self.pass_phrase)


class Talk(Action):

    y = None
    text_to_speak = None
    ids = None
    widgets = None

    edit_win = None
    edit_can = None


    input_box = None

    def __init__(self):
        self.ids = []
        self.widgets = []
        self.text_to_speak = 'I smell like beef'

    def handle_done_btn(self):
        self.text_to_speak = self.input_box.get("1.0", "end-1c")
        self.edit_win.destroy()

    def build_edit(self):
        self.edit_can.create_text(400, 90, text='Listening for the phrase: ', font=("Helvetica", 12), fill='black')
        self.input_box = Text(self.edit_win, height=2, width=35, bg="white")
        self.input_box.insert(END, self.text_to_speak)
        self.input_box.place(relx=0.5, y=130, anchor='center')

        Button(self.edit_win, text="Done", width=50, height=2, bd='1', command=self.handle_done_btn).place(relx=0.5, y=350, anchor='center')


    # implementation
    def edit(self, *args):
        print(self)
        self.edit_win = Tk()
        self.edit_win.geometry("800x480")
        self.edit_can = tk.Canvas(self.edit_win, bg="pink", width="800", height="480")
        self.edit_win.attributes("-fullscreen", True)
        self.build_edit()
        self.edit_can.pack()
        self.edit_win.mainloop()

    # implementation
    def render(self, y, canvas, win):
        self.y = y
        self.ids.append(canvas.create_rectangle(220, y, 700, y+43, fill="#f2f7f4", outline="black"))
        self.ids.append(canvas.create_text(460, y+21, text="Talk", font=("Helvetica", 16), fill='black', tags="click"))
        btn = Button(win, text="Edit", width=4, height=1, bd='1', command=self.edit)
        btn.place(x=630, y=y+7)
        self.widgets.append(btn)
        # canvas.tag_bind(str(y), "<Button-1>", self.edit)
        canvas.pack()

    # implementation
    def run(self):
        print('calling talk method to say: ' + str(self.text_to_speak))
        cntrl.say(self.text_to_speak)


class Window:
    def __init__(self, win):
        self.win = win
        self.win.geometry("800x480")
        self.myCan = tk.Canvas(self.win, bg="light blue", width="800", height="480")
        self.win.attributes("-fullscreen", True)
        self.run_list = []
        self.render_y = 50

    def create_buttons(self):
        self.fwd_button()
        self.left_button()
        self.right_button()
        self.head_turn_button()
        self.head_tilt_button()
        self.waist_button()
        self.wait_button()
        self.talk_button()
        self.clear_button()
        self.run_button()
        self.exit_button()

    def make_new_direction(self):
        direction = self.myCan.create_rectangle(250, 50, 400, 80, fill="green")
        self.myCan.pack()


    def fwd_button(self):
        #self.myCan.create_oval(255, 180, 310, 270, fil="black")
        #self.myCan.pack()

        #buttonBG = self.myCan.create_rectangle(0, 0, 50, 50, fill="red", outline="grey60")

        forwardBack_image = tk.PhotoImage(file = "fowardBack.png")
        fwd_button = Button (self.win, width = 50, height = 50, image = forwardBack_image,  bd='5', command = self.handle_back_btn)
        fwd_button.image = forwardBack_image
        fwd_button.place(x = 50, y = 50)
        self.myCan.pack()

    def talk_button(self):
        talk_image = tk.PhotoImage(file = "talk.png")
        talk_button = Button(self.win, width = 50, height = 50, image = talk_image, bd='5', command = self.handle_talk_btn)
        talk_button.image = talk_image
        talk_button.place(x = 120, y = 50)
        self.myCan.pack()

    def left_button(self):
        left_image = tk.PhotoImage(file = "left.png")
        left_button = Button(self.win, width = 50, height = 50, image = left_image,  bd='5', command=self.handle_turn_left_btn)
        left_button.image = left_image
        left_button.place(x = 50, y = 120)
        self.myCan.pack()

    def right_button(self):
        right_image = tk.PhotoImage(file = "right.png")
        right_button = Button(self.win, width = 50, height = 50, image = right_image, bd='5', command=self.handle_turn_right_btn)
        right_button.image = right_image
        right_button.place(x = 120, y = 120)
        self.myCan.pack()

    def head_turn_button(self):
        head_turn_image = tk.PhotoImage(file = "headTurn.png")
        head_turn_button = Button(self.win, width = 50, height = 50, image = head_turn_image, bd='5', command=self.handle_head_turn_btn)
        head_turn_button.image = head_turn_image
        head_turn_button.place(x = 50, y = 190)
        self.myCan.pack()

    def head_tilt_button(self):
        head_tilt_image = tk.PhotoImage(file = "headTilt.png")
        head_tilt_button = Button(self.win, width = 50, height = 50, image = head_tilt_image, bd='5', command=self.handle_head_tilt_btn)
        head_tilt_button.image = head_tilt_image
        head_tilt_button.place(x = 120, y = 190)
        self.myCan.pack()

    def waist_button(self):
        body_image = tk.PhotoImage(file = "waist.png")
        waist_button = Button(self.win, width = 50, height = 50, image = body_image, bd='5', command=self.handle_waist_btn)
        waist_button.image = body_image
        waist_button.place(x = 50, y = 260)
        self.myCan.pack()

    def wait_button(self):
        wait_image = tk.PhotoImage(file = "wait.png")
        wait_button = Button(self.win, width = 50, height = 50, image = wait_image, bd='5', command=self.handle_wait_btn)
        wait_button.image = wait_image
        wait_button.place(x = 120, y = 260)
        self.myCan.pack()

    def run_button(self):
        run_button = Button(self.win, text="Run", width = 15, height = 2, bd='5', bg = "green", command=self.handle_run_btn)
        run_button.place(x = 50, y = 330)
        self.myCan.pack()

    def clear_button(self):
        clear_button = Button(self.win, text="Clear", width = 15, height = 2, bd='5', bg = "red", command=self.handle_clear_btn)
        clear_button.place(x = 50, y = 400)
        self.myCan.pack()

    def exit_button(self):
        exit_button = Button(self.win, text="X", width=1, height=1, bd='5', bg='red', command=self.handle_exit_btn)
        exit_button.place(x = 780, y=0, anchor='ne')
        self.myCan.pack()

    def handle_back_btn(self):
        if len(self.run_list) < 8:
            action_instance = RobotForwardOrBack()
            self.run_list.append(action_instance)

            action_instance.render(self.render_y, self.myCan, self.win)

            self.render_y += 52

    def handle_turn_left_btn(self):
        if len(self.run_list) < 8:
            action_instance = RobotTurnLeft()
            self.run_list.append(action_instance)

            action_instance.render(self.render_y, self.myCan, self.win)

            self.render_y += 52

    def handle_turn_right_btn(self):
        if len(self.run_list) < 8:
            action_instance = RobotTurnRight()
            self.run_list.append(action_instance)

            action_instance.render(self.render_y, self.myCan, self.win)

            self.render_y += 52

    def handle_head_turn_btn(self):
        if len(self.run_list) < 8:
            action_instance = HeadLeftOrRight()
            self.run_list.append(action_instance)
            action_instance.render(self.render_y, self.myCan, self.win)
            self.render_y += 52

    def handle_head_tilt_btn(self):
        if len(self.run_list) < 8:
            action_instance = HeadUpOrDown()
            self.run_list.append(action_instance)
            action_instance.render(self.render_y, self.myCan, self.win)
            self.render_y += 52

    def handle_waist_btn(self):
        if len(self.run_list) < 8:
            action_instance = WaistLeftOrRight()
            self.run_list.append(action_instance)

            action_instance.render(self.render_y, self.myCan, self.win)

            self.render_y += 52

    def handle_wait_btn(self):
        if len(self.run_list) < 8:
            action_instance = Wait()
            self.run_list.append(action_instance)

            action_instance.render(self.render_y, self.myCan, self.win)

            self.render_y += 52

    def handle_talk_btn(self):
        if len(self.run_list) < 8:
            action_instance = Talk()
            self.run_list.append(action_instance)

            action_instance.render(self.render_y, self.myCan, self.win)

            self.render_y += 52

    def handle_clear_btn(self):
        for a in self.run_list:
            for i in a.ids:
                self.myCan.delete(i)
            for w in a.widgets:
                w.destroy()
            del a

        self.run_list = []
        self.render_y = 50
        pass#.reset()

    def handle_run_btn(self):
##        for a in self.run_list:
##            green = self.myCan.create_rectangle(220, a.y, 290, a.y+43, fill="green", outline="black")
##            self.myCan.update_idletasks()
##            a.run()
##            self.myCan.delete(green)

        an_win = AnimeWindow()
        self.win.update_idletasks()
        for a in self.run_list:
            a.run()
            an_win.wink()
        an_win.close()
            

    def handle_exit_btn(self):
        self.win.destroy()


        
    


def main():
    win = Tk()
    w = Window(win)
    w.create_buttons()
    win.mainloop()


main()
