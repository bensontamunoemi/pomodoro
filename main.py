import math
from tkinter import *
import pygame

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# Initialize Pygame mixer
pygame.mixer.init()


# ---------------------------- SOUND CONTROL ------------------------------- #
def play_sound():
    pygame.mixer.music.load('emergency.mp3')
    pygame.mixer.music.play(-1)  # Play indefinitely


def stop_sound():
    pygame.mixer.music.stop()


# ---------------------------- TIMER START ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        title_label.config(text="Break", bg=YELLOW, fg=RED, font=(FONT_NAME, 60, "bold"))
        count_down(long_break_sec)
        bring_window_to_front()
    elif reps % 2 == 0:
        title_label.config(text="Break", bg=YELLOW, fg=PINK, font=(FONT_NAME, 60, "bold"))
        count_down(short_break_sec)
        bring_window_to_front()
    else:
        title_label.config(text="Work", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 60, "bold"))
        count_down(work_sec)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    title_label.config(text="Timer")
    checkmark_label.config(text="")
    canvas.itemconfig(timer_text, text="00:00")
    global reps
    reps = 0
    window.attributes("-topmost", False)
    stop_sound()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer

    # Check for 15 seconds remaining in the respective periods
    if (reps % 8 == 0 and count == 15) or (reps % 2 == 0 and count == 15) or (reps % 2 != 0 and count == 15):
        play_sound()
    elif count == 0:  # Stop sound when timer reaches 0
        stop_sound()

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        checkmark_label.config(text=marks)


# ---------------------------- BRING WINDOW TO FRONT ------------------------------- #
def bring_window_to_front():
    window.attributes("-topmost", True)  # Stay on top
    window.lift()  # Lift window above others
    window.focus_force()  # Force focus on the window


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
window.resizable(False, False)

title_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 60, "bold"))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_image = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_image)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_btn = Button(text="Start", highlightbackground=YELLOW, command=start_timer)
start_btn.grid(column=0, row=2)

reset_btn = Button(text="Reset", highlightbackground=YELLOW, command=reset_timer)
reset_btn.grid(column=2, row=2)

checkmark_label = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 30, "bold"))
checkmark_label.grid(column=1, row=3)

window.mainloop()
