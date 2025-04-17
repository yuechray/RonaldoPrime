import asyncio

from src.api.dependencies import get_app_settings
from src.db.postgres import get_async_session_factory
from src.services.categories import CategoriesRepository

async def run_cli():
    settings = get_app_settings()
    session_factory = await get_async_session_factory(settings)
    repo = CategoriesRepository(session_factory)

    while True:
        print("\n=== Категории ===")
        print("1. Показать все")
        print("2. Найти по ID")
        print("3. Найти по имени")
        print("4. Добавить")
        print("5. Обновить")
        print("6. Удалить")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            categories = await repo.get_all()
            for c in categories:
                print(f"{c.category_id}: {c.category_name}")

        elif choice == "2":
            category_id = int(input("Введите ID категории: "))
            category = await repo.get_by_id(category_id)
            print(category.category_name if category else "Категория не найдена")

        elif choice == "3":
            name = input("Введите имя (или часть): ")
            results = await repo.get_by_name(name)
            for c in results:
                print(f"{c.category_id}: {c.category_name}")

        elif choice == "4":
            name = input("Введите имя новой категории: ")
            new_cat = await repo.create(name)
            print(f"Создано: {new_cat.category_id}: {new_cat.category_name}")

        elif choice == "5":
            category_id = int(input("ID категории для обновления: "))
            new_name = input("Новое имя: ")
            updated = await repo.update(category_id, new_name)
            print("Обновлено" if updated else "Не найдено")

        elif choice == "6":
            category_id = int(input("ID категории для удаления: "))
            deleted = await repo.delete(category_id)
            print("Удалено" if deleted else "Не найдено")

        elif choice == "0":
            print("Выход.")
            break

        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    asyncio.run(run_cli())