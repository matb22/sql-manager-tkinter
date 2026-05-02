import tkinter as tk
from tkinter import ttk, messagebox

from db import myDB

class TableApp:
    def __init__(self, root):
        """Создание базы данных для таблицы"""
        self.db = myDB()
        self.db._createDB()


        """Создание интерфейса"""
        self.root = root
        self.root.title("Таблица записей")
        self.root.geometry("600x400")
        
        # Создаем основную рамку
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Создаем таблицу (Treeview)
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Name", "Info"), show="headings", height=15)

        # Настраиваем заголовки
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Имя")
        self.tree.heading("Info", text="Информация")

        # Ск    рываем колонку ID (ширина 0, но она существует)
        self.tree.column("ID", width=3)
        self.tree.column("Name", width=150)
        self.tree.column("Info", width=350) 
        # Добавляем скроллбары
        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Размещаем таблицу и скроллбары
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Рамка для полей ввода
        input_frame = ttk.LabelFrame(main_frame, text="Добавление новой записи", padding="10")
        input_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Поля для ввода
        ttk.Label(input_frame, text="Имя:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.name_entry = ttk.Entry(input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Информация о записи:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.info_entry = ttk.Entry(input_frame, width=40)
        self.info_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Добавить строку", command=self.add_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить выделенную строку", command=self.delete_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить таблицу", command=self.clear_table).pack(side=tk.LEFT, padx=5)
        
        # Настраиваем вес для растягивания
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Добавляем пример данных
        self.add_sample_data()
        
        # Привязываем клавишу Enter для добавления строки
        self.root.bind('<Return>', lambda event: self.add_row())
        
    def add_row(self):
        """Функция добавления строки в таблицу"""
        name = self.name_entry.get().strip()
        info = self.info_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Предупреждение", "Поле 'Имя' не может быть пустым!")
            return
        
        # if not info:
        #     messagebox.showwarning("Предупреждение", "Поле 'Информация о записи' не может быть пустым!")
        #     return
        
        # Добавляем строку в таблицу
        self.tree.insert("", tk.END, values=(self.db.last_id+1,name, info))
        self.db.insertUser(name , info)
        # Очищаем поля ввода
        self.name_entry.delete(0, tk.END)
        self.info_entry.delete(0, tk.END)
        
        # Фокусируемся на поле "Имя" для быстрого ввода следующей записи
        self.name_entry.focus()
        
    def delete_row(self):
        """Удаление выделенной строки"""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Информация", "Выберите строку для удаления")
            return
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранную запись?"):
            for item in selected_item:
                values = self.tree.item(item, 'values')
                real_id = values[0]  
                self.db.deleteUser(int(real_id))
                self.tree.delete(item)
                
                
    
    def clear_table(self):
        """Очистка всей таблицы"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю таблицу?"):
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.db.deleteDB()
                
    
    def add_sample_data(self):
        
        
            

        # sample_data = [
        #     # ("Иван Петров", "Встреча в 15:00, проект Alpha"),
        #     # ("Мария Сидорова", "Звонок клиенту, подготовить отчет"),
        #     # ("Алексей Иванов", "Проверить документацию, отправить по почте"),
        #     # ("Елена Козлова", "Завершить разработку модуля"),
        #     # ("Дмитрий Соколов", "Техническое обслуживание сервера")
        # ]
        
        
        for user_id,name, info in self.db.all_users:
            self.tree.insert("", tk.END, values=(user_id,name, info))

if __name__ == "__main__":
    root = tk.Tk()
    TableApp(root)
    root.mainloop()