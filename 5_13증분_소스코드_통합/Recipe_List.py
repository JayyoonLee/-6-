import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Listbox, messagebox, simpledialog

# 예시 레시피 데이터베이스
recipes = {
    'Apple Pie': {'Apples': 3, 'Sugar': '100g', 'Flour': '200g'},
    'Banana Bread': {'Bananas': 2, 'Flour': '150g', 'Eggs': 2}
}

def initialize(frame):
    # 레시피 추가 함수
    def add_recipe():
        add_window = Toplevel(frame)
        add_window.title("레시피 추가")

        Label(add_window, text="레시피 이름:").grid(row=0, column=0)
        Label(add_window, text="재료 (형식: 재료=양):").grid(row=1, column=0)
        name_entry = Entry(add_window)
        ingredients_entry = Entry(add_window)
        name_entry.grid(row=0, column=1)
        ingredients_entry.grid(row=1, column=1)

        def submit():
            name = name_entry.get()
            ingredients = ingredients_entry.get()
            if name not in recipes:
                recipes[name] = dict(item.split('=') for item in ingredients.split(','))
                messagebox.showinfo("레시피 추가", f"{name} 레시피가 추가되었습니다.")
            else:
                messagebox.showerror("오류", "해당 레시피가 이미 존재합니다.")
            add_window.destroy()

        Button(add_window, text="추가", command=submit).grid(row=2, columnspan=2)

    # 레시피 보기 함수
    def view_recipes():
        recipes_window = Toplevel(frame)
        recipes_window.title("레시피 목록")
        listbox = Listbox(recipes_window)
        listbox.pack()

        for recipe in recipes:
            listbox.insert(tk.END, recipe)

        def show_details(event):
            # 선택된 항목의 인덱스를 가져옵니다.
            index = listbox.curselection()
            if index:
                selected_recipe = listbox.get(index)
                detail_window = Toplevel(recipes_window)
                detail_window.title(f"{selected_recipe} 세부 정보")

            # 세부 정보를 보여줄 라벨 추가
                details = recipes[selected_recipe]
                details_text = '\n'.join(f"{ingredient}: {amount}" for ingredient, amount in details.items())
                Label(detail_window, text=details_text).pack()

        # Listbox 선택 이벤트에 함수 바인딩
        listbox.bind('<<ListboxSelect>>', show_details)


    # 레시피 수정 함수
    def update_recipe():
        name = simpledialog.askstring("레시피 수정", "수정할 레시피 이름 입력:")
        if name in recipes:
            update_window = Toplevel(frame)
            update_window.title("레시피 수정")
            Label(update_window, text="새 재료 (형식: 재료=양):").grid(row=0, column=0)
            ingredients_entry = Entry(update_window)
            ingredients_entry.grid(row=0, column=1)

            def submit():
                ingredients = ingredients_entry.get()
                recipes[name] = dict(item.split('=') for item in ingredients.split(','))
                messagebox.showinfo("레시피 수정", f"{name} 레시피가 수정되었습니다.")
                update_window.destroy()

            Button(update_window, text="수정", command=submit).grid(row=1, columnspan=2)
        else:
            messagebox.showerror("오류", "레시피를 찾을 수 없습니다.")

    # 레시피 삭제 함수
    def delete_recipe():
        name = simpledialog.askstring("레시피 삭제", "삭제할 레시피 이름 입력:")
        if name in recipes:
            del recipes[name]
            messagebox.showinfo("레시피 삭제", f"{name} 레시피가 삭제되었습니다.")
        else:
            messagebox.showerror("오류", f"{name} 레시피를 찾을 수 없습니다.")

    # 각 기능에 대한 버튼 추가
    Button(frame, text="레시피 추가", command=add_recipe).pack(pady=5)
    Button(frame, text="레시피 보기", command=view_recipes).pack(pady=5)
    Button(frame, text="레시피 수정", command=update_recipe).pack(pady=5)
    Button(frame, text="레시피 삭제", command=delete_recipe).pack(pady=5)
