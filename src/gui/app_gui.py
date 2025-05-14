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
        self.username_entry.insert(0,"admin@test.com")

        tk.Label(self, text="Пароль:").pack(pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        self.password_entry.insert(0,"admin")
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
    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id
        self.title("Магазин")
        self.geometry("800x600")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.category_tab = self.create_category_tab(notebook)
        self.add_tab = self.create_add_product_tab(notebook)
        self.purchase_tab = self.create_purchases_tab(notebook)

        notebook.add(self.category_tab, text="📁 Категории")
        notebook.add(self.add_tab, text="➕ Добавить товар")
        notebook.add(self.purchase_tab, text="🧾 Покупки")

    def create_category_tab(self, notebook):

        frame = ttk.Frame(notebook)
        ttk.Label(frame, text="Выберите категорию:", font=("Arial", 12)).pack(pady=10)

        try:
            resp = requests.get("http://localhost:8000/categories/")
            resp.raise_for_status()
            categories = resp.json()
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить категории:\n{e}")
            categories = []

        if not categories:
            ttk.Label(frame, text="Категорий нет").pack(pady=10)
            return frame

        
        for cat in categories:
            cid  = cat["category_id"]
            name = cat["category_name"]
            
            btn = ttk.Button(
                frame,
                text=name,
                command=lambda cid=cid, name=name: self.open_category_window(cid, name)
            )
            btn.pack(fill="x", padx=50, pady=5)
        return frame

    def open_category_window(self, category_id: int, category_name: str):
        window = tk.Toplevel(self)
        window.title(f"Товары: {category_name}")
        window.geometry("800x450")

        
        cols = ("product_id", "product_name", "manufacturer_id", 
                "category_id", "date_price_change", "new_price")
        tree = ttk.Treeview(window, columns=cols, show="headings", selectmode="browse")
        headers = {
            "product_id": "ID",
            "product_name": "Название",
            "manufacturer_id": "Произв. ID",
            "category_id": "Кат. ID",
            "date_price_change": "Дата изм.",
            "new_price": "Цена"
        }
        for c in cols:
            tree.heading(c, text=headers[c])
            tree.column(c, anchor="center", stretch=True)
        tree.pack(fill="both", expand=True, padx=10, pady=(10,0))

       
        buy_btn = ttk.Button(window, text=" Купить", state="disabled",
                             command=lambda: self.on_buy(tree))
        buy_btn.pack(pady=10)

        
        def on_select(event):
            buy_btn.config(state="normal" if tree.selection() else "disabled")
        tree.bind("<<TreeviewSelect>>", on_select)

        
        try:
            resp = requests.get(f"http://localhost:8000/products/by-category/{category_id}")
            resp.raise_for_status()
            products = resp.json()
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить товары:\n{e}")
            window.destroy()
            return

       
        for p in products:
            tree.insert("", "end", values=(
                p.get("product_id"),
                p.get("product_name"),
                p.get("manufacturer_id"),
                p.get("category_id"),
                p.get("date_price_change") or "",
                p.get("new_price") or ""
            ))

    



    def get_category_id_by_name(self, category_name: str):
        # Получаем ID категории по её имени (этот запрос можно оптимизировать)
        try:
            response = requests.get("http://localhost:8000/categories/")
            response.raise_for_status()
            categories = response.json()

            for category in categories:
                if category['category_name'] == category_name:
                    return category['category_id']

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные категорий: {e}")
        return None


    def create_add_product_tab(self, notebook):
        frame = ttk.Frame(notebook)

        ttk.Label(frame, text="Название товара:").pack()
        self.name_entry = tk.Entry(frame)
        self.name_entry.pack()

        ttk.Label(frame, text="Производитель (ID):").pack()
        self.manufacturer_entry = tk.Entry(frame)
        self.manufacturer_entry.pack()

        ttk.Label(frame, text="Категория (ID):").pack()
        self.category_entry = tk.Entry(frame)
        self.category_entry.pack()

        ttk.Label(frame, text="Цена:").pack()
        self.price_entry = tk.Entry(frame)
        self.price_entry.pack()

        ttk.Button(frame, text="Добавить товар", command=self.add_product).pack(pady=10)
        return frame

    def add_product(self):
        # TODO: Отправить данные на сервер (product + price_change)
        messagebox.showinfo("Успех", "Товар добавлен (заглушка)")

    def create_purchases_tab(self, notebook):
        frame = ttk.Frame(notebook)

        self.purchase_list = ttk.Treeview(frame, columns=("id", "date", "store_id"), show="headings")
        self.purchase_list.heading("id", text="ID")
        self.purchase_list.heading("date", text="Дата")
        self.purchase_list.heading("store_id", text="ID Магазина")
        self.purchase_list.pack(fill="both", expand=True, pady=10)

        ttk.Button(frame, text="Обновить", command=self.load_purchases).pack(pady=5)
        ttk.Button(frame, text="Показать состав", command=self.show_purchase_items).pack(pady=5)
        return frame

    def load_purchases(self):
        # TODO: Загрузить покупки по user_id
        self.purchase_list.delete(*self.purchase_list.get_children())
        sample_data = [(1, "2025-05-01 10:00", 3), (2, "2025-05-02 12:30", 2)]
        for item in sample_data:
            self.purchase_list.insert("", "end", values=item)

    def show_purchase_items(self):
        selected = self.purchase_list.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Сначала выберите покупку.")
            return
        purchase_id = self.purchase_list.item(selected[0])["values"][0]

        window = tk.Toplevel(self)
        window.title(f"Состав покупки {purchase_id}")
        window.geometry("600x300")

        tree = ttk.Treeview(window, columns=("product_id", "count", "price"), show="headings")
        tree.heading("product_id", text="ID Товара")
        tree.heading("count", text="Кол-во")
        tree.heading("price", text="Цена за ед.")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # TODO: Запрос на /purchases/{id}/items
        sample_items = [(1, 2, 1200.0), (3, 1, 500.0)]
        for item in sample_items:
            tree.insert("", "end", values=item)

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()