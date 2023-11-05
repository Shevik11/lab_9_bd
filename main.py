import tkinter as tk
import mysql.connector
from tkinter import messagebox
import csv

def connect_to_mysql():
    # Параметри підключення до MySQL бази даних
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="904496Vfrc",
        database="new_ayction",
        autocommit=True
    )
    try:

        cursor = db_connection.cursor() # Створення курсора(об'єкта) для роботи з базою даних

        # Отримання списку таблиць у базі даних
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()] # Отримуємо список таблиць, fetchall() - повертає усі

        return db_connection, tables 
    except mysql.connector.Error as err:
        print(f"Помилка при підключенні до бази даних: {err}")
        return None, []
    
def show_tables():
    connection, tables = connect_to_mysql()
    if not connection:
        return

    root = tk.Tk()
    root.title("Таблиці в MySQL базі даних")
    root.geometry("600x400")  # Збільшення розмірів вікна

    table_text = tk.Text(root, wrap=tk.WORD, bg="black", fg="white")
    table_text.pack(fill="both", expand=True)
    table_text.config(state=tk.NORMAL)

    table_text.tag_configure("custom_tag", foreground="white", background="black")

    for table in tables:
        table_text.insert(tk.END, table + "\n", "custom_tag")

    table_text.config(state=tk.DISABLED)

    connection.close()

    root.mainloop()
# Збереження результату у CSV-файл
def save_to_csv_file(cursor, result):
    with open("query_result.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        # Записуємо заголовки (назви стовпців)
        csv_writer.writerow([i[0] for i in cursor.description])
        # Записуємо дані
        for row in result:
            csv_writer.writerow(row)
        print("Результати збережено у query_result.csv")

def func1():
    def save_command_and_execute_query():
        command = command_entry.get()
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="904496Vfrc",
                database="new_ayction"
            )
            cursor = db_connection.cursor()
            cursor.execute(command)

            result_window = tk.Tk()
            result_window.title("Результати запиту")

            column_names = [column[0] for column in cursor.description]
            results = cursor.fetchall()

            for i, column_name in enumerate(column_names):
                label = tk.Label(result_window, text=column_name)
                label.grid(row=0, column=i)

            for row_index, row in enumerate(results):
                for column_index, value in enumerate(row):
                    label = tk.Label(result_window, text=value)
                    label.grid(row=row_index + 1, column=column_index)

            # Add a Save to CSV button
            save_csv_button = tk.Button(result_window, text="Зберегти в CSV", command=lambda: save_to_csv_file(cursor, results))
            save_csv_button.grid(row=row_index + 2, column=0, columnspan=len(column_names))

            cursor.close()
            db_connection.close()
            result_window.mainloop()

        except mysql.connector.Error as error:
            error_label = tk.Label(result_window, text=f"Помилка при виконанні запиту: {error}")
            error_label.grid(row=0, column=0)

    def close_window():
        command_window.destroy()

    command_window = tk.Tk()
    command_window.title("Введення команди")
    command_window.geometry("400x200") 

    command_label = tk.Label(command_window, text="Введіть команду:", font=("Arial", 14))
    command_label.pack()

    command_entry = tk.Entry(command_window, font=("Arial", 14))
    command_entry.pack()

    save_button = tk.Button(command_window, text="Зберегти і виконати", command=lambda: save_command_and_execute_query(), font=("Arial", 14))
    save_button.pack()

    exit_button = tk.Button(command_window, text="Вийти", command=close_window, font=("Arial", 14))
    exit_button.pack()

    command_window.mainloop()

def save_command_and_execute_query():
    global command_entry

    command = command_entry.get()
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="904496Vfrc",
            database="new_ayction",
            autocommit=True
        )
        cursor = db_connection.cursor()
        cursor.execute(command)

        messagebox.showinfo("Успішно", "Запит успішно виконано!")

        cursor.close()
        db_connection.close()
    except mysql.connector.Error as error:
        messagebox.showerror("Помилка", f"Помилка при виконанні запиту: {error}")

def close_window():
    command_window.destroy()

def func2():
    global command_entry, command_window

    command_window = tk.Tk()
    command_window.title("Введення команди")
    command_window.geometry("400x200")

    command_label = tk.Label(command_window, text="Введіть команду:", font=("Arial", 14))
    command_label.pack()

    command_entry = tk.Entry(command_window, font=("Arial", 14))
    command_entry.pack()

    save_button = tk.Button(command_window, text="Зберегти і виконати", command=save_command_and_execute_query, font=("Arial", 14))
    save_button.pack()

    exit_button = tk.Button(command_window, text="Вийти", command=close_window, font=("Arial", 14))
    exit_button.pack()

    command_window.mainloop()
def create_new_window_yes():
        new_window = tk.Toplevel()  # Створення нового вікна

        new_window.title("Нове вікно")  # Встановлення заголовку для нового вікна
        new_window.geometry("400x300")  # Збільшення розмірів вікна

        # Додавання тексту над кнопками
        label = tk.Label(new_window, text="Це нове вікно")
        label.pack()

        # Додавання кнопок з відповідними функціями
        button3 = tk.Button(new_window, text="Запит з виведенням", command=func1, width=20, height=2)
        button4 = tk.Button(new_window, text="Запит з оновленням/\nвставленням/\nвидаленням даних", command=func2, width=20, height=2)

        button3.pack(pady = 1)
        button4.pack(pady = 1)


def main():
    # Виклик функції connect_to_mysql при запуску програми
    connection = connect_to_mysql()

    if not connection:
        return

    root = tk.Tk()
    root.title("Графічний інтерфейс")
    root.geometry("600x400")  # Встановлення розмірів вікна

    label = tk.Label(root, text="Бажаєте ввести запит?")
    label.pack()

    # Збільшення розміру шрифту тексту
    font = ("Arial", 12)

    frame = tk.Frame(root)
    frame.pack()

    button_width = 20  # Збільшення розміру кнопок
    padx_between_buttons = 10  # Відстань між кнопками

    table_button = tk.Button(frame, text="Вивести список таблиць", command=show_tables, font=font, width=button_width)
    yes_button = tk.Button(frame, text="Так", command=create_new_window_yes, font=font, width=button_width)
    no_button = tk.Button(frame, text="Ні", command=root.quit, font=font, width=button_width)

    table_button.grid(row=1, column=0, padx=padx_between_buttons)
    yes_button.grid(row=0, column=0)
    no_button.grid(row=0, column=1)

    root.mainloop()

if __name__ == "__main__":
    main()