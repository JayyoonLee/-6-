import tkinter as tk
from tkinter import messagebox, Toplevel, simpledialog, Label, Button
import pandas as pd
from datetime import datetime

df = pd.DataFrame({
    "Name": ["Sample Item"],
    "Quantity": [10],
    "Unit Price": [100],
    "Location": ["Warehouse"],
    "Expiration Date": ["2024-01-01"]
})

def initialize(frame):
    def add_ingredient():
        input_frame = Toplevel(frame)
        input_frame.title("식재료 추가")

        tk.Label(input_frame, text="종류:").grid(row=0, column=0)
        tk.Label(input_frame, text="수량:").grid(row=1, column=0)
        tk.Label(input_frame, text="개당 가격:").grid(row=2, column=0)
        tk.Label(input_frame, text="위치:").grid(row=3, column=0)
        tk.Label(input_frame, text="유통기한 (YYYY-MM-DD):").grid(row=4, column=0)

        entries = {desc: tk.Entry(input_frame) for desc in ["Name", "Quantity", "Unit Price", "Location", "Expiration Date"]}
        for i, entry in enumerate(entries.values()):
            entry.grid(row=i, column=1)

        def confirm():
            data = {desc: entry.get() for desc, entry in entries.items()}
            if data["Expiration Date"] < datetime.today().strftime("%Y-%m-%d"):
                messagebox.showerror("유통기한 만료", f"{data['Name']}의 유통기한이 이미 만료되었습니다.")
            else:
                df.loc[len(df)] = list(data.values())
                messagebox.showinfo("추가 완료", f"{data['Name']}이(가) 추가되었습니다.")
                input_frame.destroy()

        tk.Button(input_frame, text="확인", command=confirm).grid(row=5, columnspan=2)

    def view_inventory():
        inventory_window = Toplevel(frame)
        inventory_window.title("재고 목록")
        label = Label(inventory_window, text=str(df))
        label.pack()

    def delete_ingredient():
        item_to_delete = simpledialog.askstring("삭제", "삭제할 식재료 이름 입력:")
        if item_to_delete in df['Name'].values:
            df.drop(df[df['Name'] == item_to_delete].index, inplace=True)
            messagebox.showinfo("삭제 완료", f"{item_to_delete}가 삭제되었습니다.")
        else:
            messagebox.showerror("찾을 수 없음", f"{item_to_delete}가 목록에 없습니다.")

    def check_expiration():
        expired_items = df[df['Expiration Date'] < datetime.today().strftime("%Y-%m-%d")]
        if not expired_items.empty:
            messagebox.showinfo("유통기한 만료", f"만료된 항목:\n{expired_items}")
        else:
            messagebox.showinfo("유통기한 만료", "만료된 항목이 없습니다.")

    # 버튼 생성
    tk.Button(frame, text="식재료 추가", command=add_ingredient).pack(pady=10)
    tk.Button(frame, text="재고 목록 보기", command=view_inventory).pack(pady=10)
    tk.Button(frame, text="삭제", command=delete_ingredient).pack(pady=10)
    tk.Button(frame, text="유통기한 확인", command=check_expiration).pack(pady=10)

