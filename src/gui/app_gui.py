import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

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
            response = requests.post(
                "http://localhost:8000/auth/login",
                json={"email": email, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                user_id = data["user_id"]
                self.destroy()
                app = StoreApp(user_id=user_id)
                app.mainloop()
            else:
                error_data = response.json()
                messagebox.showerror("Ошибка", error_data.get("detail", "Ошибка авторизации"))
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Сервер недоступен:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неизвестная ошибка:\n{str(e)}")

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
            cid = cat["category_id"]
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
        window.geometry("800x500")

        products_frame = ttk.Frame(window)
        products_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        cols = ("product_id", "product_name", "manufacturer", 
                "category", "date_price_change", "new_price")
        tree = ttk.Treeview(products_frame, columns=cols, show="headings", selectmode="extended")
        headers = {
            "product_id": "ID",
            "product_name": "Название",
            "manufacturer": "Производитель",
            "category": "Категория",
            "date_price_change": "Дата изм.",
            "new_price": "Цена"
        }
        for c in cols:
            tree.heading(c, text=headers[c])
            tree.column(c, anchor="center", stretch=True)

        scrollbar = ttk.Scrollbar(products_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        
        control_frame = ttk.Frame(window)
        control_frame.pack(fill="x", padx=10, pady=5)

        
        edit_btn = ttk.Button(control_frame, text="Редактировать",
                            command=lambda: self.edit_product(tree, window, category_id))
        edit_btn.pack(side="left", padx=5)

        delete_btn = ttk.Button(control_frame, text="Удалить",
                             command=lambda: self.delete_product(tree, category_id))
        delete_btn.pack(side="left", padx=5)

        
        info_frame = ttk.Frame(window)
        info_frame.pack(fill="x", padx=10, pady=5)

        total_label = ttk.Label(info_frame, text="Общая сумма: 0.00")
        total_label.pack(side="left", padx=5)

        buy_btn = ttk.Button(info_frame, text="Купить выбранные", state="disabled",
                          command=lambda: self.process_purchase(tree))
        buy_btn.pack(side="right", padx=5)

        def update_buttons(event=None):
            selected_items = tree.selection()
            total = sum(float(tree.item(item)["values"][5]) for item in selected_items)
            total_label.config(text=f"Общая сумма: {total:.2f}")
            buy_btn.config(state="normal" if selected_items else "disabled")
            
            
            if len(selected_items) == 1:
                edit_btn.config(state="normal")
                delete_btn.config(state="normal")
            else:
                edit_btn.config(state="disabled")
                delete_btn.config(state="disabled")

        tree.bind("<<TreeviewSelect>>", update_buttons)

        try:
            
            manufacturers_response = requests.get("http://localhost:8000/manufacturers/")
            manufacturers = {m["manufacturer_id"]: m["manufacturer_name"] 
                           for m in manufacturers_response.json()}

            
            categories_response = requests.get("http://localhost:8000/categories/")
            categories = {c["category_id"]: c["category_name"] 
                         for c in categories_response.json()}

            
            resp = requests.get(f"http://localhost:8000/products/by-category/{category_id}")
            resp.raise_for_status()
            products = resp.json()

            for p in products:
                tree.insert("", "end", values=(
                    p.get("product_id"),
                    p.get("product_name"),
                    manufacturers.get(p.get("manufacturer_id"), f"Производитель {p.get('manufacturer_id')}"),
                    categories.get(p.get("category_id"), f"Категория {p.get('category_id')}"),
                    p.get("date_price_change") or "",
                    p.get("new_price") or ""
                ))

        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные:\n{e}")
            window.destroy()
            return

        
        edit_btn.config(state="disabled")
        delete_btn.config(state="disabled")

    def edit_product(self, tree, parent_window, category_id):
        selected_items = tree.selection()
        if not selected_items:
            return
            
        item = tree.item(selected_items[0])
        values = item["values"]
        
        edit_window = tk.Toplevel(parent_window)
        edit_window.title("Редактировать товар")
        edit_window.geometry("400x300")
        
        ttk.Label(edit_window, text="Название товара:").pack(pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.insert(0, values[1])
        name_entry.pack(pady=5)
        
        ttk.Label(edit_window, text="Производитель (ID):").pack(pady=5)
        manufacturer_entry = ttk.Entry(edit_window)
        manufacturer_entry.insert(0, values[2])
        manufacturer_entry.pack(pady=5)
        
        ttk.Label(edit_window, text="Цена:").pack(pady=5)
        price_entry = ttk.Entry(edit_window)
        price_entry.insert(0, values[5])
        price_entry.pack(pady=5)
        
        def save_changes():
            try:
                product_data = {
                    "product_name": name_entry.get().strip(),
                    "manufacturer_id": int(manufacturer_entry.get().strip()),
                    "category_id": category_id,
                    "new_price": float(price_entry.get().strip()),
                    "date_price_change": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                response = requests.put(
                    f"http://localhost:8000/products/{values[0]}",
                    json=product_data
                )
                
                if response.status_code == 200:
                    messagebox.showinfo("Успех", "Товар успешно обновлен")
                    edit_window.destroy()
                    
                    tree.item(selected_items[0], values=(
                        values[0],
                        product_data["product_name"],
                        product_data["manufacturer_id"],
                        product_data["category_id"],
                        product_data["date_price_change"],
                        product_data["new_price"]
                    ))
                else:
                    messagebox.showerror("Ошибка", response.json().get("detail", "Неизвестная ошибка"))
                    
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте правильность введенных данных")
            except requests.RequestException as e:
                messagebox.showerror("Ошибка", f"Ошибка при обновлении товара:\n{e}")
        
        ttk.Button(edit_window, text="Сохранить", command=save_changes).pack(pady=20)
        ttk.Button(edit_window, text="Отмена", command=edit_window.destroy).pack()

    def delete_product(self, tree, category_id):
        selected_items = tree.selection()
        if not selected_items:
            return
            
        item = tree.item(selected_items[0])
        product_id = item["values"][0]
        
        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот товар?"):
            return
            
        try:
            response = requests.delete(f"http://localhost:8000/products/{product_id}")
            
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Товар успешно удален")
                tree.delete(selected_items[0])
            else:
                messagebox.showerror("Ошибка", response.json().get("detail", "Неизвестная ошибка"))
                
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении товара:\n{e}")

    def process_purchase(self, tree):
        selected_items = tree.selection()
        if not selected_items:
            return

        products = []
        total_sum = 0
        for item in selected_items:
            values = tree.item(item)["values"]
            products.append({
                "product_id": int(values[0]),
                "product_name": str(values[1]),
                "price": float(values[5])
            })
            total_sum += float(values[5])

        if not messagebox.askyesno("Подтверждение", 
                                f"Вы хотите купить {len(products)} товаров на сумму {total_sum:.2f}?"):
            return

        try:
            response = requests.post(
                "http://localhost:8000/purchases/",
                json={
                    "customer_id": self.user_id,
                    "store_id": 1,
                    "products": products
                }
            )
            
            if response.status_code == 200:
                
                for item in selected_items:
                    tree.delete(item)
                messagebox.showinfo("Успех", "Покупка успешно оформлена!")
                self.load_purchases()  
            else:
                error_detail = response.json().get("detail", "Неизвестная ошибка")
                messagebox.showerror("Ошибка", f"Ошибка при оформлении покупки: {error_detail}")

        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка при оформлении покупки:\n{e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неизвестная ошибка:\n{e}")

    def get_category_id_by_name(self, category_name: str):
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
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Название товара:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = ttk.Entry(frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame, text="Производитель (ID):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.manufacturer_entry = ttk.Entry(frame)
        self.manufacturer_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame, text="Категория:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.category_combo = ttk.Combobox(frame, state="readonly")
        self.category_combo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.load_categories()

        ttk.Label(frame, text="Цена:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.price_entry = ttk.Entry(frame)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame, text="Дата изменения цены:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        ttk.Button(frame, text="Добавить товар", command=self.add_product).grid(row=5, column=0, columnspan=2, pady=20)

        return frame

    def load_categories(self):
        try:
            response = requests.get("http://localhost:8000/categories/")
            response.raise_for_status()
            categories = response.json()
            
            self.category_ids = {cat["category_name"]: cat["category_id"] for cat in categories}
            
            self.category_combo["values"] = list(self.category_ids.keys())
            
            if self.category_combo["values"]:
                self.category_combo.current(0)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить категории:\n{e}")

    def add_product(self):
        product_name = self.name_entry.get().strip()
        manufacturer_id = self.manufacturer_entry.get().strip()
        category_name = self.category_combo.get()
        price = self.price_entry.get().strip()
        date_str = self.date_entry.get().strip()

        if not all([product_name, manufacturer_id, category_name, price, date_str]):
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        try:
            manufacturer_id = int(manufacturer_id)
            price = float(price)
            category_id = self.category_ids[category_name]
            
            try:
                date_price_change = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты. Используйте формат: ГГГГ-ММ-ДД ЧЧ:ММ:СС")
                return

            response = requests.post(
                "http://localhost:8000/products/",
                json={
                    "product_name": product_name,
                    "manufacturer_id": manufacturer_id,
                    "category_id": category_id,
                    "new_price": price,
                    "date_price_change": date_str
                }
            )
            
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Товар успешно добавлен")
                self.name_entry.delete(0, tk.END)
                self.manufacturer_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                messagebox.showerror("Ошибка", response.json().get("detail", "Неизвестная ошибка"))

        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте правильность введенных данных:\n- ID производителя должен быть целым числом\n- Цена должна быть числом")
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка при отправке запроса:\n{e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неизвестная ошибка:\n{e}")

    def create_purchases_tab(self, notebook):
        frame = ttk.Frame(notebook)

        purchases_frame = ttk.Frame(frame)
        purchases_frame.pack(fill="both", expand=True, padx=10, pady=5)

        purchase_cols = ("purchase_id", "purchase_date", "total_amount", "items_count")
        self.purchases_tree = ttk.Treeview(purchases_frame, columns=purchase_cols, show="headings")
        
        headers = {
            "purchase_id": "ID покупки",
            "purchase_date": "Дата",
            "total_amount": "Сумма",
            "items_count": "Кол-во товаров"
        }
        for col in purchase_cols:
            self.purchases_tree.heading(col, text=headers[col])
            self.purchases_tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(purchases_frame, orient="vertical", command=self.purchases_tree.yview)
        self.purchases_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.purchases_tree.pack(side="left", fill="both", expand=True)

        details_frame = ttk.Frame(frame)
        details_frame.pack(fill="both", expand=True, padx=10, pady=5)

        details_cols = ("product_id", "product_name", "product_count", "product_price")
        self.details_tree = ttk.Treeview(details_frame, columns=details_cols, show="headings")
        
        details_headers = {
            "product_id": "ID товара",
            "product_name": "Название",
            "product_count": "Количество",
            "product_price": "Цена"
        }
        for col in details_cols:
            self.details_tree.heading(col, text=details_headers[col])
            self.details_tree.column(col, anchor="center")

        details_scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=self.details_tree.yview)
        self.details_tree.configure(yscrollcommand=details_scrollbar.set)
        details_scrollbar.pack(side="right", fill="y")
        self.details_tree.pack(side="left", fill="both", expand=True)

        self.purchases_tree.bind("<<TreeviewSelect>>", self.on_purchase_select)

        refresh_btn = ttk.Button(frame, text="Обновить", command=self.load_purchases)
        refresh_btn.pack(pady=5)

        self.load_purchases()
        
        return frame

    def load_purchases(self):
        for item in self.purchases_tree.get_children():
            self.purchases_tree.delete(item)
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)

        try:
            response = requests.get(f"http://localhost:8000/purchases/user/{self.user_id}")
            response.raise_for_status()
            purchases = response.json()

            for purchase in purchases:
                total_amount = sum(item["product_price"] for item in purchase["items"])
                items_count = len(purchase["items"])
                
                purchase_date = datetime.fromisoformat(purchase["purchase_date"].replace("Z", "+00:00"))
                formatted_date = purchase_date.strftime("%Y-%m-%d %H:%M:%S")

                self.purchases_tree.insert("", "end", 
                    values=(
                        purchase["purchase_id"],
                        formatted_date,
                        f"{total_amount:.2f}",
                        items_count
                    ),
                    tags=(str(purchase["purchase_id"]),)
                )

        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить историю покупок:\n{e}")

    def on_purchase_select(self, event):
        
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)

        selected_items = self.purchases_tree.selection()
        if not selected_items:
            return

        purchase_id = self.purchases_tree.item(selected_items[0])["values"][0]

        try:
            
            response = requests.get(f"http://localhost:8000/purchases/user/{self.user_id}")
            purchases = response.json()
            
            purchase = next((p for p in purchases if p["purchase_id"] == purchase_id), None)
            if not purchase:
                return

            
            for item in purchase["items"]:
                product_id = item["product_id"]
                try:
                    
                    product_response = requests.get(
                        f"http://localhost:8000/products/{product_id}",
                        params={"include_unavailable": True}
                    )
                    if product_response.status_code == 200:
                        product = product_response.json()
                        product_name = product["product_name"]
                    else:
                        product_name = f"Товар {product_id}"
                except:
                    product_name = f"Товар {product_id}"

                self.details_tree.insert("", "end", values=(
                    product_id,
                    product_name,
                    item.get("product_count", 1),
                    f"{item['product_price']:.2f}"
                ))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить детали покупки:\n{str(e)}")

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()