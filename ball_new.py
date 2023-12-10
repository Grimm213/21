from tkinter import *
import time
import random

class Ball():

    def __init__(self, canvas, platform, color):
        self.canvas = canvas
        self.platform = platform
        self.oval = canvas.create_oval(200, 200, 215, 215, fill=color)
        self.dir = [-3, -2, -1, 1, 2, 3]
        self.x = random.choice(self.dir)
        self.y = -1
        self.touch_bottom = False
        self.score = 0
        self.score_text = self.canvas.create_text(250, 20, text=f"Счет: {self.score}", font=("Arial", 16))

    def touch_platform(self, ball_pos):
        platform_pos = self.canvas.coords(self.platform.rect)
        if ball_pos[2] >= platform_pos[0] and ball_pos[0] <= platform_pos[2]:
            if ball_pos[3] >= platform_pos[1] and ball_pos[3] <= platform_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.oval, self.x, self.y)
        pos = self.canvas.coords(self.oval)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= 400:
            self.touch_bottom = True
            self.canvas.create_text(250, 200, text=f"Финальный счет: {self.score}", font=("Arial", 16))
            self.canvas.create_text(250, 225, text="Нажмите 'q' для выхода в меню", font=("Arial", 16))
            self.canvas.bind_all('<KeyPress-q>', self.quit)
        if self.touch_platform(pos) == True:
            self.y = -3
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Счет: {self.score}")
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= 500:
            self.x = -3

    def quit(self, event):
        global window
        window.destroy()
        main_menu()

class Platform():

    def __init__(self, canvas, color):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(230, 300, 330, 310, fill=color)
        self.x = 0
        self.canvas.bind_all('<KeyPress-Left>', self.left)
        self.canvas.bind_all('<KeyPress-Right>', self.right)

    def left(self, event):
        self.x = -2

    def right(self, event):
        self.x = 2

    def draw(self):
        self.canvas.move(self.rect, self.x, 0)
        pos = self.canvas.coords(self.rect)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= 500:
            self.x = 0

def start_game(event):
    global ball, platform, canvas, window
    window.destroy()
    window = Tk()
    window.title("Аркада")
    window.resizable(0, 0)
    window.wm_attributes("-topmost", 1)
    canvas = Canvas(window, width=500, height=400, bg='sky blue')
    canvas.pack()
    platform = Platform(canvas, 'green')
    ball = Ball(canvas, platform, 'red')
    while True:
        if ball.touch_bottom == False:
            ball.draw()
            platform.draw()
        window.update()
        time.sleep(0.01)

def exit_game(event):
    global window
    window.destroy()

def main_menu():
    global window
    window = Tk()
    window.title("Меню")
    window.geometry("500x400") 
    window.resizable(0, 0)
    window.wm_attributes("-topmost", 1)
    start_button = Button(window, text="Играть", font=("Arial", 20), width=20, height=2, bg='yellow')
    start_button.bind("<Button-1>", start_game)
    start_button.pack(pady=50)  # добавлен отступ
    exit_button = Button(window, text="Выход", font=("Arial", 20), width=20, height=2, bg='yellow')
    exit_button.bind("<Button-1>", exit_game)
    exit_button.pack(pady=50)  # добавлен отступ
    window.mainloop()

main_menu()
