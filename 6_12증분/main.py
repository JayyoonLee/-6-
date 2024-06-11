import tkinter as tk
from tkinter import Frame, Button, Label
import Recipe_Cost  # 수정된 Recipe_Cost 모듈 import
import Pantry_Management
import Recipe_List
import Menu_popular
import Menu_Cost

def initialize_frame(module, frame):
    for widget in frame.winfo_children():
        widget.destroy()
    module.initialize(frame)

def apply_styles(widget, font=("Helvetica", 14), bg=None, fg="white"):
    widget.config(font=font, bg=bg, fg=fg, relief="solid")

root = tk.Tk()
root.title("Module Management System")
root.geometry("1200x800")
root.config(bg="#f0f0f0")

button_frame = Frame(root, bg="#f0f0f0")
button_frame.pack(fill=tk.X, pady=10)

main_frame = Frame(root, bg="#f0f0f0")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

buttons = [
    Button(button_frame, text="식재료 관리", command=lambda: initialize_frame(Pantry_Management, main_frame)),
    Button(button_frame, text="레시피 관리", command=lambda: initialize_frame(Recipe_List, main_frame)),
    Button(button_frame, text="레시피 원가 관리", command=lambda: initialize_frame(Recipe_Cost, main_frame)),
    Button(button_frame, text="메뉴 인기 추천", command=lambda: initialize_frame(Menu_popular, main_frame)),
    Button(button_frame, text="메뉴 비용 관리", command=lambda: initialize_frame(Menu_Cost, main_frame)),
]

for button in buttons:
    apply_styles(button, bg="#4caf50" if "식재료" in button.cget("text") else "#2196f3")
    button.pack(side=tk.LEFT, padx=5, pady=5)

label = Label(main_frame, text="모듈을 선택하세요", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
label.pack(pady=20)

root.mainloop()
