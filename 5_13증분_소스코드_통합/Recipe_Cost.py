import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

class RecipeCostCalculator:
    def __init__(self, frame):
        self.frame = frame
        self.init_gui()

    def init_gui(self):
        # 데이터 초기화 (예시 데이터)
        self.df = pd.DataFrame({
            "Name": ["파스타면", "토마토 소스", "올리브 오일", "파마산 치즈", "토마토", "양상추", "오이", "베이비 당근"],
            "Quantity": [3, 2, 1, 5, 4, 1, 1, 1],
            "Unit Price": [1, 1500, 200, 30, 700, 1150, 2350, 4150],
            "Location": ["냉장고", "냉장고", "냉장고", "냉장고", "냉장고", "냉장고", "냉장고", "냉장고"],
            "Expiration Date": ["2024-05-20", "2024-05-15", "2024-05-18", "2024-05-25", "2024-05-22", "2024-05-22", "2024-05-22", "2024-05-22"]
        })

        self.recipe_data = {
            "스파게티": [("파스타면", 200), ("토마토 소스", 1), ("올리브 오일", 30), ("파마산 치즈", 20)],
            "셀러드": [("양상추", 100), ("토마토", 2), ("오이", 1), ("베이비 당근", 3), ("올리브 오일", 20), ("레몬 주스", 10)],
        }

        # 레시피 목록을 표시하는 드롭다운 목록 생성
        self.recipe_combobox = ttk.Combobox(self.frame, values=list(self.recipe_data.keys()))
        self.recipe_combobox.pack()

        # "가격 및 부족한 식재료 보기" 버튼 생성
        show_recipe_cost_button = tk.Button(self.frame, text="가격 및 부족한 식재료 보기", command=self.show_recipe_cost)
        show_recipe_cost_button.pack()

    def show_recipe_cost(self):
        selected_recipe = self.recipe_combobox.get()
        cost, shortage, missing_ingredients = self.calculate_recipe_cost(selected_recipe)
        message = self.format_message(selected_recipe, cost, shortage, missing_ingredients)
        messagebox.showinfo("레시피 상세 정보", message)

    def calculate_recipe_cost(self, recipe_name):
        # 레시피 비용 계산 로직
        recipe_ingredients = self.recipe_data.get(recipe_name, [])
        total_cost = 0
        shortage = {}
        missing_ingredients = []

        for ingredient, amount in recipe_ingredients:
            ingredient_info = self.df[self.df['Name'] == ingredient]
            if ingredient_info.empty:
                missing_ingredients.append(ingredient)
            else:
                available_quantity = ingredient_info['Quantity'].iloc[0]
                if available_quantity < amount:
                    shortage[ingredient] = amount - available_quantity
                total_cost += ingredient_info['Unit Price'].iloc[0] * min(amount, available_quantity)

        return total_cost, shortage, missing_ingredients

    def format_message(self, recipe_name, cost, shortage, missing_ingredients):
        # 메시지 포맷 생성 로직
        message = f"{recipe_name}의 총 비용: {cost}원\n"
        if missing_ingredients:
            message += "등록되지 않은 식재료: " + ", ".join(missing_ingredients) + "\n"
        if shortage:
            shortage_message = "\n".join([f"{ing}: 부족량 {amt}개" for ing, amt in shortage.items()])
            message += f"부족한 식재료:\n{shortage_message}"
        return message

def initialize(frame):
    RecipeCostCalculator(frame)
