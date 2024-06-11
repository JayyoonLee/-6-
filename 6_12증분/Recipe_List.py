import json
import os
import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Listbox, messagebox
import Recipe_Cost  # Recipe_Cost 모듈 import

# JSON 파일 경로
JSON_FILE_PATH = "recipes.json"

# JSON 파일이 있으면 로드하고, 없으면 빈 딕셔너리 생성
if os.path.exists(JSON_FILE_PATH):
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        recipes = json.load(file)
else:
    recipes = {}

def save_to_json():
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(recipes, file, ensure_ascii=False, indent=4)
    print(f"Saved recipes to {JSON_FILE_PATH}")
    Recipe_Cost.update_recipe_data()  # Recipe_Cost 모듈의 update_recipe_data 함수 호출

def apply_styles(widget, font=("Helvetica", 14), bg=None, fg="white"):
    widget.config(font=font, bg=bg, fg=fg, relief="solid")

def initialize(frame):
    frame.config(bg="#f0f0f0")

    def add_recipe():
        add_window = Toplevel(frame)
        add_window.title("레시피 추가")
        add_window.config(bg="#f0f0f0")

        Label(add_window, text="레시피 이름:", bg="#f0f0f0").grid(row=0, column=0)
        name_entry = Entry(add_window)
        name_entry.grid(row=0, column=1)

        ingredients = {}

        def add_ingredient():
            ingredient_window = Toplevel(add_window)
            ingredient_window.title("재료 추가")
            ingredient_window.config(bg="#f0f0f0")

            Label(ingredient_window, text="재료 이름:", bg="#f0f0f0").grid(row=0, column=0)
            ingredient_name_entry = Entry(ingredient_window)
            ingredient_name_entry.grid(row=0, column=1)

            Label(ingredient_window, text="양:", bg="#f0f0f0").grid(row=1, column=0)
            ingredient_amount_entry = Entry(ingredient_window)
            ingredient_amount_entry.grid(row=1, column=1)

            def confirm_ingredient():
                name = ingredient_name_entry.get()
                amount = ingredient_amount_entry.get()
                if name and amount:
                    ingredients[name] = amount
                    messagebox.showinfo("재료 추가 완료", f"{name} {amount}이(가) 추가되었습니다.")
                    ingredient_window.destroy()
                else:
                    messagebox.showerror("입력 오류", "재료 이름과 양을 입력해주세요.")

            confirm_button = Button(ingredient_window, text="확인", command=confirm_ingredient)
            apply_styles(confirm_button, bg="#4caf50")
            confirm_button.grid(row=2, columnspan=2, pady=10)

        add_ingredient_button = Button(add_window, text="재료 추가", command=add_ingredient)
        apply_styles(add_ingredient_button, bg="#2196f3")
        add_ingredient_button.grid(row=1, columnspan=2, pady=10)

        def confirm_recipe():
            name = name_entry.get()
            if name and ingredients:
                recipes[name] = ingredients
                save_to_json()
                messagebox.showinfo("레시피 추가 완료", f"{name} 레시피가 추가되었습니다.")
                add_window.destroy()
            else:
                messagebox.showerror("입력 오류", "레시피 이름과 최소 한 가지 재료를 입력해주세요.")

        confirm_button = Button(add_window, text="레시피 추가", command=confirm_recipe)
        apply_styles(confirm_button, bg="#4caf50")
        confirm_button.grid(row=2, columnspan=2, pady=10)

    def view_recipes():
        recipes_window = Toplevel(frame)
        recipes_window.title("레시피 목록")
        recipes_window.config(bg="#f0f0f0")
        listbox = Listbox(recipes_window)
        listbox.pack(fill=tk.BOTH, expand=True)

        for recipe in recipes:
            listbox.insert(tk.END, recipe)

        def show_details(event):
            index = listbox.curselection()
            if index:
                selected_recipe = listbox.get(index[0])
                detail_window = Toplevel(recipes_window)
                detail_window.title(f"{selected_recipe} 세부 정보")
                detail_window.config(bg="#f0f0f0")
                details = recipes[selected_recipe]
                details_text = '\n'.join(f"{ingredient}: {amount}" for ingredient, amount in details.items())
                Label(detail_window, text=details_text, bg="#f0f0f0").pack()

        listbox.bind('<<ListboxSelect>>', show_details)

    def update_recipe():
        update_window = Toplevel(frame)
        update_window.title("레시피 수정")
        update_window.config(bg="#f0f0f0")

        listbox = Listbox(update_window)
        listbox.pack(fill=tk.BOTH, expand=True)

        for recipe in recipes:
            listbox.insert(tk.END, recipe)

        def on_select(event):
            selected_index = listbox.curselection()
            if not selected_index:
                return

            selected_recipe = listbox.get(selected_index[0])
            ingredients = recipes[selected_recipe]

            edit_window = Toplevel(update_window)
            edit_window.title(f"{selected_recipe} 수정")
            edit_window.config(bg="#f0f0f0")

            ingredient_entries = {}

            for i, (ingredient, amount) in enumerate(ingredients.items()):
                Label(edit_window, text=f"{ingredient}:", bg="#f0f0f0").grid(row=i, column=0)
                entry = Entry(edit_window)
                entry.insert(0, amount)
                entry.grid(row=i, column=1)
                ingredient_entries[ingredient] = entry

            def confirm():
                for ingredient, entry in ingredient_entries.items():
                    recipes[selected_recipe][ingredient] = entry.get()
                save_to_json()
                messagebox.showinfo("레시피 수정", f"{selected_recipe} 레시피가 수정되었습니다.")
                edit_window.destroy()
                update_window.destroy()

            confirm_button = Button(edit_window, text="수정", command=confirm)
            apply_styles(confirm_button, bg="#2196f3")
            confirm_button.grid(row=len(ingredients), columnspan=2, pady=10)

        listbox.bind('<<ListboxSelect>>', on_select)

    def delete_recipe():
        delete_window = Toplevel(frame)
        delete_window.title("레시피 삭제")
        delete_window.config(bg="#f0f0f0")

        listbox = Listbox(delete_window)
        listbox.pack(fill=tk.BOTH, expand=True)

        for recipe in recipes:
            listbox.insert(tk.END, recipe)

        def confirm_delete():
            selected_index = listbox.curselection()
            if selected_index:
                selected_recipe = listbox.get(selected_index[0])
                messagebox.showinfo("레시피 삭제", f"'{selected_recipe}' 레시피가 삭제되었습니다.")
                delete_window.destroy()
                del recipes[selected_recipe]
                save_to_json()

            else:
                messagebox.showerror("오류", "삭제할 레시피를 선택해주세요.")

        delete_button = Button(delete_window, text="삭제", command=confirm_delete)
        apply_styles(delete_button, bg="#f44336")
        delete_button.pack(pady=10)

    buttons = [
        ("레시피 추가", add_recipe, "#4caf50"),
        ("레시피 보기", view_recipes, "#2196f3"),
        ("레시피 수정", update_recipe, "#ff9800"),
        ("레시피 삭제", delete_recipe, "#f44336")
    ]

    for text, command, color in buttons:
        btn = Button(frame, text=text, command=command)
        apply_styles(btn, bg=color)
        btn.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("레시피 관리 프로그램")
    root.geometry("2000x1000")
    root.config(bg="#f0f0f0")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    initialize(main_frame)

    root.mainloop()
