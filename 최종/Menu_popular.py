import tkinter as tk
from tkinter import messagebox
import pandas as pd
import json
import os

# 파일 경로
JSON_FILE_PATH = "recipes.json"
MENU_SALES_FILE_PATH = "menu_sales.csv"

# JSON 파일이 있으면 로드하고, 없으면 빈 딕셔너리 생성
if os.path.exists(JSON_FILE_PATH):
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        recipes = json.load(file)
else:
    recipes = {}

def apply_styles(widget, font=("Helvetica", 14), bg=None, fg="white"):
    widget.config(font=font, bg=bg, fg=fg, relief="solid")

def recommend_popular_menu():
    if not os.path.exists(MENU_SALES_FILE_PATH):
        messagebox.showinfo("결과", "추천할 메뉴가 없습니다. 더 많은 레시피를 입력해주세요.")
        return

    df = pd.read_csv(MENU_SALES_FILE_PATH)
    if df.empty:
        messagebox.showinfo("결과", "추천할 메뉴가 없습니다. 더 많은 레시피를 입력해주세요.")
        return

    most_cooked_recipe = df.loc[df['count'].idxmax()]['메뉴']
    count = df.loc[df['count'].idxmax()]['count']

    if most_cooked_recipe in recipes:
        recipe_ingredients = recipes[most_cooked_recipe]
        filtered_ingredients = {k: v for k, v in recipe_ingredients.items() if k not in ['판매가', '원자재값']}
        most_used_ingredient = max(filtered_ingredients, key=filtered_ingredients.get)
        most_used_amount = filtered_ingredients[most_used_ingredient]

        messagebox.showinfo("인기 메뉴 추천", 
                            f"가장 많이 요리된 메뉴: '{most_cooked_recipe}' (횟수: {count})\n"
                            f"가장 많이 사용된 식재료: '{most_used_ingredient}'")
    else:
        messagebox.showerror("에러", "레시피 정보를 가져올 수 없습니다.")

def initialize(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    
    frame.config(bg="#f0f0f0")

    recommend_button = tk.Button(frame, text="인기 메뉴 추천", command=recommend_popular_menu)
    apply_styles(recommend_button, bg="#2196f3")
    recommend_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("인기 메뉴 추천 시스템")
    root.geometry("800x600")
    root.config(bg="#f0f0f0")
    
    initialize(root)
    
    root.mainloop()
