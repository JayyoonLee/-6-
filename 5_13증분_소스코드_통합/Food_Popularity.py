import tkinter as tk
from tkinter import messagebox
from collections import defaultdict

# 사용자 레시피 데이터와 요리 횟수, 식재료를 저장할 딕셔너리
user_recipes = defaultdict(lambda: {'count': 0, 'ingredients': []})

# 인기 메뉴 추천 함수
def recommend_popular_menu():
    if not user_recipes:
        messagebox.showinfo("결과", "추천할 메뉴가 없습니다. 더 많은 레시피를 입력해주세요.")
        return
    
    # 요리 횟수를 기준으로 가장 많이 요리된 메뉴 찾기
    most_cooked_recipe = max(user_recipes, key=lambda recipe: user_recipes[recipe]['count'])
    
    # 가장 많이 사용된 식재료 찾기
    ingredient_count = defaultdict(int)
    for data in user_recipes.values():
        for ingredient in data['ingredients']:
            ingredient_count[ingredient] += 1
    if ingredient_count:
        most_used_ingredient = max(ingredient_count, key=ingredient_count.get)
    else:
        most_used_ingredient = "없음"
    
    # 결과 메시지 보여주기
    messagebox.showinfo("인기 메뉴 추천", 
                        f"가장 많이 요리된 메뉴: '{most_cooked_recipe}' (횟수: {user_recipes[most_cooked_recipe]['count']})\n"
                        f"가장 많이 사용된 식재료: '{most_used_ingredient}'")

# 레시피를 리스트에 추가하는 함수
def add_recipe():
    recipe = recipe_entry.get()
    ingredients = ingredient_entry.get().split(",")
    if recipe:
        # 레시피와 요리 횟수를 저장
        user_recipes[recipe]['count'] += 1
        user_recipes[recipe]['ingredients'].extend(ingredients)
        
        recipe_entry.delete(0, tk.END)  # 레시피 입력 필드 초기화
        ingredient_entry.delete(0, tk.END)  # 식재료 입력 필드 초기화
        messagebox.showinfo("레시피 추가", f"'{recipe}' 레시피가 추가되었습니다.")
    else:
        messagebox.showerror("오류", "레시피를 입력해주세요.")

# GUI 초기화
root = tk.Tk()
root.title("인기 메뉴 추천 시스템")

# 레시피 입력 필드
tk.Label(root, text="레시피 입력:").pack()
recipe_entry = tk.Entry(root)
recipe_entry.pack()

# 식재료 입력 필드
tk.Label(root, text="식재료 입력 (쉼표로 구분):").pack()
ingredient_entry = tk.Entry(root)
ingredient_entry.pack()

# 레시피 추가 버튼
add_button = tk.Button(root, text="레시피 추가", command=add_recipe)
add_button.pack()

# 인기 메뉴 추천 버튼
recommend_button = tk.Button(root, text="인기 메뉴 추천", command=recommend_popular_menu)
recommend_button.pack()

# 메인 루프 실행
root.mainloop()