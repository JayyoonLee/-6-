import tkinter as tk
from Pantry_Management import PantryManagement

# 다른 모듈 import
import Recipe_Cost  # 수정된 Recipe_Cost 모듈 import
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
root.title("식당 관리 프로그램")
root.geometry("1200x800")
root.config(bg="#f0f0f0")

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(fill=tk.X, pady=10)

main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

pantry_management = PantryManagement()

buttons = [
    tk.Button(button_frame, text="식재료 관리", command=lambda: pantry_management.initialize(main_frame)),
    tk.Button(button_frame, text="레시피 관리", command=lambda: initialize_frame(Recipe_List, main_frame)),
    tk.Button(button_frame, text="레시피 원가 관리", command=lambda: initialize_frame(Recipe_Cost, main_frame)),
    tk.Button(button_frame, text="정산 관리", command=lambda: initialize_frame(Menu_Cost, main_frame)),
    tk.Button(button_frame, text="인기 메뉴 추천", command=lambda: initialize_frame(Menu_popular, main_frame)),
]

for button in buttons:
    apply_styles(button, bg="#4caf50")
    button.pack(side=tk.LEFT, padx=5, pady=5)

label = tk.Label(main_frame, text="원하는 메뉴를 선택하세요", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
label.pack(pady=20)

root.mainloop()
