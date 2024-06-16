import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import json
import os

# JSON 파일 경로
JSON_FILE_PATH = "recipes.json"

# JSON 파일 로드 함수
def load_recipe_data():
    global recipe_data
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            recipe_data = json.load(file)
    else:
        recipe_data = {}

# JSON 파일 저장 함수
def save_to_json():
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(recipe_data, file, ensure_ascii=False, indent=4)
    print(f"Saved recipes to {JSON_FILE_PATH}")

# 초기 데이터 로드
load_recipe_data()

# CSV 파일 로드
ingredients_csv_path = "Ingredients.csv"
df = pd.read_csv(ingredients_csv_path, encoding='utf-8')

def apply_styles(widget, font=("Helvetica", 14), bg=None, fg="white"):
    widget.config(font=font, bg=bg, fg=fg, relief="solid")

def calculate_recipe_cost(recipe_name):
    recipe_ingredients = recipe_data.get(recipe_name)
    if recipe_ingredients:
        total_cost = 0
        missing_ingredients = []
        for ingredient, amount in recipe_ingredients.items():
            if ingredient in ['판매가', '원자재값']:
                continue
            ingredient_info = df[df["Name"] == ingredient]
            if not ingredient_info.empty:
                unit_price = float(ingredient_info.iloc[0]["Unit Price"])
                total_cost += unit_price * int(amount)
            else:
                missing_ingredients.append(ingredient)
        return total_cost, missing_ingredients
    else:
        return None, None

def find_shortage_ingredients(recipe_name):
    recipe_ingredients = recipe_data.get(recipe_name)
    if recipe_ingredients:
        shortage = {}
        for ingredient, amount in recipe_ingredients.items():
            if ingredient in ['판매가', '원자재값']:
                continue
            ingredient_info = df[df["Name"] == ingredient]
            if not ingredient_info.empty:
                available_quantity = int(ingredient_info.iloc[0]["Quantity"])
                if available_quantity < int(amount):
                    shortage[ingredient] = int(amount) - available_quantity
        return shortage
    else:
        return None

def show_recipe_cost():
    selected_recipe = recipe_combobox.get()
    if selected_recipe:
        cost, missing_ingredients = calculate_recipe_cost(selected_recipe)
        if cost is not None:
            # 레시피의 원자재값을 JSON 파일에 저장
            recipe_data[selected_recipe]['원자재값'] = cost
            costper = cost*100/recipe_data[selected_recipe].get('판매가','설정되지 않음')
            save_to_json()
            
            message = f"{selected_recipe}의 원자재값: {cost}원"
            if missing_ingredients:
                message += "\n등록되지 않은 식재료가 존재합니다:\n"
                for ingredient in missing_ingredients:
                    message += f"- {ingredient}\n"
                message += f"원가율 : {costper}%"
            messagebox.showinfo("레시피 원자재값", message)

        else:
            messagebox.showerror("에러", "레시피 정보를 가져올 수 없거나 필요한 식재료가 부족합니다.")
    else:
        messagebox.showerror("에러", "레시피를 선택해주세요.")

def show_shortage_ingredients():
    selected_recipe = recipe_combobox.get()
    if selected_recipe:
        shortage = find_shortage_ingredients(selected_recipe)
        if shortage:
            message = "부족한 식재료:\n"
            for ingredient, amount in shortage.items():
                message += f"- {ingredient}: {amount}\n"
            messagebox.showinfo("부족한 식재료", message)
        else:
            messagebox.showinfo("부족한 식재료", "부족한 식재료가 없습니다.")
    else:
        messagebox.showerror("에러", "레시피를 선택해주세요.")

def initialize(frame):
    frame.config(bg="#f0f0f0")

    global recipe_combobox

    recipe_combobox = ttk.Combobox(frame, values=list(recipe_data.keys()))
    recipe_combobox.pack(pady=10)

    show_recipe_cost_button = tk.Button(frame, text="원자재가 확인", command=show_recipe_cost)
    apply_styles(show_recipe_cost_button, bg="#4caf50")
    show_recipe_cost_button.pack(pady=10)

    show_shortage_ingredients_button = tk.Button(frame, text="부족한 식재료 보기", command=show_shortage_ingredients)
    apply_styles(show_shortage_ingredients_button, bg="#f44336")
    show_shortage_ingredients_button.pack(pady=10)

def update_recipe_data():
    load_recipe_data()
    recipe_combobox['values'] = list(recipe_data.keys())

if __name__ == "__main__":
    root = tk.Tk()
    root.title("원가 계산 프로그램")
    root.geometry("800x600")
    root.config(bg="#f0f0f0")

    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(fill=tk.BOTH, expand=True)

    initialize(main_frame)

    root.mainloop()
