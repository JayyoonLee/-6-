import tkinter as tk
from tkinter import messagebox, Toplevel, Listbox
import pandas as pd
from datetime import datetime
import os

class PantryManagement:
    def __init__(self, csv_file_path="Ingredients.csv"):
        self.csv_file_path = csv_file_path
        if os.path.exists(self.csv_file_path):
            self.df = pd.read_csv(self.csv_file_path)
        else:
            self.df = pd.DataFrame(columns=["Name", "Quantity", "Unit Price", "Location", "Expiration Date"])

    def save_to_csv(self):
        self.df.to_csv(self.csv_file_path, index=False)
        print(f"Saved dataframe to {self.csv_file_path}")

    def check_expiration(self):
        try:
            self.df["Expiration Date"] = pd.to_datetime(self.df["Expiration Date"], format="%Y-%m-%d", errors='coerce')
        except Exception as e:
            messagebox.showerror("날짜 형식 오류", f"날짜 변환 중 오류가 발생했습니다: {e}")
            return

        today = pd.to_datetime(datetime.today().strftime("%Y-%m-%d"))

        expired_ingredients = self.df[self.df["Expiration Date"] < today]
        if not expired_ingredients.empty:
            expired_items = expired_ingredients["Name"].tolist()
            self.df = self.df.drop(expired_ingredients.index)
            self.save_to_csv()
            messagebox.showinfo("유통기한 알림", f"유통기한이 만료된 식재료가 삭제되었습니다: {', '.join(expired_items)}")
        else:
            messagebox.showinfo("유통기한 알림", "현재 유통기한이 만료된 식재료가 없습니다.")

    def add_ingredient(self, frame):
        input_frame = Toplevel(frame)
        input_frame.title("식재료 추가")
        input_frame.config(bg="#f0f0f0")

        labels_texts = ["종류:", "수량:", "개당 가격:", "위치:", "유통기한 (YYYY-MM-DD):"]
        entries = {}

        for i, text in enumerate(labels_texts):
            tk.Label(input_frame, text=text, font=("Helvetica", 14), bg="#f0f0f0").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(input_frame, font=("Helvetica", 14))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[text.split(":")[0]] = entry

        def confirm():
            data = {desc: entry.get() for desc, entry in entries.items()}

            for key, value in data.items():
                if not value:
                    messagebox.showerror("입력 오류", f"{key} 필드를 입력해주세요.")
                    return

            if "유통기한 (YYYY-MM-DD)" in data:
                try:
                    expiration_date = pd.to_datetime(data["유통기한 (YYYY-MM-DD)"], format="%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("날짜 형식 오류", "유통기한 형식이 잘못되었습니다. (올바른 형식: YYYY-MM-DD)")
                    return

                if expiration_date < pd.to_datetime(datetime.today().strftime("%Y-%m-%d")):
                    messagebox.showerror("유통기한 만료", f"{data['종류']}의 유통기한이 이미 만료되었습니다.")
                    return
            else:
                messagebox.showerror("입력 오류", "유통기한 필드를 입력해주세요.")
                return

            self.df.loc[len(self.df)] = data.values()
            self.save_to_csv()
            messagebox.showinfo("추가 완료", f"{data['종류']}이(가) 추가되었습니다.")
            input_frame.destroy()

        confirm_button = tk.Button(input_frame, text="확인", command=confirm)
        self.apply_styles(confirm_button, font=("Helvetica", 14), bg="#4caf50")
        confirm_button.grid(row=5, columnspan=2, pady=10)

    def apply_styles(self, widget, font=("Helvetica", 14), bg=None, fg="white", width=20, height=2):
            widget.config(font=font, bg=bg, fg=fg, relief="solid", width=width, height=height)

    def initialize(self, frame):
            for widget in frame.winfo_children():
                widget.destroy()
            
            frame.config(bg="#f0f0f0")

            button_width = 20  # 버튼 너비 설정
            button_height = 2  # 버튼 높이 설정

            add_button = tk.Button(frame, text="추가", command=lambda: self.add_ingredient(frame), width=button_width, height=button_height)
            self.apply_styles(add_button, font=("Helvetica", 14), bg="#4caf50")
            add_button.pack(pady=5, padx=10)

            show_button = tk.Button(frame, text="목록 보기", command=self.show_ingredients, width=button_width, height=button_height)
            self.apply_styles(show_button, font=("Helvetica", 14), bg="#2196f3")
            show_button.pack(pady=5, padx=10)

            update_button = tk.Button(frame, text="수정", command=lambda: self.update_ingredient(frame), width=button_width, height=button_height)
            self.apply_styles(update_button, font=("Helvetica", 14), bg="#6495ed")
            update_button.pack(pady=5, padx=10)

            delete_button = tk.Button(frame, text="삭제", command=lambda: self.delete_ingredient(frame), width=button_width, height=button_height)
            self.apply_styles(delete_button, font=("Helvetica", 14), bg="#ff9800")
            delete_button.pack(pady=5, padx=10)

            check_button = tk.Button(frame, text="유통기한 만료 확인", command=self.check_expiration, width=button_width, height=button_height)
            self.apply_styles(check_button, font=("Helvetica", 14), bg="#f44336")
            check_button.pack(pady=5, padx=10)
            
    def show_ingredients(self):
        self.df = pd.read_csv(self.csv_file_path)
        messagebox.showinfo("식재료 목록", self.df.to_string(index=False))

    def update_ingredient(self, frame):
        update_frame = Toplevel(frame)
        update_frame.title("식재료 수정")
        update_frame.config(bg="#f0f0f0")

        listbox = Listbox(update_frame, font=("Helvetica", 14))
        listbox.pack(fill=tk.BOTH, expand=True)

        for name in self.df["Name"].values:
            listbox.insert(tk.END, name)

        def on_select(event):
            selected_index = listbox.curselection()
            if not selected_index:
                return

            selected_name = listbox.get(selected_index)
            ingredient_data = self.df[self.df["Name"] == selected_name].iloc[0]

            edit_frame = Toplevel(update_frame)
            edit_frame.title(f"{selected_name} 수정")
            edit_frame.config(bg="#f0f0f0")

            columns = ["Quantity", "Unit Price", "Location", "Expiration Date"]
            labels_texts = ["수량:", "개당 가격:", "위치:", "유통기한 (YYYY-MM-DD):"]
            entries = {}

            for i, (col, text) in enumerate(zip(columns, labels_texts)):
                tk.Label(edit_frame, text=text, font=("Helvetica", 14), bg="#f0f0f0").grid(row=i, column=0, padx=5, pady=5)
                entry = tk.Entry(edit_frame, font=("Helvetica", 14))
                entry.insert(0, ingredient_data[col])
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries[col] = entry

            def confirm():
                for col, entry in entries.items():
                    value = entry.get()
                    if value:
                        self.df.loc[self.df["Name"] == selected_name, col] = value
                self.save_to_csv()
                messagebox.showinfo("수정 완료", f"{selected_name}의 정보가 수정되었습니다.")
                edit_frame.destroy()

            confirm_button = tk.Button(edit_frame, text="확인", command=confirm)
            self.apply_styles(confirm_button, font=("Helvetica", 14), bg="#4caf50")
            confirm_button.grid(row=5, columnspan=2, pady=10)

        listbox.bind('<<ListboxSelect>>', on_select)

    def delete_ingredient(self, frame):
        input_frame = Toplevel(frame)
        input_frame.title("식재료 삭제")
        input_frame.config(bg="#f0f0f0")

        tk.Label(input_frame, text="식재료 명:", font=("Helvetica", 14), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(input_frame, font=("Helvetica", 14))
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        def confirm():
            name = name_entry.get()
            if name in self.df["Name"].values:
                self.df = self.df[self.df["Name"] != name]
                self.save_to_csv()
                messagebox.showinfo("성공", f"{name}이(가) 삭제되었습니다!")
            else:
                messagebox.showerror("오류", f"{name}을(를) 찾을 수 없습니다!")
            input_frame.destroy()

        confirm_button = tk.Button(input_frame, text="확인", command=confirm)
        self.apply_styles(confirm_button, font=("Helvetica", 14), bg="#f44336")
        confirm_button.grid(row=1, columnspan=2, pady=10)

# tkinter 초기화 및 메인 루프 설정
if __name__ == "__main__":
    root = tk.Tk()
    root.title("식재료 관리 프로그램")
    root.geometry("800x600")
    root.config(bg="#f0f0f0")

    pantry_management = PantryManagement()
    
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    pantry_management.initialize(main_frame)

    root.mainloop()
