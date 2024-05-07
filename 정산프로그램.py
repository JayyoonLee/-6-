import tkinter as tk
from tkinter import messagebox

# 식재료 정보를 저장하는 데이터 구조
ingredients = []

# GUI 초기화
root = tk.Tk()
root.title("식재료 정산 프로그램")

# 새로운 식재료 추가 함수
def add_ingredient():
    ingredient_name = ingredient_entry.get()
    ingredient_quantity = int(quantity_entry.get())
    ingredient_price = float(price_entry.get())
    ingredients.append((ingredient_name, ingredient_quantity, ingredient_price))
    messagebox.showinfo("추가 완료", f"{ingredient_name} {ingredient_quantity}개 추가되었습니다.")

# 식재료 목록 보기 함수
def show_ingredients():
    message = "식재료 목록:\n"
    for ingredient in ingredients:
        message += f"{ingredient[0]} - 수량: {ingredient[1]}, 가격: {ingredient[2]}\n"
    messagebox.showinfo("식재료 목록", message)

# 정산 함수
def calculate_costs():
    total_cost = sum(ingredient[1] * ingredient[2] for ingredient in ingredients)
    messagebox.showinfo("총 비용", f"총 비용은 {total_cost} 원 입니다.")

# 식재료 추가 UI
ingredient_frame = tk.Frame(root)
ingredient_frame.pack()
ingredient_label = tk.Label(ingredient_frame, text="식재료 이름:")
ingredient_label.grid(row=0, column=0)
ingredient_entry = tk.Entry(ingredient_frame)
ingredient_entry.grid(row=0, column=1)
quantity_label = tk.Label(ingredient_frame, text="수량:")
quantity_label.grid(row=1, column=0)
quantity_entry = tk.Entry(ingredient_frame)
quantity_entry.grid(row=1, column=1)
price_label = tk.Label(ingredient_frame, text="가격:")
price_label.grid(row=2, column=0)
price_entry = tk.Entry(ingredient_frame)
price_entry.grid(row=2, column=1)
add_ingredient_button = tk.Button(ingredient_frame, text="추가", command=add_ingredient)
add_ingredient_button.grid(row=3, columnspan=2)

# 식재료 목록 보기 버튼
show_ingredients_button = tk.Button(root, text="식재료 목록 보기", command=show_ingredients)
show_ingredients_button.pack()

# 정산 버튼
calculate_button = tk.Button(root, text="정산", command=calculate_costs)
calculate_button.pack()

# 이벤트 루프 시작
root.mainloop()
