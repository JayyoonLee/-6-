import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# 레시피 데이터 및 가격 정보
recipe_data = {
    "스파게티": [("파스타면", 200), ("토마토 소스", 150), ("올리브 오일", 30), ("파마산 치즈", 20)],
    "셀러드": [("양상추", 100), ("토마토", 50), ("오이", 30), ("베이비 당근", 20), ("올리브 오일", 10), ("레몬 주스", 5)],
}

# 재료별 가격
ingredient_prices = {
    "파스타면": 5,
    "토마토 소스": 4,
    "올리브 오일": 8,
    "파마산 치즈": 10,
    "양상추": 2,
    "토마토": 3,
    "오이": 2,
    "베이비 당근": 4,
    "레몬 주스": 1
}

def initialize(frame):
    def calculate_recipe_cost(recipe_name):
        """선택된 레시피의 총 비용 계산"""
        ingredients = recipe_data.get(recipe_name, [])
        total_cost = sum(ingredient_prices.get(item, 0) * (amount / 100) for item, amount in ingredients)
        return total_cost

    def show_recipe_cost():
        """비용 계산 결과를 표시하는 함수"""
        selected_recipe = recipe_combobox.get()
        if selected_recipe:
            cost = calculate_recipe_cost(selected_recipe)
            messagebox.showinfo("레시피 비용", f"{selected_recipe}의 총 비용은 {cost:.2f}입니다.")
        else:
            messagebox.showerror("에러", "레시피를 선택해주세요.")

    # 레시피 선택 콤보박스
    recipe_combobox = ttk.Combobox(frame, values=list(recipe_data.keys()), state='readonly')
    recipe_combobox.pack(pady=10)

    # 비용 계산 버튼
    show_recipe_cost_button = tk.Button(frame, text="레시피 비용 계산", command=show_recipe_cost)
    show_recipe_cost_button.pack(pady=10)
