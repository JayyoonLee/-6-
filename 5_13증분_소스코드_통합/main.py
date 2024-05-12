import tkinter as tk
from tkinter import Frame, Button

# 모듈 임포트
import Pantry_List, Pantry_State, Recipe_List, Recipe_Cost

# 프레임을 초기화하는 함수
def initialize_frame(module, frame):
    # 기존 프레임 내용 제거
    for widget in frame.winfo_children():
        widget.destroy()
    # 모듈 초기화 함수 호출
    module.initialize(frame)

# 메인 윈도우 설정
root = tk.Tk()
root.title("Module Management System")
root.geometry("600x400")

# 버튼을 위한 프레임 설정
button_frame = Frame(root)
button_frame.pack(fill=tk.X)

# 주 프레임 설정
main_frame = Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# 각 모듈에 대한 버튼 추가
buttons = [
    Button(button_frame, text="식재료 관리", command=lambda: initialize_frame(Pantry_List, main_frame)),
    Button(button_frame, text="재고 관리", command=lambda: initialize_frame(Pantry_State, main_frame)),
    Button(button_frame, text="레시피 관리", command=lambda: initialize_frame(Recipe_List, main_frame)),
    Button(button_frame, text="레시피 원가 관리", command=lambda: initialize_frame(Recipe_Cost, main_frame))
]

# 버튼을 버튼 프레임에 배치
for button in buttons:
    button.pack(side=tk.LEFT)

# 메인 윈도우 이벤트 루프 실행
root.mainloop()
