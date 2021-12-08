from tkinter import *

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT = "Courier"
FONT_SIZE = 18
FONT_STYLE = "bold"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20


class Pomodoro(Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro")
        self.config(padx=100, pady=50, bg=YELLOW)
        self.completed_work_periods = 0
        self.repetitions = 0
        self.attributes("-topmost", True)
        self.timer = None

        self.canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
        self.image = PhotoImage(file="tomato.png")

        self.canvas.create_image(100, 112, image=self.image)
        self.timer_text = self.canvas.create_text(100, 130, text="00:00", fill="white",
                                                  font=(FONT, FONT_SIZE, FONT_STYLE))
        self.canvas.grid(row=1, column=1)

        self.current_status = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT, 32, FONT_STYLE))
        self.current_status.grid(row=0, column=1)

        self.button_start = Button(text="Start", fg=RED, font=(FONT, FONT_SIZE, FONT_STYLE),
                                   command=self.start_countdown)
        self.button_start.grid(row=2, column=0)

        self.button_reset = Button(text="Reset", fg=RED, font=(FONT, FONT_SIZE, FONT_STYLE), command=self.reset_timer)
        self.button_reset.grid(row=2, column=2)

        self.completed_work_label = Label(text="0 / 4", fg=GREEN, bg=YELLOW, font=(FONT, FONT_SIZE, FONT_STYLE))
        self.completed_work_label.grid(row=2, column=1)

        self.mainloop()

    def start_countdown(self):
        self.repetitions += 1

        work_time_in_s = WORK_MIN * 60
        short_break_in_s = SHORT_BREAK_MIN * 60
        long_break_in_s = LONG_BREAK_MIN * 60

        if self.repetitions % 8 == 0:
            self.countdown(long_break_in_s)
            self.current_status.config(text="Break", fg=RED)
        elif self.repetitions % 2 == 0:
            self.countdown(short_break_in_s)
            self.current_status.config(text="Break", fg=PINK)
        else:
            self.countdown(work_time_in_s)
            self.current_status.config(text="Work", fg=GREEN)

    def countdown(self, count):
        minutes = count // 60
        seconds = count % 60

        if minutes < 10:
            minutes = f"0{minutes}"
        if seconds < 10:
            seconds = f"0{seconds}"

        self.canvas.itemconfig(self.timer_text, text=f"{minutes}:{seconds}")

        if count > 0:
            self.timer = self.after(1000, self.countdown, count - 1)
        else:
            self.bell()
            self.start_countdown()
            if self.repetitions == 9 and self.completed_work_periods == 4:
                self.reset_timer()
            elif self.repetitions % 2 == 0:
                self.completed_work_periods += 1
            self.completed_work_label.config(text=f"{self.completed_work_periods} / 4")

    def reset_timer(self):
        try:
            self.after_cancel(self.timer)
            self.timer = None
            self.repetitions = 0
            self.completed_work_periods = 0
            self.canvas.itemconfig(self.timer_text, text="00:00")
            self.completed_work_label.config(text="0 / 4")
            self.current_status.config(text="Timer", fg=GREEN)
        except ValueError:
            pass


app = Pomodoro()
