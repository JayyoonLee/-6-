import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

def show_calendar():
    root = tk.Tk()
    root.title("Calendar")

    # 현재 날짜 가져오기
    today = datetime.today()

    # 현재 날짜를 기준으로 달력 설정
    calendar = Calendar(root, selectmode='day', year=today.year, month=today.month, day=today.day, showweeknumbers=False)
    calendar.pack(pady=20)

    def grab_date():
        selected_date = calendar.get_date()
        date_label.config(text="Selected Date is: " + selected_date)

    grab_date_button = tk.Button(root, text="Get Date", command=grab_date)
    grab_date_button.pack(pady=10)

    date_label = tk.Label(root, text="")
    date_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    show_calendar()

