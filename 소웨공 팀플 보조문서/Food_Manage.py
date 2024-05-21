import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime

# 식재료 정보 담는 데이터프레임 생성
df = pd.DataFrame(columns=["Name", "Quantity", "Unit Price", "Location", "Expiration Date"])

def initialize(frame):
    # GUI 초기화
    root = tk.Tk()
    root.title("식재료 관리 프로그램")

    # 전체화면 설정
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    # 화면 크기 가져오기
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 새로운 식재료 추가 함수
    def add_ingredient():
        input_frame = tk.Toplevel(root)
        input_frame.title("식재료 추가")
        window_width = screen_width // 3
        window_height = screen_height // 3
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        input_frame.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        tk.Label(input_frame, text="종류:").grid(row=0, column=0, sticky="w")
        tk.Label(input_frame, text="수량:").grid(row=1, column=0, sticky="w")
        tk.Label(input_frame, text="개당 가격:").grid(row=2, column=0, sticky="w")
        tk.Label(input_frame, text="위치:").grid(row=3, column=0, sticky="w")
        tk.Label(input_frame, text="유통기한 (YYYY-MM-DD):").grid(row=4, column=0, sticky="w")
        name_entry = tk.Entry(input_frame)
        quantity_entry = tk.Entry(input_frame)
        unit_price_entry = tk.Entry(input_frame)
        location_entry = tk.Entry(input_frame)
        expiration_entry = tk.Entry(input_frame)
        name_entry.grid(row=0, column=1, sticky="ew")
        quantity_entry.grid(row=1, column=1, sticky="ew")
        unit_price_entry.grid(row=2, column=1, sticky="ew")
        location_entry.grid(row=3, column=1, sticky="ew")
        expiration_entry.grid(row=4, column=1, sticky="ew")

        input_frame.grid_columnconfigure(1, weight=1)

        def confirm():
            name = name_entry.get()
            quantity = quantity_entry.get()
            unit_price = unit_price_entry.get()
            location = location_entry.get()
            expiration_date = expiration_entry.get()
            
            today = datetime.today().strftime("%Y-%m-%d")
            if expiration_date < today:
                messagebox.showerror("유통기한 만료", f"{name}의 유통기한이 이미 만료되었습니다.")
            else:
                df.loc[len(df)] = [name, quantity, unit_price, location, expiration_date]
                messagebox.showinfo("추가 완료", f"{name}이(가) 추가되었습니다.")
                input_frame.destroy()

        confirm_button = tk.Button(input_frame, text="확인", command=confirm)
        confirm_button.place(relx=0.5 , rely=0.8, anchor="center",width=200, height=50 )

    def show_ingredients():
        messagebox.showinfo("식재료 목록", df.to_string(index=False))

    def delete_ingredient():
        input_frame = tk.Toplevel(root) 
        input_frame.title("식재료 삭제")
        window_width = screen_width // 3
        window_height = screen_height // 3
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        input_frame.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        tk.Label(input_frame, text="식재료 명:").grid(row=0, column=0, sticky="w")
        name_entry = tk.Entry(input_frame)
        name_entry.grid(row=0, column=1, sticky="ew")

        input_frame.grid_columnconfigure(1, weight=1)

        def confirm():
            name = name_entry.get()
            if name in df["Name"].values:
                df.drop(df[df["Name"] == name].index, inplace=True)
                messagebox.showinfo("성공", f"{name} 삭제되었습니다!")
            else:
                messagebox.showerror("오류", f"{name}을(를) 찾을 수 없습니다!")
            input_frame.destroy()

        confirm_button = tk.Button(input_frame, text="확인", command=confirm)
        confirm_button.grid(row=1, columnspan=2)

    def check_expiration():
        today = datetime.today().strftime("%Y-%m-%d")
        expired_ingredients = df[df["Expiration Date"] < today]
        if not expired_ingredients.empty:
            for index, row in expired_ingredients.iterrows():
                df.drop(index, inplace=True)
            messagebox.showinfo("유통기한 알림", "유통기한이 만료된 식재료가 삭제되었습니다.")
        else:
            messagebox.showinfo("유통기한 알림", "현재 유통기한이 만료된 식재료가 없습니다.")

    # 버튼 생성 및 배치
    buttons = [("식재료 추가", add_ingredient),
            ("식재료 목록", show_ingredients),
            ("식재료 삭제", delete_ingredient),
            ("유통기한 확인", check_expiration)]

    button_width = 300
    button_height = 150
    button_spacing = 10
    total_button_width = len(buttons) * (button_width + button_spacing) - button_spacing
    x_start = (screen_width - total_button_width) // 2

    
    y_offset = -200  # 버튼들을 화면 위쪽으로 200 픽셀 올림

    for i, (text, command) in enumerate(buttons):
        button = tk.Button(root, text=text, command=command, width=button_width, height=button_height, bg="lightgrey")
        x_position = x_start + i * (button_width + button_spacing)
        y_position = screen_height // 2 - button_height // 2 + y_offset
        button.place(x=x_position, y=y_position, width=button_width, height=button_height)

    # 뒤로 가기 메소드
    def go_back():
        root.destroy()  # 현재 화면 종료

    # 뒤로 가기 버튼 배치
    back_button = tk.Button(root, text="뒤로 가기", command=go_back, bg="lightgrey")
    back_button.pack(side=tk.BOTTOM, pady=20)

    # 이벤트 루프 시작
    root.mainloop()

