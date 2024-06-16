import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# JSON 파일 경로
JSON_FILE_PATH = "recipes.json"

# JSON 파일 로드 함수
def load_recipes():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

class RestaurantGUI:
    def __init__(self, master):
        self.master = master
        self.master.config(bg="#f0f0f0")
        self.restaurant = Restaurant("My Restaurant")

        self.sales_frame = tk.LabelFrame(self.master, text="주문 기록", bg="#f0f0f0", padx=10, pady=10)
        self.sales_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.sales_label = tk.Label(self.sales_frame, text="판매된 항목:", bg="#f0f0f0")
        self.sales_label.grid(row=0, column=0, padx=5, pady=5)

        self.menu_combobox = ttk.Combobox(self.sales_frame)
        self.menu_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.quantity_label = tk.Label(self.sales_frame, text="수량:", bg="#f0f0f0")
        self.quantity_label.grid(row=0, column=2, padx=5, pady=5)
        self.quantity_entry = tk.Entry(self.sales_frame)
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=5)

        self.record_sale_button = tk.Button(self.sales_frame, text="기록", command=self.record_sale)
        apply_styles(self.record_sale_button, bg="#f44336")
        self.record_sale_button.grid(row=0, column=4, padx=5, pady=5)

        self.expenses_frame = tk.LabelFrame(self.master, text="지출 기록", bg="#f0f0f0", padx=10, pady=10)
        self.expenses_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.expenses_label = tk.Label(self.expenses_frame, text="지출 금액:", bg="#f0f0f0")
        self.expenses_label.grid(row=0, column=0, padx=5, pady=5)
        self.expenses_entry = tk.Entry(self.expenses_frame)
        self.expenses_entry.grid(row=0, column=1, padx=5, pady=5)

        self.record_expense_button = tk.Button(self.expenses_frame, text="기록", command=self.record_expense)
        apply_styles(self.record_expense_button, bg="#ff9800")
        self.record_expense_button.grid(row=0, column=2, padx=5, pady=5)

        self.profit_button = tk.Button(self.master, text="이익 계산", command=self.calculate_profit)
        apply_styles(self.profit_button, bg="#607d8b")
        self.profit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.info_text = tk.Text(self.master, height=10, width=50)
        self.info_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.menu_records_label = tk.Label(self.master, text="메뉴 항목", bg="#f0f0f0")
        self.menu_records_label.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.menu_records = tk.Text(self.master, height=10, width=30)
        self.menu_records.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.sales_records_label = tk.Label(self.master, text="판매 수량 기록", bg="#f0f0f0")
        self.sales_records_label.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.sales_records = tk.Text(self.master, height=10, width=30)
        self.sales_records.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        self.expenses_records_label = tk.Label(self.master, text="지출 기록", bg="#f0f0f0")
        self.expenses_records_label.grid(row=4, column=2, padx=10, pady=5, sticky="ew")

        self.expenses_records = tk.Text(self.master, height=10, width=30)
        self.expenses_records.grid(row=5, column=2, padx=10, pady=10, sticky="ew")

        self.load_menu()

    def load_menu(self):
        recipes = load_recipes()
        for name, details in recipes.items():
            price = details.get('판매가', 0)
            self.restaurant.add_item_to_menu(name, price)
            self.menu_combobox['values'] = list(self.restaurant.menu.keys())
            self.menu_records.insert(tk.END, f"{name}: {price}원\n")

    def record_sale(self):
        if self.restaurant:
            item = self.menu_combobox.get()
            quantity = int(self.quantity_entry.get())
            self.restaurant.record_sale(item, quantity)
            self.info_text.insert(tk.END, f"{item} {quantity}개를 주문하여 매출에 추가되었습니다.\n")
            self.sales_records.insert(tk.END, f"{item}: {quantity}개\n")
            self.update_total_profit()

    def record_expense(self):
        if self.restaurant:
            expense = float(self.expenses_entry.get())
            self.restaurant.record_expense(expense)
            self.info_text.insert(tk.END, f"{expense}원이 지출에 추가되었습니다.\n")
            self.expenses_records.insert(tk.END, f"{expense}원\n")

    def calculate_profit(self):
        if self.restaurant:
            self.restaurant.calculate_expenses()
            total_profit = self.restaurant.calculate_profit()
            total_sales = self.restaurant.calculate_sales()
            self.info_text.insert(tk.END, f"총 매출: {total_sales}원\n")
            self.info_text.insert(tk.END, f"총 이익: {total_profit}원\n")

    def update_total_profit(self):
        if self.restaurant:
            total_profit = self.restaurant.calculate_profit()
            self.total_profit_value.config(text=f"{total_profit}원")

class Restaurant:
    def __init__(self, name):
        self.name = name
        self.sales = {}
        self.expenses = 0
        self.profit = 0
        self.menu = {}

    def add_item_to_menu(self, item, price):
        self.menu[item] = price

    def record_sale(self, item, quantity):
        if item in self.menu:
            if item in self.sales:
                self.sales[item] += quantity
            else:
                self.sales[item] = quantity

    def record_expense(self, expense):
        self.expenses += expense

    def calculate_sales(self):
        total_sales = 0
        for item, quantity in self.sales.items():
            total_sales += self.menu[item] * quantity
        return total_sales

    def calculate_expenses(self):
        return self.expenses

    def calculate_profit(self):
        total_sales = self.calculate_sales()
        self.profit = total_sales - self.expenses
        return self.profit

def apply_styles(widget, font=("Helvetica", 14), bg=None, fg="white"):
    widget.config(font=font, bg=bg, fg=fg, relief="solid")

def initialize(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.config(bg="#f0f0f0")
    app = RestaurantGUI(frame)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("레시피 관리 프로그램")
    root.geometry("2000x1000")
    root.config(bg="#f0f0f0")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    initialize(main_frame)

    root.mainloop()
