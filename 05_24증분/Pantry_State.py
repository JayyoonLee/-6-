import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox, simpledialog
def apply_styles(widget, font=("Helvetica", 14), bg=None, fg="white"):
    widget.config(font=font, bg=bg, fg=fg, relief="solid")

inventory = {
    'Apples': 50,
    'Bananas': 75,
    'Cherries': 100
}

def initialize(frame):
    frame.config(bg="#f0f0f0")

    def add_inventory():
        add_window = Toplevel(frame)
        add_window.title("재고 추가")
        add_window.config(bg="#f0f0f0")

        Label(add_window, text="상품명:", bg="#f0f0f0").grid(row=0, column=0)
        Label(add_window, text="수량:", bg="#f0f0f0").grid(row=1, column=0)
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

        apply_styles(Button(add_window, text="추가", command=submit), bg="#4caf50")
        Button(add_window, text="추가", command=submit).grid(row=2, columnspan=2)

    def view_inventory():
        inventory_window = Toplevel(frame)
        inventory_window.title("재고 목록")
        inventory_window.config(bg="#f0f0f0")
        inventory_list = "\n".join(f"{item}: {qty}" for item, qty in inventory.items())
        Label(inventory_window, text=inventory_list, bg="#f0f0f0").pack()

    def update_inventory():
        update_window = Toplevel(frame)
        update_window.title("재고 수정")
        update_window.config(bg="#f0f0f0")

        Label(update_window, text="상품명:", bg="#f0f0f0").grid(row=0, column=0)
        Label(update_window, text="새 수량:", bg="#f0f0f0").grid(row=1, column=0)
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

        apply_styles(Button(update_window, text="수정", command=submit), bg="#2196f3")
        Button(update_window, text="수정", command=submit).grid(row=2, columnspan=2)

    def delete_inventory():
        product = simpledialog.askstring("재고 삭제", "삭제할 상품명 입력:")
        if product in inventory:
            del inventory[product]
            messagebox.showinfo("재고 삭제", f"{product}의 재고가 삭제되었습니다.")
        else:
            messagebox.showerror("오류", f"{product}는 재고 목록에 없습니다.")

    buttons = [
        ("재고 추가", add_inventory, "#4caf50"),
        ("재고 보기", view_inventory, "#2196f3"),
        ("재고 수정", update_inventory, "#ff9800"),
        ("재고 삭제", delete_inventory, "#f44336")
    ]

    for text, command, color in buttons:
        btn = Button(frame, text=text, command=command)
        apply_styles(btn, bg=color)
        btn.pack(pady=5)
