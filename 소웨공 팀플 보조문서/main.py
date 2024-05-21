import tkinter as tk
from tkinter import Frame, Button

# 모듈 임포트
import Food_Manage

# 프레임을 초기화하는 함수
def initialize_frame(module, frame):
    # 기존 프레임 내용 제거
    for widget in frame.winfo_children():
        widget.destroy()
    # 모듈 초기화 함수 호출
    module.initialize(frame)

# 메인 윈도우 설정
root = tk.Tk()
root.title("식재료 관리 프로그램")
# 전체화면 설정
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

# 버튼을 위한 프레임 설정
button_frame = Frame(root)
button_frame.pack(fill=tk.X)

# 주 프레임 설정
main_frame = Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# 각 모듈에 대한 버튼 추가
buttons = [
    Button(button_frame, text="식재료 관리", command=lambda: initialize_frame(Food_Manage, main_frame)),
    # 추가 모듈 버튼 추가 가능
]

# 버튼을 버튼 프레임에 배치
for button in buttons:
    button.pack(side=tk.LEFT)

# 메인 윈도우 이벤트 루프 시작
root.mainloop()
