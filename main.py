import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk

class Game:
    def run(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def description(self):
        raise NotImplementedError("Subclass must implement abstract method")

class BallNew(Game):
    def run(self):
        subprocess.Popen(["python", "ball_new.py"])

    def description(self):
        return "В этой игре необходимо отбивать мячик и набивать счётчик."

class Snake(Game):
    def run(self):
        subprocess.Popen(["python", "snake.py"])

    def description(self):
        return "Вы играете за змейку, пожирайте яблоки и становитесь больше."

class Navigator():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1000x800')
        self.root.title("Game Launcher")
        self.games = {"1": BallNew(), "2": Snake()}
        self.selected_game = self.games["1"]
        self.create_widgets()

    def create_widgets(self):
        image = Image.open("background.png")
        image = image.resize((1000, 800), Image.BICUBIC)
        self.photo = ImageTk.PhotoImage(image)

        self.background_label = tk.Label(self.root, image=self.photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.root, text="Добро пожаловать в мир игр", font=('Arial', 30), fg='white', bg='royal blue').grid(row=0, column=0, pady=100, padx=200)

        for i, (game_name, game) in enumerate(self.games.items()):
            button = tk.Button(self.root, text=game_name, bg='royal blue', fg='white', width=20, height=4, command=lambda game=game: self.select_game(game), highlightthickness=0, borderwidth=0)
            button.grid(row=i+1, column=0, pady=2)

        self.description_text = tk.Text(self.root, height=4, width=50, bg='royal blue', fg='white')
        self.description_text.grid(row=3, column=0, pady=20)
        self.description_text.insert(tk.END, self.selected_game.description())

        tk.Button(self.root, text="Начать", fg='white', bg='royal blue', width=20, height=4, command=self.start_game, highlightthickness=0, borderwidth=0).grid(row=4, column=0, pady=2)
        tk.Button(self.root, text="Выход", fg='white', bg='royal blue', width=20, height=4, command=self.root.destroy, highlightthickness=0, borderwidth=0).grid(row=5, column=0, pady=2)

        # Кнопка "Вход в личный кабинет" в верхнем правом углу
        self.login_button = tk.Button(self.root, text="Вход в личный кабинет", fg='white', bg='royal blue', command=self.login, highlightthickness=0, borderwidth=0)
        self.login_button.place(relx=1.0, rely=0.0, x=-10, y=10, anchor='ne')

    def login(self):
        # Здесь добавьте код для входа в личный кабинет
        pass

    def select_game(self, game):
        self.selected_game = game
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, game.description())

    def start_game(self):
        if self.selected_game:
            self.selected_game.run()
        else:
            messagebox.showinfo("Ошибка", "Выберите игру перед началом!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    Navigator().run()
