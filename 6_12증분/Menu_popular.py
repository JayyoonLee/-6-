import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import json
import os

# JSON 파일 경로
JSON_FILE_PATH = "recipes.json"

# JSON 파일이 있으면 로드하고, 없으면 빈 딕셔너리 생성
if os.path.exists(JSON_FILE_PATH):
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        recipes = json.load(file)
else:
    recipes = {}

user_recipes = defaultdict(lambda: {'count': 0, 'ingredients': []})

def apply_styles(widget, font=("Helvetica", 14), bg=None, fg="white"):
    widget.config(font=font, bg=bg, fg=fg, relief="solid")

def recommend_popular_menu():
    if not user_recipes:
        messagebox.showinfo("결과", "추천할 메뉴가 없습니다. 더 많은 레시피를 입력해주세요.")
        return

    most_cooked_recipe = max(user_recipes, key=lambda recipe: user_recipes[recipe]['count'])

    ingredient_count = defaultdict(int)
    for data in user_recipes.values():
        for ingredient in data['ingredients']:
            ingredient_count[ingredient] += 1
    if ingredient_count:
        most_used_ingredient = max(ingredient_count, key=ingredient_count.get)
    else:
        most_used_ingredient = "없음"

    messagebox.showinfo("인기 메뉴 추천", 
                        f"가장 많이 요리된 메뉴: '{most_cooked_recipe}' (횟수: {user_recipes[most_cooked_recipe]['count']})\n"
                        f"가장 많이 사용된 식재료: '{most_used_ingredient}'")

def initialize(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    
    frame.config(bg="#f0f0f0")

    # recipes.json 파일에서 레시피를 직접 등록
    for recipe_name, ingredients in recipes.items():
        user_recipes[recipe_name]['count'] += 1
        user_recipes[recipe_name]['ingredients'].extend(ingredients.keys())
    
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
