import tkinter as tk
from tkinter import ttk, messagebox
import requests


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Авторизация")
        self.geometry("720x400")

        tk.Label(self, text="Логин:").pack(pady=(40, 10))
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Пароль:").pack(pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Войти", command=self.login).pack(pady=30)

    def login(self):
        email = self.username_entry.get()
        password = self.password_entry.get()

        try:
            response = requests.post("http://localhost:8000/auth/login", json={
                "email": email,
                "password": password
            })

            if response.status_code == 200:
                data = response.json()
                user_id = data["user_id"]
                self.destroy()
                app = StoreApp(user_id=user_id)
                app.mainloop()
            else:
                messagebox.showerror("Ошибка", response.json().get("detail", "Ошибка авторизации"))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Сервер недоступен:\n{e}")




class StoreApp(tk.Tk):
    def __init__(self,user_id: int):
        super().__init__()
        self.user_id = user_id

        self.title("Магазин")
        self.geometry("700x500")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.view_tab = self.create_view_products_tab(notebook)
        self.add_tab = self.create_add_product_tab(notebook)
        self.buy_tab = self.create_buy_product_tab(notebook)

        notebook.add(self.view_tab, text="📦 Товары")
        notebook.add(self.add_tab, text="➕ Добавить")
        notebook.add(self.buy_tab, text="🛒 Купить")

    def create_view_products_tab(self, notebook):
        frame = ttk.Frame(notebook)

        self.products_list = ttk.Treeview(frame, columns=("id", "name", "price", "stock"), show="headings")
        self.products_list.heading("id", text="ID")
        self.products_list.heading("name", text="Название")
        self.products_list.heading("price", text="Цена")
        self.products_list.heading("stock", text="Остаток")
        self.products_list.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Обновить", command=self.load_products).pack(pady=5)
        return frame

    def create_add_product_tab(self, notebook):
        frame = ttk.Frame(notebook)

        tk.Label(frame, text="Название товара:").pack(pady=5)
        self.name_entry = tk.Entry(frame)
        self.name_entry.pack()

        tk.Label(frame, text="Цена:").pack(pady=5)
        self.price_entry = tk.Entry(frame)
        self.price_entry.pack()

        tk.Label(frame, text="Количество:").pack(pady=5)
        self.stock_entry = tk.Entry(frame)
        self.stock_entry.pack()

        ttk.Button(frame, text="Добавить товар", command=self.add_product).pack(pady=10)
        return frame

    def create_buy_product_tab(self, notebook):
        frame = ttk.Frame(notebook)

        tk.Label(frame, text="ID товара:").pack(pady=5)
        self.buy_id_entry = tk.Entry(frame)
        self.buy_id_entry.pack()

        tk.Label(frame, text="Количество:").pack(pady=5)
        self.buy_qty_entry = tk.Entry(frame)
        self.buy_qty_entry.pack()

        ttk.Button(frame, text="Купить", command=self.buy_product).pack(pady=10)
        return frame

    # Логики нет 

    def load_products(self):
        # Тут можно заглушка для запроса API 
        self.products_list.delete(*self.products_list.get_children())
        sample_data = [(1, "Телефон", 999.99, 10), (2, "Ноутбук", 1499.50, 5)]
        for item in sample_data:
            self.products_list.insert("", "end", values=item)

    def add_product(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()
        messagebox.showinfo("Добавление", f"Товар '{name}' добавлен. (Заглушка)")

    def buy_product(self):
        product_id = self.buy_id_entry.get()
        qty = self.buy_qty_entry.get()
        messagebox.showinfo("Покупка", f"Куплено {qty} шт. товара с ID {product_id}. (Заглушка)")

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()