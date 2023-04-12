import contextlib
import turtle
import math
import tkinter as tk
from tkinter import simpledialog, messagebox, colorchooser
import random


# Generate a random color in hexadecimal format
def random_color():
    return f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'


# Determine if a color is dark based on its RGB values
def is_dark_color(color):
    r, g, b = turtle.Screen().getcanvas().winfo_rgb(color)
    r, g, b = r / 255, g / 255, b / 255
    return (r * 0.299 + g * 0.587 + b * 0.114) < 128


# Function to exit the program when the turtle window is closed
def on_closing():
    exit()


# Draw circle parts based on angles and colors provided
def draw_circle_parts(angles, colors, radius, max_arc_length=50):
    t = turtle.Turtle()
    turtle.title(angles)
    t.speed("fastest")
    t.penup()
    t.goto(0, -radius)

    total_angle = sum(angles)
    for i, angle in enumerate(angles):
        t.fillcolor(colors[i])
        t.begin_fill()
        t.goto(0, 0)
        t.setheading(90)
        start_angle = sum(angles[:i])
        end_angle = start_angle + angle
        arc_length = radius * math.pi * angle / 180
        for j in range(int(start_angle), int(end_angle) + 1):
            t.goto(radius * math.cos(j * math.pi / 180), radius * math.sin(j * math.pi / 180))
        t.goto(0, 0)
        t.end_fill()

        # Display the percentage text for each slice
        if arc_length > max_arc_length:
            t.penup()
            angle_percent = round(angle / total_angle * 100, 2)
            t.goto(radius * 0.8 * math.cos((start_angle + end_angle) / 2 * math.pi / 180),
                   radius * 0.8 * math.sin((start_angle + end_angle) / 2 * math.pi / 180))
            t.pendown()
            # Change text color based on the slice color
            if is_dark_color(colors[i]):
                t.pencolor('white')
            else:
                t.pencolor('black')
            t.write(f'{angle_percent}%', align='center', font=('Arial', 8, 'normal'))
            t.penup()

    t.hideturtle()
    turtle_screen = turtle.Screen()
    turtle_screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", on_closing)
    turtle_screen.mainloop()


def main():
    angles = []
    colors = []
    total = 0

    root = tk.Tk()
    root.withdraw()

    # Collect slice data from the user
    while total != 100:
        data = simpledialog.askfloat('Percentage', '[*] Enter a percentage:')
        if data is None:
            exit()
        if total + data > 100:
            messagebox.showerror('Error', f'The sum of percentages exceeds 100... ({100 - total}% remaining)')
        else:
            angles.append(data * 3.6)
            total += data
            color = colorchooser.askcolor(title="Choose a color... (Close for a random one)")[1]
            if color is None:
                # Select a random color
                color = random_color()
            colors.append(color)
    with contextlib.suppress(turtle.Terminator):
        draw_circle_parts(angles, colors, 200)


if __name__ == '__main__':
    main()
