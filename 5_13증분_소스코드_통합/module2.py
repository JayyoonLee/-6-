import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox, simpledialog

# 예시 데이터베이스: 간단한 재고 목록
inventory = {
    'Apples': 50,
    'Bananas': 75,
    'Cherries': 100
}

def initialize(frame):
    # 재고 추가 함수
    def add_inventory():
        add_window = Toplevel(frame)
        add_window.title("재고 추가")

        Label(add_window, text="상품명:").grid(row=0, column=0)
        Label(add_window, text="수량:").grid(row=1, column=0)
        product_entry = Entry(add_window)
        quantity_entry = Entry(add_window)
        product_entry.grid(row=0, column=1)
        quantity_entry.grid(row=1, column=1)

        def submit():
            product = product_entry.get()
            quantity = int(quantity_entry.get())
            if product in inventory:
                inventory[product] += quantity
            else:
                inventory[product] = quantity
            messagebox.showinfo("재고 추가", f"{product}의 재고가 {quantity}만큼 추가되었습니다.")
            add_window.destroy()

        Button(add_window, text="추가", command=submit).grid(row=2, columnspan=2)

    # 재고 보기 함수
    def view_inventory():
        inventory_window = Toplevel(frame)
        inventory_window.title("재고 목록")
        inventory_list = "\n".join(f"{item}: {qty}" for item, qty in inventory.items())
        Label(inventory_window, text=inventory_list).pack()

    # 재고 수정 함수
    def update_inventory():
        update_window = Toplevel(frame)
        update_window.title("재고 수정")

        Label(update_window, text="상품명:").grid(row=0, column=0)
        Label(update_window, text="새 수량:").grid(row=1, column=0)
        product_entry = Entry(update_window)
        new_quantity_entry = Entry(update_window)
        product_entry.grid(row=0, column=1)
        new_quantity_entry.grid(row=1, column=1)

        def submit():
            product = product_entry.get()
            new_quantity = int(new_quantity_entry.get())
            if product in inventory:
                inventory[product] = new_quantity
                messagebox.showinfo("재고 수정", f"{product}의 재고가 {new_quantity}으로 수정되었습니다.")
            else:
                messagebox.showerror("오류", f"{product}는 재고 목록에 없습니다.")
            update_window.destroy()

        Button(update_window, text="수정", command=submit).grid(row=2, columnspan=2)

    # 재고 삭제 함수
    def delete_inventory():
        product = simpledialog.askstring("재고 삭제", "삭제할 상품명 입력:")
        if product in inventory:
            del inventory[product]
            messagebox.showinfo("재고 삭제", f"{product}의 재고가 삭제되었습니다.")
        else:
            messagebox.showerror("오류", f"{product}는 재고 목록에 없습니다.")

    # 각 기능에 대한 버튼 추가
    Button(frame, text="재고 추가", command=add_inventory).pack(pady=5)
    Button(frame, text="재고 보기", command=view_inventory).pack(pady=5)
    Button(frame, text="재고 수정", command=update_inventory).pack(pady=5)
    Button(frame, text="재고 삭제", command=delete_inventory).pack(pady=5)

