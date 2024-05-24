import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime

# 식재료 정보 담는 데이터프레임 생성
df = pd.DataFrame(columns=["Name", "Quantity", "Unit Price", "Location", "Expiration Date"])

# UI 스타일 적용 함수
def apply_styles(widget, font=("Helvetica", 14), bg=None, fg="white"):
    widget.config(font=font, bg=bg, fg=fg, relief="solid")

# 새로운 식재료 추가 함수
def add_ingredient(frame):
    # 입력 폼 생성
    input_frame = tk.Toplevel(frame)
    input_frame.title("식재료 추가")
    input_frame.config(bg="#f0f0f0")

    labels_texts = ["종류:", "수량:", "개당 가격:", "위치:", "유통기한 (YYYY-MM-DD):"]
    entries = {}

    for i, text in enumerate(labels_texts):
        tk.Label(input_frame, text=text, font=("Helvetica", 14), bg="#f0f0f0").grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(input_frame, font=("Helvetica", 14))
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[text.split(":")[0]] = entry

    def confirm():
        data = {desc: entry.get() for desc, entry in entries.items()}

        # 필수 필드가 비어 있는지 확인
        for key, value in data.items():
            if not value:
                messagebox.showerror("입력 오류", f"{key} 필드를 입력해주세요.")
                return

        # 유통기한이 이미 지난 경우를 처리
        if "유통기한" in data and data["유통기한"] < datetime.today().strftime("%Y-%m-%d"):
            messagebox.showerror("유통기한 만료", f"{data['종류']}의 유통기한이 이미 만료되었습니다.")
            return

        df.loc[len(df)] = data.values()
        messagebox.showinfo("추가 완료", f"{data['종류']}이(가) 추가되었습니다.")
        input_frame.destroy()

    confirm_button = tk.Button(input_frame, text="확인", command=confirm)
    apply_styles(confirm_button, bg="#4caf50")
    confirm_button.grid(row=5, columnspan=2, pady=10)

# 식재료 조회 함수
def show_ingredients():
    messagebox.showinfo("식재료 목록", df.to_string(index=False))

# 식재료 삭제 함수
def delete_ingredient(frame):
    input_frame = tk.Toplevel(frame)
    input_frame.title("식재료 삭제")
    input_frame.config(bg="#f0f0f0")

    tk.Label(input_frame, text="식재료 명:", font=("Helvetica", 14), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(input_frame, font=("Helvetica", 14))
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    def confirm():
        name = name_entry.get()
        if name in df["Name"].values:
            df.drop(df[df["Name"] == name].index, inplace=True)
            messagebox.showinfo("성공", f"{name} 삭제되었습니다!")
        else:
            messagebox.showerror("오류", f"{name}을(를) 찾을 수 없습니다!")
        input_frame.destroy()

    confirm_button = tk.Button(input_frame, text="확인", command=confirm)
    apply_styles(confirm_button, bg="#f44336")
    confirm_button.grid(row=1, columnspan=2, pady=10)

# 유통기한 알림 확인 함수
def check_expiration():
    today = datetime.today().strftime("%Y-%m-%d")
    expired_ingredients = df[df["Expiration Date"] < today]
    if not expired_ingredients.empty:
        for index, row in expired_ingredients.iterrows():
            df.drop(index, inplace=True)
        messagebox.showinfo("유통기한 알림", "유통기한이 만료된 식재료가 삭제되었습니다.")
    else:
        messagebox.showinfo("유통기한 알림", "현재 유통기한이 만료된 식재료가 없습니다.")

def initialize(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    
    frame.config(bg="#f0f0f0")

    add_button = tk.Button(frame, text="추가", command=lambda: add_ingredient(frame))
    apply_styles(add_button, bg="#4caf50")
    add_button.pack(pady=5, padx=10, fill=tk.X)

    show_button = tk.Button(frame, text="목록 보기", command=show_ingredients)
    apply_styles(show_button, bg="#2196f3")
    show_button.pack(pady=5, padx=10, fill=tk.X)

    delete_button = tk.Button(frame, text="삭제", command=lambda: delete_ingredient(frame))
    apply_styles(delete_button, bg="#ff9800")
    delete_button.pack(pady=5, padx=10, fill=tk.X)

    check_button = tk.Button(frame, text="유통기한 만료 확인", command=check_expiration)
    apply_styles(check_button, bg="#f44336")
    check_button.pack(pady=5, padx=10, fill=tk.X)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("식재료 관리 프로그램")
    root.geometry("800x600")
    root.config(bg="#f0f0f0")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    initialize(main_frame)

    root.mainloop()
