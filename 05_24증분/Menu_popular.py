import tkinter as tk
from tkinter import messagebox
from collections import defaultdict

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

def add_recipe():
    recipe = recipe_entry.get()
    ingredients = ingredient_entry.get().split(",")
    if recipe:
        user_recipes[recipe]['count'] += 1
        user_recipes[recipe]['ingredients'].extend(ingredients)
        
        recipe_entry.delete(0, tk.END)
        ingredient_entry.delete(0, tk.END)
        messagebox.showinfo("레시피 추가", f"'{recipe}' 레시피가 추가되었습니다.")
    else:
        messagebox.showerror("오류", "레시피를 입력해주세요.")

def initialize(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    
    frame.config(bg="#f0f0f0")
    
    tk.Label(frame, text="레시피 입력:", bg="#f0f0f0").pack()
    global recipe_entry
    recipe_entry = tk.Entry(frame)
    recipe_entry.pack()

    tk.Label(frame, text="식재료 입력 (쉼표로 구분):", bg="#f0f0f0").pack()
    global ingredient_entry
    ingredient_entry = tk.Entry(frame)
    ingredient_entry.pack()

    add_button = tk.Button(frame, text="레시피 추가", command=add_recipe)
    apply_styles(add_button, bg="#4caf50")
    add_button.pack()

    recommend_button = tk.Button(frame, text="인기 메뉴 추천", command=recommend_popular_menu)
    apply_styles(recommend_button, bg="#2196f3")
    recommend_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("인기 메뉴 추천 시스템")
    root.geometry("800x600")
    root.config(bg="#f0f0f0")
    
    initialize(root)
    
    root.mainloop()
