import tkinter as tk    # GUI 만들기 위함
from tkinter import messagebox
import pandas as pd     # 데이터 프레임 사용을 위함
from datetime import datetime   # 오늘 날짜 확인 위함

# 식재료 정보 담는 데이터프레임 생성
df = pd.DataFrame(columns=["Name", "Quantity", "Unit Price", "Location", "Expiration Date"])

# GUI 초기화
root = tk.Tk()
root.title("식재료 관리 프로그램")

# 새로운 식재료 추가 함수
def add_ingredient():
    # 입력 폼 생성
    input_frame = tk.Toplevel(root)
    input_frame.title("식재료 추가")

    # 각 항목에 대한 레이블 및 입력 필드 생성
    tk.Label(input_frame, text="종류:").grid(row=0, column=0)
    tk.Label(input_frame, text="수량:").grid(row=1, column=0)
    tk.Label(input_frame, text="개당 가격:").grid(row=2, column=0)
    tk.Label(input_frame, text="위치:").grid(row=3, column=0)
    tk.Label(input_frame, text="유통기한 (YYYY-MM-DD):").grid(row=4, column=0)
    name_entry = tk.Entry(input_frame)
    quantity_entry = tk.Entry(input_frame)
    unit_price_entry = tk.Entry(input_frame)
    location_entry = tk.Entry(input_frame)
    expiration_entry = tk.Entry(input_frame)
    name_entry.grid(row=0, column=1)
    quantity_entry.grid(row=1, column=1)
    unit_price_entry.grid(row=2, column=1)
    location_entry.grid(row=3, column=1)
    expiration_entry.grid(row=4, column=1)

    # 확인 버튼 생성 
    def confirm():
        name = name_entry.get()
        quantity = quantity_entry.get()
        unit_price = unit_price_entry.get()
        location = location_entry.get()
        expiration_date = expiration_entry.get()
        
        # 이미 유통기한 지난 식재료는 추가 X
        today = datetime.today().strftime("%Y-%m-%d")
        if expiration_date < today:
            messagebox.showerror("유통기한 만료", f"{name}의 유통기한이 이미 만료되었습니다.")
        else:
            # 데이터프레임에 추가
            df.loc[len(df)] = [name, quantity, unit_price, location, expiration_date]
            messagebox.showinfo("추가 완료", f"{name}이(가) 추가되었습니다.")
            input_frame.destroy()

    # 확인 버튼 생성하고 클릭 시 confirm 함수가 실행되도록함
    confirm_button = tk.Button(input_frame, text="확인", command=confirm)
    confirm_button.grid(row=5, columnspan=2)

# 식재료 조회 함수
def show_ingredients():
    messagebox.showinfo("식재료 목록", df.to_string(index=False))

# 식재료 삭제 함수
def delete_ingredient():
    # 입력 폼 생성
    input_frame = tk.Toplevel(root) # 새로운 창 생성
    input_frame.title("식재료 삭제")    # 새로운 창의 제목 = 식재료 삭제

    # 레이블 및 입력 필드 생성
    # 식재료 명 입력받고 해당 식재료를 데이터 프레임에서 삭제함
    tk.Label(input_frame, text="식재료 명:").grid(row=0, column=0)
    name_entry = tk.Entry(input_frame)
    name_entry.grid(row=0, column=1)

    # 확인 버튼 생성
    def confirm():
        # 입력된 식재료를 데이터프레임에서 삭제
        name = name_entry.get()
        if name in df["Name"].values:
            df.drop(df[df["Name"] == name].index, inplace=True)
            messagebox.showinfo("성공", f"{name} 삭제되었습니다!")
        else:
            messagebox.showerror("오류", f"{name}을(를) 찾을 수 없습니다!")
        # 창 닫기
        input_frame.destroy()

    # 확인 버튼 생성 & 클릭 시 confirm() 실행
    confirm_button = tk.Button(input_frame, text="확인", command=confirm)
    confirm_button.grid(row=1, columnspan=2)

# 유통기한 알림 확인 함수
def check_expiration():
    # 오늘 날짜 가져오기
    today = datetime.today().strftime("%Y-%m-%d")
    # 유통기한 만료된 식재료 확인
    expired_ingredients = df[df["Expiration Date"] < today]
    # 만료된 식재료가 있을 시 삭제하고 메시지를 통해 알림
    if not expired_ingredients.empty:
        for index, row in expired_ingredients.iterrows():
            df.drop(index, inplace=True)
        messagebox.showinfo("유통기한 알림", f"유통기한이 만료된 식재료가 삭제되었습니다.")
    else:
        messagebox.showinfo("유통기한 알림", "현재 유통기한이 만료된 식재료가 없습니다.")


# 버튼 생성
# 추가 목록보기 삭제 유통기한 확인 버튼 생성
add_button = tk.Button(root, text="추가", command=add_ingredient)
add_button.pack()
show_button = tk.Button(root, text="목록 보기", command=show_ingredients)
show_button.pack()
delete_button = tk.Button(root, text="삭제", command=delete_ingredient)
delete_button.pack()
check_button = tk.Button(root, text="유통기한 만료 확인", command=check_expiration)
check_button.pack()

# 이벤트 루프 시작
root.mainloop()
