from models import Product, Category
from data_loader import load_data_from_json


def main():
    """Основная функция для демонстрации работы классов."""
    print("=== Демонстрация работы с классами Product и Category ===\n")

    # Создание объектов вручную
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("Созданные товары:")
    print(f"1. {product1.name} - {product1.price} руб.")
    print(f"2. {product2.name} - {product2.price} руб.")
    print(f"3. {product3.name} - {product3.price} руб.")

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(f"\nКатегория: {category1.name}")
    print(f"Описание: {category1.description}")
    print(f"Количество товаров в категории: {len(category1.products)}")
    print(f"Общее количество категорий: {Category.category_count}")
    print(f"Общее количество товаров: {Category.product_count}")

    # Загрузка данных из JSON
    print("\n=== Загрузка данных из JSON ===\n")

    try:
        categories = load_data_from_json("products.json")

        print(f"Загружено категорий: {len(categories)}")
        print(f"Общее количество категорий (с учетом загруженных): {Category.category_count}")
        print(f"Общее количество товаров (с учетом загруженных): {Category.product_count}")

        for i, category in enumerate(categories, 1):
            print(f"\nКатегория {i}: {category.name}")
            print(f"Количество товаров: {len(category.products)}")
            for product in category.products:
                print(f"  - {product.name}: {product.price} руб. (осталось: {product.quantity})")

    except FileNotFoundError:
        print("Файл products.json не найден. Пожалуйста, убедитесь, что он находится в корне проекта.")


if __name__ == "__main__":
    main()
